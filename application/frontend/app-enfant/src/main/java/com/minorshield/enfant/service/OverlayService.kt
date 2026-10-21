package com.minorshield.enfant.service

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Intent
import android.graphics.PixelFormat
import android.view.ContextThemeWrapper
import android.os.Build
import android.os.IBinder
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.WindowManager
import android.widget.TextView
import androidx.core.app.NotificationCompat
import com.minorshield.enfant.R
import com.minorshield.enfant.network.ChildApiClient
import com.minorshield.enfant.ui.PairingActivity
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.cancel
import kotlinx.coroutines.delay
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import retrofit2.HttpException

class OverlayService : Service() {

    companion object {
        const val EXTRA_CHILD_ID = "child_id"
        const val ACTION_WARNING = "com.minorshield.enfant.SHOW_WARNING"
        const val EXTRA_REMAINING = "remaining"
        const val EXTRA_LIMIT     = "limit"
        const val EXTRA_REASON    = "reason"
        private const val TAG         = "OverlayService"
        private const val CHANNEL_ID  = "minorshield_overlay"
        private const val NOTIF_ID    = 1
        private const val POLL_MS     = 3_000L
        // Délai laissé à l'enfant pour quitter le contenu après un déblocage
        private const val GRACE_MS    = 60_000L
        // Délai après une détection ("Quitter") avant de reprendre l'analyse :
        // laisse le temps de quitter le contenu avant de recapturer.
        private const val QUIT_GRACE_MS = 10_000L
        // Compte à rebours sur l'écran d'avertissement : si l'enfant n'appuie
        // pas sur "Quitter", l'écran se ferme automatiquement après ce délai.
        private const val QUIT_COUNTDOWN_MS = 5_000L
    }

    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    private var windowManager: WindowManager? = null
    private var overlayView: View? = null
    // null | "warning" | "block". Le blocage total est prioritaire sur l'avertissement.
    private var overlayMode: String? = null
    private var quitTimer: android.os.CountDownTimer? = null
    private var pollingStarted = false
    private var childId = ""
    private lateinit var prefs: com.minorshield.enfant.utils.ChildPreferencesManager

    override fun onCreate() {
        super.onCreate()
        prefs         = com.minorshield.enfant.utils.ChildPreferencesManager(this)
        windowManager = getSystemService(WINDOW_SERVICE) as WindowManager
        createNotificationChannel()
        startForeground(NOTIF_ID, buildNotification())
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        // Demande d'affichage d'un avertissement (déclenché par la détection).
        if (intent?.action == ACTION_WARNING) {
            val remaining = intent.getIntExtra(EXTRA_REMAINING, 0)
            val limit     = intent.getIntExtra(EXTRA_LIMIT, 3)
            val reason    = intent.getStringExtra(EXTRA_REASON)
            showWarning(remaining, limit, reason)
            return START_STICKY
        }

        // Après un redémarrage du service par le système, l'Intent d'origine
        // n'est pas redélivré (extras perdus) — on retombe sur la valeur
        // persistée en préférences, qui elle survit à un kill/reboot.
        val fromIntent = intent?.getStringExtra(EXTRA_CHILD_ID)
        childId = if (!fromIntent.isNullOrBlank()) fromIntent else prefs.childId.orEmpty()

        if (childId.isBlank()) {
            Log.w(TAG, "childId introuvable — arrêt du service overlay")
            stopSelf()
        } else if (!pollingStarted) {
            pollingStarted = true
            startPolling()
        }
        return START_STICKY
    }

    private fun startPolling() {
        scope.launch {
            while (isActive) {
                try {
                    val status = ChildApiClient.service.getLockStatus(childId)
                    launch(Dispatchers.Main) {
                        // Transition verrouillé → déverrouillé = le parent vient
                        // de débloquer. On accorde un délai de grâce, sinon le
                        // contenu encore à l'écran serait re-détecté et
                        // re-verrouillerait l'appareil en quelques secondes.
                        if (prefs.isLocked && !status.is_locked) {
                            prefs.graceUntil = System.currentTimeMillis() + GRACE_MS
                            prefs.warningActive = false
                            Log.i(TAG, "Déblocage parent — pause de ${GRACE_MS / 1000}s avant reprise")
                        }
                        prefs.isLocked = status.is_locked
                        // Blocage total (quota épuisé) : prioritaire, retire tout
                        // avertissement en cours.
                        if (status.is_locked) showBlock(status.reason)
                        else if (overlayMode == "block") hideOverlay()
                    }
                } catch (e: HttpException) {
                    if (e.code() == 404) {
                        // L'enfant n'existe plus côté serveur : le parent l'a
                        // supprimé. On délie l'appareil au lieu de continuer à
                        // interroger un identifiant mort indéfiniment.
                        Log.i(TAG, "Enfant supprimé par le parent — déliaison de l'appareil")
                        launch(Dispatchers.Main) { handleChildRemoved() }
                        return@launch
                    }
                    Log.w(TAG, "Échec de la vérification du statut (HTTP ${e.code()})")
                } catch (e: Exception) {
                    Log.w(TAG, "Échec de la vérification du statut de verrouillage", e)
                }
                delay(POLL_MS)
            }
        }
    }

