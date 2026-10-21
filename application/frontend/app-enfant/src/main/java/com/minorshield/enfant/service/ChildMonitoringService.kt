package com.minorshield.enfant.service

import android.app.Activity
import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Intent
import android.graphics.Bitmap
import android.os.Build
import android.os.IBinder
import android.provider.Settings
import android.util.Log
import androidx.core.app.NotificationCompat
import com.minorshield.enfant.network.ChildApiClient
import com.minorshield.enfant.network.HeartbeatRequest
import com.minorshield.enfant.utils.ChildPreferencesManager
import com.minorshield.enfant.utils.ForegroundAppDetector
import com.minorshield.enfant.utils.ImageCompressor
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.cancel
import kotlinx.coroutines.delay
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.toRequestBody
import retrofit2.HttpException

class ChildMonitoringService : Service() {

    companion object {
        const val EXTRA_RESULT_CODE = "result_code"
        const val EXTRA_DATA        = "data"
        private const val TAG          = "ChildMonitoring"
        private const val CHANNEL_ID   = "ms_monitoring"
        private const val NOTIF_ID     = 2
        private const val CAPTURE_MS   = 2_500L   // capture toutes les 2.5s
        private const val HEARTBEAT_MS = 30_000L  // signal de vie toutes les 30s
    }

    private val scope          = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    private lateinit var captureManager    : ChildScreenCaptureManager
    private lateinit var prefs             : ChildPreferencesManager
    private lateinit var foregroundDetector: ForegroundAppDetector

    /** True dès que la capture est initialisée — évite de s'arrêter sur un intent vide tardif. */
    @Volatile private var isCapturing = false

    override fun onCreate() {
        super.onCreate()
        Log.i(TAG, "onCreate")
        prefs              = ChildPreferencesManager(this)
        captureManager     = ChildScreenCaptureManager(this)
        foregroundDetector = ForegroundAppDetector(this)
        createNotificationChannel()
        startForeground(NOTIF_ID, buildNotification())
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        // ATTENTION : Activity.RESULT_OK vaut -1. La valeur par défaut ci-dessous
        // doit donc être RESULT_CANCELED (0), jamais -1 — sinon un consentement
        // accordé est interprété comme "absent" et la capture ne démarre jamais.
        val resultCode = intent?.getIntExtra(EXTRA_RESULT_CODE, Activity.RESULT_CANCELED)
            ?: Activity.RESULT_CANCELED
        val data       = intent?.let { getProjectionData(it) }

        if (resultCode == Activity.RESULT_OK && data != null) {
            Log.i(TAG, "onStartCommand — jeton MediaProjection reçu, initialisation...")
            try {
                captureManager.initialize(resultCode, data) {
                    isCapturing = true
                    prefs.isCaptureRunning = true
                    // Nouvelle session de capture = état propre. Ces drapeaux sont
                    // persistés ; s'ils restaient bloqués (ex: warningActive d'un
                    // avertissement dont l'overlay ne s'était pas affiché), la
                    // capture serait mise en pause DÉFINITIVEMENT.
                    prefs.warningActive = false
                    prefs.graceUntil = 0L
                    Log.i(TAG, "Capture initialisée avec succès — démarrage de la boucle")
                    startMonitoringLoop()
                }
            } catch (e: Exception) {
                Log.e(TAG, "Échec de l'initialisation de la capture", e)
            }
        } else if (isCapturing) {
            // Un intent sans jeton est arrivé alors que la capture tourne déjà
            // (ex: intent vide mis en file avant le démarrage légitime).
            // On l'ignore : l'arrêter tuerait une capture parfaitement valide.
            Log.i(TAG, "Intent sans jeton ignoré — la capture est déjà active")
        } else {
            // Redémarrage du service (kill système, reboot) sans jeton MediaProjection —
            // impossible à récupérer sans nouvelle autorisation de l'utilisateur.
            // On le signale au lieu de rester actif silencieusement sans jamais capturer.
            Log.w(TAG, "Autorisation de capture manquante — arrêt et notification à l'utilisateur")
            // Prévenir le parent tout de suite que l'appareil n'est plus protégé,
            // sans attendre l'expiration du heartbeat côté serveur.
            scope.launch { sendHeartbeat(protectionActive = false) }
            notifyMonitoringStoppedAndStop(startId)
        }
        return START_STICKY
    }

