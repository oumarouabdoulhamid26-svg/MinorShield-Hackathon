package com.minorshield.enfant.ui

import android.Manifest
import android.app.AlertDialog
import android.content.Intent
import android.content.pm.PackageManager
import android.media.projection.MediaProjectionManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.provider.Settings
import android.view.LayoutInflater
import android.view.View
import android.widget.EditText
import android.widget.ProgressBar
import android.widget.TextView
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.lifecycle.lifecycleScope
import com.minorshield.enfant.R
import com.minorshield.enfant.databinding.EnfantActivityMainBinding
import com.minorshield.enfant.network.ChildApiClient
import com.minorshield.enfant.network.VerifyPinRequest
import com.minorshield.enfant.service.ChildMonitoringService
import com.minorshield.enfant.service.OverlayService
import com.minorshield.enfant.utils.ChildPreferencesManager
import com.minorshield.enfant.utils.ForegroundAppDetector
import kotlinx.coroutines.launch
import retrofit2.HttpException

class MainActivity : AppCompatActivity() {

    private lateinit var binding: EnfantActivityMainBinding
    private lateinit var prefs  : ChildPreferencesManager

    private val OVERLAY_PERM_CODE     = 1001
    private val MEDIA_PROJECTION_CODE = 1002

    private val notificationPermissionLauncher =
        registerForActivityResult(ActivityResultContracts.RequestPermission()) {
            // Qu'elle soit accordée ou refusée, on continue le parcours —
            // sans elle les notifications de statut seront juste invisibles.
            checkOverlayPermission()
        }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = EnfantActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        prefs = ChildPreferencesManager(this)
        binding.tvChildName.text = prefs.childName ?: "Enfant"

        binding.btnDisconnect.setOnClickListener { disconnectDevice() }
        // Le listener de btnFixPermissions est défini dans refreshProtectionStatus(),
        // car l'action dépend de la permission réellement manquante.

