package com.minorshield.ui

import android.app.AlertDialog
import android.os.Bundle
import android.text.InputType
import android.view.Gravity
import android.view.View
import android.widget.EditText
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import com.minorshield.network.ChildUpdateRequest
import androidx.core.content.ContextCompat
import androidx.lifecycle.lifecycleScope
import com.minorshield.R
import com.minorshield.databinding.ActivityChildDetailBinding
import com.minorshield.network.ChildResponse
import com.minorshield.network.ParentApiClient
import com.minorshield.network.WarningLimitRequest
import com.minorshield.utils.ChildAvatar
import com.minorshield.utils.ParentPreferencesManager
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.TimeZone

/**
 * Fiche détaillée d'un enfant : identité, appareil lié, état réel de la
 * protection et activité de détection.
 */
class ChildDetailActivity : AppCompatActivity() {

    companion object {
        const val EXTRA_CHILD_ID = "child_id"
    }

    private lateinit var binding: ActivityChildDetailBinding
    private lateinit var prefs  : ParentPreferencesManager
    private var childId: String = ""

    // Sélecteur d'image système (aucune permission requise).
    private val pickAvatar = registerForActivityResult(
        ActivityResultContracts.GetContent()
    ) { uri ->
        if (uri != null && childId.isNotBlank()) {
            if (com.minorshield.utils.PhotoStorage.copyFrom(
                    this, uri, com.minorshield.utils.PhotoStorage.childFile(this, childId))) {
                showChildAvatar()
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityChildDetailBinding.inflate(layoutInflater)
        setContentView(binding.root)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        title = "Fiche enfant"

        prefs   = ParentPreferencesManager(this)
        childId = intent.getStringExtra(EXTRA_CHILD_ID).orEmpty()

        if (childId.isBlank()) {
            Toast.makeText(this, "Enfant introuvable", Toast.LENGTH_SHORT).show()
            finish()
            return
        }

        binding.avatarChild.setOnClickListener { pickAvatar.launch("image/*") }
    }

    /** Affiche la photo de l'enfant si définie, sinon l'initiale colorée. */
    private fun showChildAvatar() {
        val file = com.minorshield.utils.PhotoStorage.childFile(this, childId)
        val hasPhoto = com.minorshield.utils.PhotoStorage.loadInto(binding.ivAvatar, file)
        binding.ivAvatar.visibility = if (hasPhoto) View.VISIBLE else View.GONE
        binding.tvAvatar.visibility = if (hasPhoto) View.GONE else View.VISIBLE
    }

    override fun onResume() {
        super.onResume()
        // Rechargé à chaque affichage : l'état de protection évolue en continu.
        loadChild()
    }

    private fun loadChild() {
        lifecycleScope.launch {
            try {
                val child = ParentApiClient.service.getChildren().children
                    .firstOrNull { it.id == childId }

                if (child == null) {
                    Toast.makeText(
                        this@ChildDetailActivity,
                        "Cet enfant n'existe plus",
                        Toast.LENGTH_SHORT
                    ).show()
                    finish()
                    return@launch
                }
                render(child)
            } catch (e: Exception) {
                Toast.makeText(
                    this@ChildDetailActivity,
                    "Serveur injoignable — impossible de charger la fiche",
                    Toast.LENGTH_SHORT
                ).show()
            }
        }
    }

    private fun render(child: ChildResponse) {
        // ── Identité ─────────────────────────────────────────────────
        binding.tvAvatar.text = ChildAvatar.initialOf(child.name)
        binding.tvAvatar.background = ChildAvatar.circleFor(child.name)
        showChildAvatar()
        binding.tvName.text = child.name
        binding.tvAge.text = child.age?.let { "$it ans" } ?: "Âge non renseigné"

        // ── En ligne / hors ligne ────────────────────────────────────
        val online = child.protection_active
        binding.tvOnlineStatus.text = if (online) "En ligne" else "Hors ligne"
        binding.statusDot.setBackgroundResource(
            if (online) R.drawable.bg_active_badge else R.drawable.bg_status_dot_inactive
        )

        // ── Niveau de protection (état réel des briques) ─────────────
        renderProtection(child)

        // ── Activité ─────────────────────────────────────────────────
        binding.tvDetectionCount.text = child.detections_count.toString()
        binding.tvLastActivity.text = formatRelative(child.last_detection ?: child.last_seen_at)

        // ── Appareil ─────────────────────────────────────────────────
        binding.tvDevice.text = child.device_model ?: "Appareil non identifié"
        binding.tvPairedAt.text = child.paired_at?.let { formatDate(it) } ?: "Non lié"

        // ── Avertissements ───────────────────────────────────────────
        renderWarnings(child)

        // ── Réglages par enfant (âge, intensité, mots perso) ─────────
        renderChildSettings(child)

        // ── Code d'appairage ─────────────────────────────────────────
        renderPairing(child)

        // Déconnexion à distance : seulement si un appareil est effectivement lié.
        binding.btnDisconnect.visibility = if (child.is_active) View.VISIBLE else View.GONE
        binding.btnDisconnect.setOnClickListener { confirmDisconnect(child) }

        binding.btnDelete.setOnClickListener { confirmDelete(child) }
    }

    private fun confirmDisconnect(child: ChildResponse) {
        AlertDialog.Builder(this)
            .setTitle("Déconnecter ${child.name} ?")
            .setMessage(
                "La liaison avec l'appareil sera rompue et la surveillance " +
                    "s'arrêtera. L'historique des détections est conservé. Un nouveau " +
                    "code d'appairage sera généré pour relier un appareil plus tard."
            )
            .setPositiveButton("Déconnecter") { _, _ -> disconnect() }
            .setNegativeButton("Annuler", null)
            .show()
    }

    private fun disconnect() {
        binding.btnDisconnect.isEnabled = false
        lifecycleScope.launch {
            try {
                ParentApiClient.service.disconnectChild(childId)
                Toast.makeText(
                    this@ChildDetailActivity,
                    "Appareil déconnecté — un nouveau code d'appairage a été généré",
                    Toast.LENGTH_LONG
                ).show()
                loadChild()
            } catch (e: Exception) {
                binding.btnDisconnect.isEnabled = true
                Toast.makeText(
                    this@ChildDetailActivity,
                    "Échec de la déconnexion — vérifiez la connexion",
                    Toast.LENGTH_SHORT
                ).show()
            }
        }
    }

    private fun renderProtection(child: ChildResponse) {
        val (label, detail, colorRes) = when (child.protection_level) {
            "complete" -> Triple(
                "Complète",
                "La capture, le blocage et l'identification des applications fonctionnent.",
                R.color.accent_green
            )
            "partial" -> Triple(
                "Partielle",
                "Les contenus sont analysés et bloqués, mais l'application consultée " +
                    "ne peut pas être identifiée (accès aux données d'utilisation désactivé).",
                R.color.accent_yellow
            )
            "degraded" -> Triple(
                "Dégradée",
                "Une autorisation manque sur l'appareil : les contenus ne peuvent pas " +
                    "être bloqués. Ouvrez MinorShield sur le téléphone de l'enfant.",
                R.color.accent_orange
            )
            else -> Triple(
                "Inactive",
                "Aucun signal récent de l'appareil : l'application est fermée, " +
                    "le téléphone éteint, ou la surveillance est arrêtée.",
                R.color.accent_red
            )
        }

        binding.tvProtectionLevel.text = label
        binding.tvProtectionLevel.setTextColor(ContextCompat.getColor(this, colorRes))
        binding.tvProtectionDetail.text = detail

        // Le déblocage n'a de sens que si l'appareil est effectivement verrouillé
        binding.btnUnlock.visibility = if (child.is_locked) View.VISIBLE else View.GONE
        binding.btnUnlock.setOnClickListener { unlock() }
    }

    private fun renderPairing(child: ChildResponse) {
        // Une fois l'appareil lié, le backend efface le code : la carte disparaît.
        val code = child.pairing_code
        if (code.isNullOrBlank()) {
            binding.cardPairing.visibility = View.GONE
            return
        }

        binding.cardPairing.visibility = View.VISIBLE
        binding.tvPairingCode.text = code

        val expiry = child.pairing_expires_at?.let { parseIso(it) }
        val remainingMs = (expiry?.time ?: 0L) - System.currentTimeMillis()

        if (expiry == null || remainingMs <= 0) {
            binding.tvPairingExpiry.text = "Code expiré"
        } else {
            val h = remainingMs / 3_600_000
            val m = (remainingMs % 3_600_000) / 60_000
            binding.tvPairingExpiry.text =
                if (h > 0) "Valide encore ${h}h ${m}min" else "Valide encore ${m}min"
        }

        // Toujours proposer la régénération quand la carte de code est visible :
        // le parent peut ainsi générer un nouveau code à la demande (ex: après
        // avoir déconnecté l'appareil), pas seulement à l'expiration.
        binding.btnRegenerateCode.visibility = View.VISIBLE
        binding.btnRegenerateCode.setOnClickListener { regenerateCode() }
    }

    private fun regenerateCode() {
        binding.btnRegenerateCode.isEnabled = false
        lifecycleScope.launch {
            try {
                ParentApiClient.service.regenerateCode(childId)
                Toast.makeText(this@ChildDetailActivity, "Nouveau code généré", Toast.LENGTH_SHORT).show()
                loadChild()
            } catch (e: Exception) {
                binding.btnRegenerateCode.isEnabled = true
                Toast.makeText(this@ChildDetailActivity, "Échec — vérifiez la connexion", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun renderWarnings(child: ChildResponse) {
        // warning_limit == 0 → « illimité » : on n'affiche pas de quota.
        val unlimited = child.warning_limit <= 0
        binding.tvWarningsState.text = if (unlimited)
            "${child.warnings_used} avertissement(s) aujourd'hui — quota illimité (jamais de blocage)"
        else
            "${child.warnings_used} / ${child.warning_limit} avertissements utilisés aujourd'hui"
        binding.btnWarningLimit.text = if (unlimited) "Illimité" else child.warning_limit.toString()

        binding.btnWarningLimit.setOnClickListener { chooseWarningLimit(child) }
        binding.btnResetWarnings.setOnClickListener { resetWarnings() }
    }

    private fun chooseWarningLimit(child: ChildResponse) {
        val pad = (20 * resources.displayMetrics.density).toInt()
        val et = EditText(this).apply {
            inputType = InputType.TYPE_CLASS_NUMBER
            hint = "Nombre d'avertissements (ex : 3)"
            if (child.warning_limit > 0) {
                setText(child.warning_limit.toString())
                setSelection(text.length)
            }
            setPadding(pad, pad / 2, pad, pad / 2)
        }
        AlertDialog.Builder(this)
            .setTitle("Avertissements avant blocage")
            .setMessage(
                "Saisissez le nombre d'avertissements autorisés avant le blocage, " +
                    "ou choisissez « Illimité » pour ne jamais bloquer sur ce quota."
            )
            .setView(et)
            .setPositiveButton("Valider") { _, _ ->
                val n = et.text.toString().trim().toIntOrNull()
                if (n == null || n < 1)
                    Toast.makeText(this, "Entrez un nombre ≥ 1, ou choisissez Illimité", Toast.LENGTH_SHORT).show()
                else
                    applyWarningLimit(n)
            }
            .setNeutralButton("Illimité") { _, _ -> applyWarningLimit(0) }
            .setNegativeButton("Annuler", null)
            .show()
    }

    private fun applyWarningLimit(limit: Int) {
        lifecycleScope.launch {
            try {
                ParentApiClient.service.setWarningLimit(childId, WarningLimitRequest(limit))
                val msg = if (limit <= 0) "Avertissements réglés sur : Illimité" else "Limite réglée à $limit"
                Toast.makeText(this@ChildDetailActivity, msg, Toast.LENGTH_SHORT).show()
                loadChild()
            } catch (e: Exception) {
                Toast.makeText(this@ChildDetailActivity, "Échec — vérifiez la connexion", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun resetWarnings() {
        lifecycleScope.launch {
            try {
                ParentApiClient.service.resetWarnings(childId)
                Toast.makeText(this@ChildDetailActivity, "Compteur réinitialisé", Toast.LENGTH_SHORT).show()
                loadChild()
            } catch (e: Exception) {
                Toast.makeText(this@ChildDetailActivity, "Échec — vérifiez la connexion", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun unlock() {
        binding.btnUnlock.isEnabled = false
        lifecycleScope.launch {
            try {
                ParentApiClient.service.unlockChild(childId)
                Toast.makeText(
                    this@ChildDetailActivity,
                    "Appareil débloqué — la surveillance reprendra dans une minute",
                    Toast.LENGTH_LONG
                ).show()
                loadChild()
            } catch (e: Exception) {
                binding.btnUnlock.isEnabled = true
                Toast.makeText(
                    this@ChildDetailActivity,
                    "Échec du déblocage — vérifiez la connexion",
                    Toast.LENGTH_SHORT
                ).show()
            }
        }
    }

    // ── Réglages par enfant : âge, intensité, mots sensibles perso ──────

    private fun renderChildSettings(child: ChildResponse) {
        binding.tvAgeSetting.text = child.age?.let { "$it ans" } ?: "Non défini"
        binding.tvIntensitySetting.text = intensityLabel(child.block_intensity)
        val count = child.custom_keywords
            ?.split(Regex("[,\n]"))?.map { it.trim() }?.count { it.isNotEmpty() } ?: 0
        binding.tvKeywordsSetting.text = if (count > 0) "$count mot(s)" else "Aucun"

        binding.itemAge.setOnClickListener { editAge(child) }
        binding.itemIntensity.setOnClickListener { editIntensity(child) }
        binding.itemKeywords.setOnClickListener { editKeywords(child) }

        renderScreenTime()
        binding.itemScreenTime.setOnClickListener { editScreenTime() }
    }

    // ── Temps d'écran autorisé ──────────────────────────────────────────
    // Réglage indicatif : la valeur est mémorisée localement mais n'est pas
    // encore appliquée sur l'appareil de l'enfant (fonctionnalité à venir).
    private fun screenTimePrefs() =
        getSharedPreferences("child_screentime", MODE_PRIVATE)

    private fun renderScreenTime() {
        val hours = screenTimePrefs().getInt(childId, 0)
        binding.tvScreenTimeSetting.text = if (hours > 0) "${hours} h/jour" else "Non défini"
    }

    private fun editScreenTime() {
        val current = screenTimePrefs().getInt(childId, 0)
        val et = EditText(this).apply {
            inputType = InputType.TYPE_CLASS_NUMBER
            hint = "Heures par jour (ex : 3)"
            if (current > 0) { setText(current.toString()); setSelection(text.length) }
            val pad = (20 * resources.displayMetrics.density).toInt()
            setPadding(pad, pad / 2, pad, pad / 2)
        }
        AlertDialog.Builder(this)
            .setTitle("Temps d'écran autorisé")
            .setMessage(
                "Fixez la durée quotidienne d'utilisation du téléphone autorisée pour cet enfant.\n\n" +
                    "Note : ce réglage est enregistré mais son application sur l'appareil de " +
                    "l'enfant arrive dans une prochaine mise à jour."
            )
            .setView(et)
            .setPositiveButton("Enregistrer") { _, _ ->
                val h = et.text.toString().trim().toIntOrNull()
                if (h == null || h !in 1..24) {
                    Toast.makeText(this, "Entrez un nombre d'heures entre 1 et 24", Toast.LENGTH_SHORT).show()
                } else {
                    screenTimePrefs().edit().putInt(childId, h).apply()
                    renderScreenTime()
                    Toast.makeText(this, "Temps d'écran réglé à ${h} h/jour", Toast.LENGTH_SHORT).show()
                }
            }
            .setNeutralButton("Retirer") { _, _ ->
                screenTimePrefs().edit().remove(childId).apply()
                renderScreenTime()
            }
            .setNegativeButton("Annuler", null)
            .show()
    }

    private fun intensityLabel(code: String): String = when (code) {
        "moyen"      -> "Moyen"
        "tres_eleve" -> "Très élevé"
        else         -> "Élevé"
    }

    private fun editAge(child: ChildResponse) {
        val et = EditText(this).apply {
            inputType = InputType.TYPE_CLASS_NUMBER
            setText(child.age?.toString() ?: "")
            hint = "Âge en années"
        }
        AlertDialog.Builder(this)
            .setTitle("Âge de l'enfant")
            .setView(et)
            .setPositiveButton("Enregistrer") { _, _ ->
                val age = et.text.toString().trim().toIntOrNull()
                if (age != null && age in 1..25) saveChild(ChildUpdateRequest(age = age))
                else Toast.makeText(this, "Âge invalide (1 à 25)", Toast.LENGTH_SHORT).show()
            }
            .setNegativeButton("Annuler", null)
            .show()
    }

    private fun editIntensity(child: ChildResponse) {
        val codes  = arrayOf("moyen", "eleve", "tres_eleve")
        val labels = arrayOf(
            "Moyen — ado plus âgé (ne bloque que l'explicite)",
            "Élevé — recommandé",
            "Très élevé — jeune enfant (bloque au moindre doute)",
        )
        val current = codes.indexOf(child.block_intensity).let { if (it < 0) 1 else it }
        AlertDialog.Builder(this)
            .setTitle("Intensité de blocage")
            .setSingleChoiceItems(labels, current) { dialog, which ->
                dialog.dismiss()
                saveChild(ChildUpdateRequest(block_intensity = codes[which]))
            }
            .setNegativeButton("Annuler", null)
            .show()
    }

    private fun editKeywords(child: ChildResponse) {
        val pad = (16 * resources.displayMetrics.density).toInt()
        val et = EditText(this).apply {
            setText(child.custom_keywords ?: "")
            hint = "Un mot par ligne (ou séparés par des virgules)"
            minLines = 3
            gravity = Gravity.TOP or Gravity.START
            inputType = InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_FLAG_MULTI_LINE
            setPadding(pad, pad / 2, pad, pad / 2)
        }
        AlertDialog.Builder(this)
            .setTitle("Mots sensibles — ${child.name}")
            .setMessage("Ces mots seront considérés comme inappropriés UNIQUEMENT pour cet enfant.")
            .setView(et)
            .setPositiveButton("Enregistrer") { _, _ ->
                saveChild(ChildUpdateRequest(custom_keywords = et.text.toString()))
            }
            .setNegativeButton("Annuler", null)
            .show()
    }

    private fun saveChild(req: ChildUpdateRequest) {
        lifecycleScope.launch {
            try {
                ParentApiClient.service.updateChild(childId, req)
                Toast.makeText(this@ChildDetailActivity, "Réglage enregistré", Toast.LENGTH_SHORT).show()
                loadChild()
            } catch (e: Exception) {
                Toast.makeText(this@ChildDetailActivity, "Échec — vérifiez la connexion", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun confirmDelete(child: ChildResponse) {
        AlertDialog.Builder(this)
            .setTitle("Supprimer ${child.name} ?")
            .setMessage(
                "L'appareil sera dissocié et tout son historique de détections " +
                    "sera définitivement supprimé."
            )
            .setPositiveButton("Supprimer") { _, _ -> delete() }
            .setNegativeButton("Annuler", null)
            .show()
    }

    private fun delete() {
        lifecycleScope.launch {
            try {
                ParentApiClient.service.deleteChild(childId)
                if (prefs.selectedChildId == childId) prefs.selectedChildId = ""
                Toast.makeText(this@ChildDetailActivity, "Enfant supprimé", Toast.LENGTH_SHORT).show()
                finish()
            } catch (e: Exception) {
                Toast.makeText(
                    this@ChildDetailActivity,
                    "Échec de la suppression — vérifiez la connexion",
                    Toast.LENGTH_SHORT
                ).show()
            }
        }
    }

    // ── Formatage des dates ──────────────────────────────────────────

    /**
     * Le backend horodate en UTC (datetime.utcnow). Sans forcer le fuseau ici,
     * les dates seraient interprétées comme locales et « dernière activité »
     * afficherait un décalage permanent.
     */
    private fun parseIso(iso: String): Date? = runCatching {
        SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss", Locale.US).apply {
            timeZone = TimeZone.getTimeZone("UTC")
        }.parse(iso.substringBefore("."))
    }.getOrNull()

    private fun formatDate(iso: String): String {
        val date = parseIso(iso) ?: return "—"
        return SimpleDateFormat("dd MMMM yyyy", Locale.FRANCE).format(date)
    }

    /** "Il y a 5 min", "Il y a 2 h"... plus parlant qu'un horodatage brut. */
    private fun formatRelative(iso: String?): String {
        if (iso == null) return "Aucune"
        val date = parseIso(iso) ?: return "—"
        val minutes = (System.currentTimeMillis() - date.time) / 60_000

        return when {
            minutes < 1    -> "À l'instant"
            minutes < 60   -> "Il y a ${minutes} min"
            minutes < 1440 -> "Il y a ${minutes / 60} h"
            else           -> "Il y a ${minutes / 1440} j"
        }
    }

    override fun onSupportNavigateUp(): Boolean {
        onBackPressedDispatcher.onBackPressed()
        return true
    }
}