    /** Lecture du jeton MediaProjection, compatible Android 13+ (API 33). */
    private fun getProjectionData(intent: Intent): Intent? =
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            intent.getParcelableExtra(EXTRA_DATA, Intent::class.java)
        } else {
            @Suppress("DEPRECATION") intent.getParcelableExtra(EXTRA_DATA)
        }

    private fun notifyMonitoringStoppedAndStop(startId: Int) {
        val notification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("MinorShield — Surveillance interrompue")
            .setContentText("Rouvrez l'app MinorShield pour réautoriser la capture d'écran")
            .setSmallIcon(android.R.drawable.ic_dialog_alert)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setAutoCancel(true)
            .build()

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
            stopForeground(STOP_FOREGROUND_DETACH)
        } else {
            @Suppress("DEPRECATION") stopForeground(false)
        }
        (getSystemService(NOTIFICATION_SERVICE) as NotificationManager).notify(NOTIF_ID, notification)
        // stopSelf(startId) — et non stopSelf() — pour ne PAS tuer le service si un
        // démarrage plus récent (avec jeton valide) est déjà arrivé entre-temps.
        stopSelf(startId)
    }

    private fun startMonitoringLoop() {
        scope.launch {
            Log.i(TAG, "Boucle de capture démarrée (intervalle ${CAPTURE_MS}ms)")
            var lastHeartbeat = 0L
            while (isActive) {
                // Le heartbeat est envoyé même quand l'appareil est verrouillé :
                // la protection est bien active, c'est la capture qui est en pause.
                if (System.currentTimeMillis() - lastHeartbeat >= HEARTBEAT_MS) {
                    sendHeartbeat(protectionActive = isProtectionOperational())
                    lastHeartbeat = System.currentTimeMillis()
                }
                when {
                    prefs.isLocked -> Unit       // blocage total : rien à analyser
                    prefs.warningActive -> Unit  // avertissement affiché : capture en pause
                    isInGracePeriod() -> Unit    // déblocage/quitter récent : on laisse le temps de quitter
                    else -> runCaptureCycle()
                }
                delay(CAPTURE_MS)
            }
            Log.w(TAG, "Boucle de capture arrêtée (scope non actif)")
        }
    }

    /**
     * Vrai si l'image est quasi entièrement noire (échantillonnage d'une grille
     * de pixels). Signe typique d'une surface vidéo protégée (DRM) que
     * MediaProjection ne peut pas capturer.
     */
    private fun isMostlyBlack(bitmap: Bitmap): Boolean {
        val steps = 12
        val w = bitmap.width
        val h = bitmap.height
        if (w == 0 || h == 0) return true

        var dark = 0
        var total = 0
        for (i in 1 until steps) {
            for (j in 1 until steps) {
                val px = bitmap.getPixel(w * i / steps, h * j / steps)
                val r = (px shr 16) and 0xFF
                val g = (px shr 8) and 0xFF
                val b = px and 0xFF
                if (r < 16 && g < 16 && b < 16) dark++
                total++
            }
        }
        // Plus de 96% de pixels quasi-noirs → considéré comme noir (DRM)
        return total > 0 && dark.toFloat() / total > 0.96f
    }

    /**
     * Après un déblocage par le parent, on suspend l'analyse un court instant :
     * le contenu incriminé est souvent encore affiché, et le ré-analyser
     * re-verrouillerait l'appareil immédiatement — le déblocage semblerait
     * alors ne pas fonctionner.
     */
    private fun isInGracePeriod(): Boolean {
        val remaining = prefs.graceUntil - System.currentTimeMillis()
        if (remaining <= 0) return false
        Log.d(TAG, "Analyse en pause (déblocage récent) — ${remaining / 1000}s restantes")
        return true
    }

    /**
     * La protection n'est réelle que si les DEUX briques fonctionnent :
     * la capture d'écran (MediaProjection) et l'overlay de blocage.
     * Sans overlay, on détecte mais on ne bloque rien — l'utilisateur croirait
     * à tort être protégé.
     */
    private fun isProtectionOperational(): Boolean {
        val canOverlay =
            Build.VERSION.SDK_INT < Build.VERSION_CODES.M || Settings.canDrawOverlays(this)
        return isCapturing && canOverlay
    }

    private fun showWarningOverlay(remaining: Int, limit: Int, reason: String?) {
        val intent = Intent(this, OverlayService::class.java).apply {
            action = OverlayService.ACTION_WARNING
            putExtra(OverlayService.EXTRA_REMAINING, remaining)
            putExtra(OverlayService.EXTRA_LIMIT, limit)
            putExtra(OverlayService.EXTRA_REASON, reason)
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) startForegroundService(intent)
        else startService(intent)
    }

    private suspend fun sendHeartbeat(protectionActive: Boolean) {
        val childId = prefs.childId ?: return
        val canOverlay =
            Build.VERSION.SDK_INT < Build.VERSION_CODES.M || Settings.canDrawOverlays(this)
        try {
            ChildApiClient.service.sendHeartbeat(
                childId,
                HeartbeatRequest(
                    protection_active = protectionActive,
                    capture_active    = isCapturing,
                    overlay_allowed   = canOverlay,
                    usage_access      = ForegroundAppDetector.hasUsageAccess(this),
                )
            )
        } catch (e: Exception) {
            Log.d(TAG, "Heartbeat non envoyé (serveur injoignable)")
        }
    }

    private suspend fun runCaptureCycle() {
        val childId = prefs.childId
        if (childId == null) {
            Log.w(TAG, "Cycle ignoré — aucun childId enregistré")
            return
        }
        val bitmap = captureManager.captureScreen()
        if (bitmap == null) {
            Log.d(TAG, "Cycle ignoré — aucune image disponible (imageReader vide ou non initialisé)")
            return
        }

        // Une capture quasi-noire vient presque toujours d'un contenu vidéo
        // protégé par DRM (Netflix, YouTube protégé...) : Android rend ces
        // surfaces en noir, on ne peut pas les analyser. Inutile d'envoyer une
        // image noire au serveur (elle serait scorée "safe" à tort). On la
        // signale et on saute le cycle.
        if (isMostlyBlack(bitmap)) {
            Log.w(TAG, "Capture quasi-noire — contenu protégé DRM ? Cycle ignoré")
            bitmap.recycle()
            return
        }

        try {
            val bytes       = ImageCompressor.compress(bitmap)
            val imagePart   = MultipartBody.Part.createFormData(
                "image", "screenshot.jpg",
                bytes.toRequestBody("image/jpeg".toMediaTypeOrNull())
            )
            val childPart   = childId.toRequestBody("text/plain".toMediaTypeOrNull())

            // L'app réellement au premier plan, avec son nom lisible résolu
            // localement. Auparavant on envoyait notre propre package en dur,
            // d'où le "com.minorshield.enfant" affiché au parent.
            val foreground  = foregroundDetector.current()
            val packagePart = (foreground?.packageName ?: "")
                .toRequestBody("text/plain".toMediaTypeOrNull())
            val namePart    = (foreground?.appName ?: "")
                .toRequestBody("text/plain".toMediaTypeOrNull())

            val result = ChildApiClient.service.detect(imagePart, childPart, packagePart, namePart)

            val score = maxOf(result.nsfw_score, result.image_score)
            Log.d(TAG, "Analyse reçue — score=$score, label=${result.label}, categorie=${result.category}")

            // C'est le backend qui décide : ses règles sont plus fines qu'un seuil
            // brut. Sur "nsfw", on fait avancer le système d'avertissements.
            if (result.label == "nsfw") {
                val incident = ChildApiClient.service.reportIncident(childId)
                Log.i(TAG, "Contenu inapproprié (${result.category}) — ${incident.status}, " +
                        "restant=${incident.remaining}/${incident.warning_limit}")
                if (incident.status == "blocked") {
                    // Quota épuisé : blocage total (OverlayService l'affichera via
                    // son polling, dans les 3s).
                    prefs.isLocked = true
                    prefs.graceUntil = 0L
                } else {
                    // Avertissement : écran dismissible avec bouton Quitter.
                    prefs.warningActive = true
                    showWarningOverlay(incident.remaining, incident.warning_limit, result.category)
                }
            }
        } catch (e: HttpException) {
            if (e.code() == 404) {
                // Enfant supprimé par le parent : inutile de continuer à
                // envoyer des captures. OverlayService gère la déliaison.
                Log.i(TAG, "Enfant introuvable côté serveur — arrêt de la surveillance")
                stopSelf()
            } else {
                Log.w(TAG, "Échec de l'analyse (HTTP ${e.code()}) — nouvel essai au prochain cycle")
            }
        } catch (e: Exception) {
            Log.w(TAG, "Échec de l'analyse d'une capture — nouvelle tentative au prochain cycle", e)
        } finally {
            bitmap.recycle()
        }
    }

    override fun onDestroy() {
        Log.w(TAG, "onDestroy — la capture s'arrête")
        isCapturing = false
        prefs.isCaptureRunning = false
        scope.cancel()
        captureManager.release()
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null

    private fun buildNotification(): Notification =
        NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("MinorShield — Analyse en cours")
            .setContentText("Surveillance des contenus active")
            .setSmallIcon(android.R.drawable.ic_lock_idle_lock)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .setOngoing(true)
            .build()

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID, "Surveillance MinorShield",
                NotificationManager.IMPORTANCE_LOW
            )
            (getSystemService(NOTIFICATION_SERVICE) as NotificationManager)
                .createNotificationChannel(channel)
        }
    }
}