    private fun overlayParams(): WindowManager.LayoutParams {
        // NON focusable dans les deux cas : un overlay plein écran focusable
        // lancé depuis un service en arrière-plan est bloqué par certaines ROMs
        // (MIUI/Xiaomi). Les boutons d'un overlay non-focusable restent
        // cliquables — c'est le motif standard pour un bouton d'overlay.
        return WindowManager.LayoutParams(
            WindowManager.LayoutParams.MATCH_PARENT,
            WindowManager.LayoutParams.MATCH_PARENT,
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O)
                WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
            else
                @Suppress("DEPRECATION") WindowManager.LayoutParams.TYPE_SYSTEM_ALERT,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or
                WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN or
                WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON,
            PixelFormat.TRANSLUCENT
        )
    }

    /**
     * Un contexte Service n'a PAS de thème Material. Les composants Material
     * (MaterialButton...) exigent Theme.MaterialComponents et plantent sinon.
     * On habille donc le contexte d'inflation avec le thème de l'app.
     */
    private fun themedInflater(): LayoutInflater =
        LayoutInflater.from(ContextThemeWrapper(this, R.style.Theme_MinorShieldEnfant))

    /** Blocage TOTAL : quota d'avertissements épuisé, aucun bouton de sortie. */
    private fun showBlock(reason: String? = null) {
        if (overlayMode == "block") return
        hideOverlay()   // remplace un éventuel avertissement

        val view = themedInflater().inflate(R.layout.overlay_blocked, null)
        addOverlay(view, mode = "block")
    }

    /** AVERTISSEMENT : dismissible via "Quitter" tant qu'il reste des avertissements. */
    private fun showWarning(remaining: Int, limit: Int, reason: String? = null) {
        if (overlayMode == "block") return  // le blocage total est prioritaire
        prefs.warningActive = true
        hideOverlay()

        val view = themedInflater().inflate(R.layout.overlay_warning, null)

        // Catégorie du contenu détecté (nudité / violence / texte), sous le titre.
        labelForReason(reason)?.let { label ->
            view.findViewById<TextView>(R.id.tvWarningCategory)?.apply {
                text = label
                visibility = View.VISIBLE
            }
        }

        // limit <= 0 → quota « illimité » : pas de décompte, seulement l'alerte.
        view.findViewById<TextView>(R.id.tvWarningCount)?.text = if (limit <= 0) {
            "Contenu inapproprié détecté et masqué."
        } else {
            val plural = if (remaining > 1) "avertissements" else "avertissement"
            "Il vous reste $remaining/$limit $plural avant la restriction prévue par l'administrateur."
        }

        val btnQuit = view.findViewById<com.google.android.material.button.MaterialButton>(R.id.btnQuit)
        btnQuit?.setOnClickListener { onQuit() }

        // Compte à rebours : si l'enfant n'appuie pas sur "Quitter", l'écran se
        // ferme automatiquement au bout de QUIT_COUNTDOWN_MS.
        quitTimer?.cancel()
        quitTimer = object : android.os.CountDownTimer(QUIT_COUNTDOWN_MS, 1_000L) {
            override fun onTick(msLeft: Long) {
                btnQuit?.text = "Quitter (${Math.ceil(msLeft / 1000.0).toInt()})"
            }
            override fun onFinish() {
                btnQuit?.text = "Quitter"
                onQuit()
            }
        }.start()

        addOverlay(view, mode = "warning")
    }

    /** Traduit la catégorie technique du backend en libellé lisible. */
    private fun labelForReason(reason: String?): String? = when (reason) {
        "nudite"   -> "Nudité"
        "violence" -> "Violence"
        "texte"    -> "Texte inapproprié"
        else       -> null
    }

    /** "Quitter" : ferme l'avertissement, renvoie à l'accueil, met l'analyse en pause. */
    private fun onQuit() {
        prefs.warningActive = false
        prefs.graceUntil = System.currentTimeMillis() + QUIT_GRACE_MS
        hideOverlay()
        // Renvoie l'enfant à l'écran d'accueil du téléphone (le contenu
        // incriminé n'est alors plus affiché).
        startActivity(
            Intent(Intent.ACTION_MAIN)
                .addCategory(Intent.CATEGORY_HOME)
                .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        )
    }

    private fun addOverlay(view: View, mode: String) {
        try {
            windowManager?.addView(view, overlayParams())
            overlayView = view
            overlayMode = mode
            Log.i(TAG, "Overlay '$mode' affiché")
        } catch (e: Exception) {
            Log.e(TAG, "Impossible d'afficher l'overlay '$mode'", e)
        }
    }

    /**
     * Le parent a supprimé cet enfant : on retire le blocage, on arrête la
     * surveillance, on efface les données locales et on renvoie l'appareil à
     * l'écran de liaison.
     */
    private fun handleChildRemoved() {
        hideOverlay()
        stopService(Intent(this, ChildMonitoringService::class.java))
        prefs.clear()

        startActivity(
            Intent(this, PairingActivity::class.java)
                .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK)
        )
        stopSelf()
    }

    private fun hideOverlay() {
        quitTimer?.cancel()
        quitTimer = null
        val v = overlayView ?: return
        try {
            windowManager?.removeView(v)
        } catch (_: Exception) { }
        overlayView = null
        overlayMode = null
    }

    override fun onDestroy() {
        hideOverlay()
        scope.cancel()
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null

    private fun buildNotification(): Notification =
        NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("MinorShield actif")
            .setContentText("Protection en cours...")
            .setSmallIcon(android.R.drawable.ic_lock_idle_lock)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .setOngoing(true)
            .build()

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "MinorShield Protection",
                NotificationManager.IMPORTANCE_LOW
            ).apply { description = "Service de protection MinorShield" }
            (getSystemService(NOTIFICATION_SERVICE) as NotificationManager)
                .createNotificationChannel(channel)
        }
    }
}