        checkPermissionsAndStart()
    }

    override fun onResume() {
        super.onResume()
        // Les autorisations peuvent être révoquées à tout moment (réinstallation,
        // réglages système, redémarrage). On revérifie à chaque ouverture plutôt
        // qu'au seul premier lancement, sinon la protection tombe en silence.
        refreshProtectionStatus()
    }

    private fun refreshProtectionStatus() {
        val canOverlay =
            Build.VERSION.SDK_INT < Build.VERSION_CODES.M || Settings.canDrawOverlays(this)
        val capturing  = prefs.isCaptureRunning
        val hasUsage   = ForegroundAppDetector.hasUsageAccess(this)

        // La carte principale était codée en dur sur "Tu es protégé" : elle
        // affirmait la protection même capture coupée. On la met en accord
        // avec l'état réel — un enfant (et son parent) doivent pouvoir s'y fier.
        renderStatusCard(protected = capturing && canOverlay)
        renderChecklist(capturing, canOverlay, hasUsage)

        // Les deux premières briques sont vitales (sans elles, rien n'est bloqué).
        // L'accès aux données d'usage est secondaire : la protection fonctionne
        // sans, mais le parent ne saura pas DANS QUELLE application le contenu
        // a été vu.
        val problem = when {
            !canOverlay && !capturing ->
                "La protection n'est pas encore activée. Appuie sur le bouton pour l'activer."
            !canOverlay ->
                "Il manque une autorisation pour bloquer les contenus. Appuie pour l'activer."
            !capturing ->
                "L'analyse de l'écran est en pause. Appuie pour la relancer."
            !hasUsage ->
                "Une autorisation en plus permet d'indiquer à tes parents dans quelle " +
                "application un contenu a été vu."
            else -> null
        }

        if (problem == null) {
            binding.cardWarning.visibility = View.GONE
            return
        }

        binding.tvWarningDetail.text = problem
        binding.cardWarning.visibility = View.VISIBLE

        // Cette permission ne peut pas être accordée par une popup : on envoie
        // directement l'utilisateur à l'écran système correspondant.
        val usageOnly = canOverlay && capturing && !hasUsage
        binding.tvWarningTitle.text =
            if (usageOnly) "ℹ️ Information manquante" else "⚠️ Protection incomplète"
        binding.btnFixPermissions.text =
            if (usageOnly) "Autoriser l'accès aux données" else "Réactiver la protection"
        binding.btnFixPermissions.setOnClickListener {
            if (usageOnly) openUsageAccessSettings() else checkPermissionsAndStart()
        }
    }

    /** Affiche l'état des 3 briques : accordée (✓ teal) ou manquante (✗ rouge). */
    private fun renderChecklist(capturing: Boolean, canOverlay: Boolean, hasUsage: Boolean) {
        bindCheckRow(binding.checkCaptureIcon, binding.checkCaptureStatus, capturing,
            okText = "Active", koText = "À autoriser")
        bindCheckRow(binding.checkOverlayIcon, binding.checkOverlayStatus, canOverlay,
            okText = "Autorisé", koText = "À autoriser")
        bindCheckRow(binding.checkUsageIcon, binding.checkUsageStatus, hasUsage,
            okText = "Autorisée", koText = "Optionnelle")
    }

    private fun bindCheckRow(
        icon: android.widget.TextView,
        status: android.widget.TextView,
        granted: Boolean,
        okText: String,
        koText: String,
    ) {
        if (granted) {
            icon.text = "✓"
            icon.setTextColor(getColor(R.color.enfant_teal))
            status.text = okText
            status.setTextColor(getColor(R.color.enfant_teal))
        } else {
            icon.text = "✗"
            icon.setTextColor(getColor(R.color.danger))
            status.text = koText
            status.setTextColor(getColor(R.color.danger))
        }
    }

    /** Met la carte principale en accord avec l'état réel de la surveillance. */
    private fun renderStatusCard(protected: Boolean) {
        if (protected) {
            binding.shieldCircle.setBackgroundResource(R.drawable.bg_teal_circle)
            binding.ivShield.setImageResource(R.drawable.ic_shield_safe)
            binding.tvStatusTitle.text    = "Tu es protégé"
            binding.tvStatusSubtitle.text = "Tes parents veillent sur toi"
            binding.statusBadge.setBackgroundResource(R.drawable.bg_safe_badge)
            binding.badgeDot.setBackgroundResource(R.drawable.bg_active_dot_teal)
            binding.tvStatusBadge.text = "Surveillance active"
            binding.tvStatusBadge.setTextColor(getColor(R.color.enfant_teal))
            binding.tvHeaderStatus.text = "Actif"
        } else {
            binding.shieldCircle.setBackgroundResource(R.drawable.bg_alert_circle)
            binding.ivShield.setImageResource(R.drawable.ic_shield_safe)
            binding.tvStatusTitle.text    = "Protection interrompue"
            binding.tvStatusSubtitle.text = "Une autorisation est nécessaire pour te protéger"
            binding.statusBadge.setBackgroundResource(R.drawable.bg_alert_badge)
            binding.badgeDot.setBackgroundResource(R.drawable.bg_alert_dot)
            binding.tvStatusBadge.text = "Surveillance inactive"
            binding.tvStatusBadge.setTextColor(getColor(R.color.danger))
            binding.tvHeaderStatus.text = "Inactif"
        }
    }

    private fun openUsageAccessSettings() {
        Toast.makeText(
            this,
            "Sélectionne MinorShield Enfant, puis active l'accès",
            Toast.LENGTH_LONG
        ).show()
        try {
            startActivity(ForegroundAppDetector.usageAccessSettingsIntent())
        } catch (_: Exception) {
            Toast.makeText(this, "Réglage introuvable sur cet appareil", Toast.LENGTH_SHORT).show()
        }
    }

    private fun disconnectDevice() {
        val childId = prefs.childId
        if (childId == null) {
            Toast.makeText(this, "Appareil non appairé", Toast.LENGTH_SHORT).show()
            return
        }

        val view    = LayoutInflater.from(this).inflate(R.layout.dialog_disconnect, null)
        val etPin   = view.findViewById<EditText>(R.id.etPin)
        val tvError = view.findViewById<TextView>(R.id.tvError)
        val progress = view.findViewById<ProgressBar>(R.id.progress)

        val dialog = AlertDialog.Builder(this)
            .setTitle("Déconnexion protégée")
            .setView(view)
            .setPositiveButton("Déconnecter", null)
            .setNegativeButton("Annuler", null)
            .create()

        dialog.setOnShowListener {
            val btn = dialog.getButton(AlertDialog.BUTTON_POSITIVE)
            btn.setOnClickListener {
                val pin = etPin.text?.toString().orEmpty()
                tvError.visibility = View.GONE

                if (pin.isBlank()) {
                    showDialogError(tvError, "Saisis le code PIN de ton parent")
                    return@setOnClickListener
                }

                btn.isEnabled = false
                progress.visibility = View.VISIBLE

                lifecycleScope.launch {
                    val outcome = attemptDisconnect(childId, pin)
                    progress.visibility = View.GONE

                    when (outcome) {
                        DisconnectOutcome.SUCCESS -> {
                            dialog.dismiss()
                            finishDisconnectLocally()
                        }
                        DisconnectOutcome.WRONG_PIN -> {
                            btn.isEnabled = true
                            showDialogError(tvError, "Code PIN incorrect")
                        }
                        DisconnectOutcome.NO_PIN -> {
                            btn.isEnabled = true
                            showDialogError(
                                tvError,
                                "Aucun PIN n'a été défini par ton parent — déconnexion impossible"
                            )
                        }
                        DisconnectOutcome.NETWORK -> {
                            btn.isEnabled = true
                            showDialogError(
                                tvError,
                                "Serveur injoignable — réessaie une fois connecté à Internet"
                            )
                        }
                    }
                }
            }
        }

        dialog.show()
    }

    private enum class DisconnectOutcome { SUCCESS, WRONG_PIN, NO_PIN, NETWORK }

    /**
     * Vérifie le PIN puis délie l'appareil côté serveur.
     *
     * On ne nettoie rien localement tant que le serveur n'a pas confirmé la
     * déliaison : sinon l'appareil se détacherait alors que le parent
     * continuerait de voir l'enfant comme appairé.
     */
    private suspend fun attemptDisconnect(childId: String, pin: String): DisconnectOutcome {
        return try {
            val result = ChildApiClient.service.verifyPin(childId, VerifyPinRequest(pin))
            when {
                !result.pin_configured -> DisconnectOutcome.NO_PIN
                !result.valid          -> DisconnectOutcome.WRONG_PIN
                else -> {
                    ChildApiClient.service.unpairDevice(childId)
                    DisconnectOutcome.SUCCESS
                }
            }
        } catch (e: HttpException) {
            // 404 : l'enfant a déjà été supprimé par le parent → la déliaison
            // locale est légitime, l'appareil n'a plus rien à surveiller.
            if (e.code() == 404) DisconnectOutcome.SUCCESS else DisconnectOutcome.NETWORK
        } catch (e: Exception) {
            DisconnectOutcome.NETWORK
        }
    }

    /** Arrête la surveillance, purge les données locales et revient à la liaison. */
    private fun finishDisconnectLocally() {
        stopService(Intent(this, ChildMonitoringService::class.java))
        stopService(Intent(this, OverlayService::class.java))
        prefs.clearPairingKeepingServer()

        Toast.makeText(this, "Appareil déconnecté", Toast.LENGTH_SHORT).show()
        startActivity(
            Intent(this, PairingActivity::class.java)
                .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK)
        )
        finish()
    }

    private fun showDialogError(view: TextView, message: String) {
        view.text = message
        view.visibility = View.VISIBLE
    }

    // ── Étape 1 : permission notifications (Android 13+) ─────────────────────

    private fun checkPermissionsAndStart() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU &&
            ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS)
                != PackageManager.PERMISSION_GRANTED
        ) {
            notificationPermissionLauncher.launch(Manifest.permission.POST_NOTIFICATIONS)
        } else {
            checkOverlayPermission()
        }
    }

    // ── Étape 2 : permission overlay ──────────────────────────────────────────

    private fun checkOverlayPermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M && !Settings.canDrawOverlays(this)) {
            Toast.makeText(this,
                "Autorise MinorShield à s'afficher par-dessus les autres apps",
                Toast.LENGTH_LONG).show()
            startActivityForResult(
                Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                    Uri.parse("package:$packageName")),
                OVERLAY_PERM_CODE
            )
        } else {
            requestMediaProjection()
        }
    }

    // ── Étape 3 : permission MediaProjection ─────────────────────────────────

    private fun requestMediaProjection() {
        val mgr = getSystemService(MEDIA_PROJECTION_SERVICE) as MediaProjectionManager
        startActivityForResult(mgr.createScreenCaptureIntent(), MEDIA_PROJECTION_CODE)
    }

    // ── Résultats des permissions ─────────────────────────────────────────────

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        when (requestCode) {
            OVERLAY_PERM_CODE -> {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M && Settings.canDrawOverlays(this)) {
                    requestMediaProjection()
                } else {
                    Toast.makeText(this,
                        "Permission refusée — l'overlay de blocage ne fonctionnera pas",
                        Toast.LENGTH_SHORT).show()
                    requestMediaProjection()
                }
            }

            MEDIA_PROJECTION_CODE -> {
                val childId = prefs.childId ?: return
                startOverlayService(childId)
                if (resultCode == RESULT_OK && data != null) {
                    startMonitoringService(resultCode, data, childId)
                } else {
                    Toast.makeText(this,
                        "Capture d'écran refusée — la détection automatique est désactivée",
                        Toast.LENGTH_LONG).show()
                }
            }
        }
    }

    // ── Démarrage des services ────────────────────────────────────────────────

    private fun startOverlayService(childId: String) {
        val intent = Intent(this, OverlayService::class.java)
            .putExtra(OverlayService.EXTRA_CHILD_ID, childId)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O)
            startForegroundService(intent)
        else
            startService(intent)
    }

    private fun startMonitoringService(resultCode: Int, data: Intent, childId: String) {
        val intent = Intent(this, ChildMonitoringService::class.java)
            .putExtra(ChildMonitoringService.EXTRA_RESULT_CODE, resultCode)
            .putExtra(ChildMonitoringService.EXTRA_DATA, data)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O)
            startForegroundService(intent)
        else
            startService(intent)
    }
}
