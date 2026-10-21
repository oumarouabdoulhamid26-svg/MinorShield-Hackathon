package com.minorshield.ui.fragments

import android.app.AlertDialog
import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import com.google.android.material.textfield.TextInputEditText
import com.google.android.material.textfield.TextInputLayout
import com.minorshield.R
import com.minorshield.databinding.FragmentReglagesBinding
import com.minorshield.network.ParentApiClient
import com.minorshield.network.SetPinRequest
import com.minorshield.ui.LoginActivity
import com.minorshield.ui.SubscriptionActivity
import com.minorshield.utils.LocaleManager
import com.minorshield.utils.ParentPreferencesManager
import com.minorshield.utils.SubscriptionManager
import kotlinx.coroutines.launch
import retrofit2.HttpException

class ReglagesFragment : Fragment() {

    private var _binding: FragmentReglagesBinding? = null
    private val binding get() = _binding!!

    // Sélecteur d'image système (aucune permission requise avec GetContent).
    private val pickAvatar = registerForActivityResult(
        androidx.activity.result.contract.ActivityResultContracts.GetContent()
    ) { uri ->
        if (uri != null && _binding != null) {
            val ctx = requireContext()
            if (com.minorshield.utils.PhotoStorage.copyFrom(
                    ctx, uri, com.minorshield.utils.PhotoStorage.parentFile(ctx))) {
                showAvatar()
            }
        }
    }

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        _binding = FragmentReglagesBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        val prefs = ParentPreferencesManager(requireContext())

        bindProfile(prefs)
        showAvatar()
        binding.itemProfile.setOnClickListener { showEditProfileDialog(prefs) }
        binding.avatarProfile.setOnClickListener { pickAvatar.launch("image/*") }
        // Synchronise le profil depuis le backend (nom/email réels — utile après
        // une simple connexion, où le nom n'est pas encore en local).
        viewLifecycleOwner.lifecycleScope.launch {
            try {
                val p = ParentApiClient.service.getProfile()
                p.name?.let { prefs.name = it }
                prefs.email = p.email
                if (_binding != null) bindProfile(prefs)
            } catch (_: Exception) { }
        }

        val sub = SubscriptionManager(requireContext())
        binding.tvSubscriptionStatus.text = if (sub.isPremium) "Premium ✓" else "Gratuit"
        // Rafraîchit depuis le backend (source de vérité) puis met à jour le label
        viewLifecycleOwner.lifecycleScope.launch {
            sub.refreshFromBackend()
            if (_binding != null) {
                binding.tvSubscriptionStatus.text = if (sub.isPremium) "Premium ✓" else "Gratuit"
            }
        }

        binding.itemSubscription.setOnClickListener {
            startActivity(Intent(requireContext(), SubscriptionActivity::class.java))
        }

        binding.btnLogout.setOnClickListener {
            prefs.logout()
            ParentApiClient.clearToken()
            val intent = Intent(requireContext(), LoginActivity::class.java)
            intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
            startActivity(intent)
        }

        binding.itemChangePin.setOnClickListener {
            showSetPinDialog()
        }

        setupLanguagePicker()
        setupNotificationSwitches()
    }

    /**
     * Choix de la langue de l'interface (français / anglais / langue du
     * téléphone). Android recrée les écrans pour recharger les textes.
     */
    private fun setupLanguagePicker() {
        binding.tvLanguageValue.text = LocaleManager.currentLabel(requireContext())

        binding.itemLanguage.setOnClickListener {
            val codes  = LocaleManager.SUPPORTED.keys.toList()
            val labels = LocaleManager.SUPPORTED.values.toTypedArray()
            val current = codes.indexOf(LocaleManager.current(requireContext()))

            AlertDialog.Builder(requireContext())
                .setTitle(R.string.settings_language_title)
                .setSingleChoiceItems(labels, current) { dialog, which ->
                    dialog.dismiss()
                    LocaleManager.apply(requireContext(), codes[which])
                    // Recréation immédiate pour afficher la nouvelle langue.
                    activity?.recreate()
                }
                .setNegativeButton(android.R.string.cancel, null)
                .show()
        }
    }

    /**
     * Les deux interrupteurs pilotent de vraies préférences côté serveur
     * (le backend décide d'envoyer, ou non, les push). On charge l'état réel
     * puis on enregistre chaque changement.
     */
    private fun setupNotificationSwitches() {
        viewLifecycleOwner.lifecycleScope.launch {
            try {
                val prefs = ParentApiClient.service.getNotifPrefs()
                if (_binding != null) {
                    binding.switchNotifDetection.isChecked = prefs.on_detection
                    binding.switchNotifSummary.isChecked   = prefs.daily_summary
                }
            } catch (_: Exception) {
                // Serveur injoignable : on garde l'état affiché par défaut.
            }
        }

        // setOnClickListener (et non OnCheckedChange) : ne se déclenche que sur
        // action de l'utilisateur, pas lors du chargement initial ci-dessus.
        val save = View.OnClickListener { pushNotifPrefs() }
        binding.switchNotifDetection.setOnClickListener(save)
        binding.switchNotifSummary.setOnClickListener(save)
    }

    private fun pushNotifPrefs() {
        viewLifecycleOwner.lifecycleScope.launch {
            try {
                ParentApiClient.service.updateNotifPrefs(
                    com.minorshield.network.NotificationPrefs(
                        on_detection  = binding.switchNotifDetection.isChecked,
                        daily_summary = binding.switchNotifSummary.isChecked,
                    )
                )
            } catch (_: Exception) {
                if (isAdded) Toast.makeText(
                    requireContext(),
                    "Préférence non enregistrée — vérifiez la connexion",
                    Toast.LENGTH_SHORT
                ).show()
            }
        }
    }

    /** Affiche la photo de profil si elle existe, sinon l'initiale. */
    private fun showAvatar() {
        if (_binding == null) return
        val file = com.minorshield.utils.PhotoStorage.parentFile(requireContext())
        val hasPhoto = com.minorshield.utils.PhotoStorage.loadInto(binding.ivProfileAvatar, file)
        binding.ivProfileAvatar.visibility = if (hasPhoto) View.VISIBLE else View.GONE
        binding.tvAvatarLetter.visibility  = if (hasPhoto) View.GONE else View.VISIBLE
    }

    private fun bindProfile(prefs: ParentPreferencesManager) {
        val name = prefs.name.ifBlank {
            prefs.email.substringBefore("@").replace(".", " ").ifBlank { "Administrateur" }
        }
        binding.tvProfileName.text  = name
        binding.tvProfileEmail.text = prefs.email
        binding.tvAvatarLetter.text = name.firstOrNull()?.uppercase() ?: "A"
    }

    /** Dialogue de modification du nom et de l'email du parent. */
    private fun showEditProfileDialog(prefs: ParentPreferencesManager) {
        val ctx = requireContext()
        val pad = (16 * resources.displayMetrics.density).toInt()

        val etName = android.widget.EditText(ctx).apply {
            hint = "Nom"
            setText(prefs.name)
            inputType = android.text.InputType.TYPE_TEXT_FLAG_CAP_WORDS
        }
        val etEmail = android.widget.EditText(ctx).apply {
            hint = "Email"
            setText(prefs.email)
            inputType = android.text.InputType.TYPE_TEXT_VARIATION_EMAIL_ADDRESS
        }
        val container = android.widget.LinearLayout(ctx).apply {
            orientation = android.widget.LinearLayout.VERTICAL
            setPadding(pad, pad / 2, pad, 0)
            addView(etName)
            addView(etEmail)
        }

        val dialog = AlertDialog.Builder(ctx)
            .setTitle("Modifier le profil")
            .setView(container)
            .setPositiveButton("Enregistrer", null)
            .setNegativeButton("Annuler", null)
            .create()

        dialog.setOnShowListener {
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener {
                val newName  = etName.text?.toString()?.trim().orEmpty()
                val newEmail = etEmail.text?.toString()?.trim().orEmpty()
                if (newEmail.isEmpty() ||
                    !android.util.Patterns.EMAIL_ADDRESS.matcher(newEmail).matches()
                ) {
                    etEmail.error = "Email invalide"
                    return@setOnClickListener
                }
                viewLifecycleOwner.lifecycleScope.launch {
                    try {
                        val p = ParentApiClient.service.updateProfile(
                            com.minorshield.network.UpdateProfileRequest(
                                name  = newName.ifBlank { null },
                                email = newEmail,
                            )
                        )
                        prefs.name  = p.name ?: newName
                        prefs.email = p.email
                        if (_binding != null) bindProfile(prefs)
                        Toast.makeText(ctx, "Profil mis à jour", Toast.LENGTH_SHORT).show()
                        dialog.dismiss()
                    } catch (e: HttpException) {
                        when (e.code()) {
                            409  -> etEmail.error = "Email déjà utilisé"
                            else -> Toast.makeText(ctx, "Erreur serveur (${e.code()})", Toast.LENGTH_SHORT).show()
                        }
                    } catch (e: Exception) {
                        Toast.makeText(ctx, "Serveur injoignable", Toast.LENGTH_SHORT).show()
                    }
                }
            }
        }
        dialog.show()
    }

    private fun showSetPinDialog() {
        // On demande d'abord au serveur si un PIN existe : cela détermine s'il
        // faut exiger le PIN actuel (le serveur le vérifie de toute façon).
        viewLifecycleOwner.lifecycleScope.launch {
            val pinConfigured = try {
                ParentApiClient.service.getProfile().pin_configured
            } catch (e: Exception) {
                Toast.makeText(
                    requireContext(),
                    "Serveur injoignable — impossible de modifier le PIN",
                    Toast.LENGTH_SHORT
                ).show()
                return@launch
            }
            buildPinDialog(pinConfigured)
        }
    }

    private fun buildPinDialog(pinConfigured: Boolean) {
        val view = LayoutInflater.from(requireContext()).inflate(R.layout.dialog_set_pin, null)
        val tvIntro        = view.findViewById<android.widget.TextView>(R.id.tvPinIntro)
        val tilCurrentPin  = view.findViewById<TextInputLayout>(R.id.tilCurrentPin)
        val tilPin         = view.findViewById<TextInputLayout>(R.id.tilPin)
        val tilPinConfirm  = view.findViewById<TextInputLayout>(R.id.tilPinConfirm)
        val etCurrentPin   = view.findViewById<TextInputEditText>(R.id.etCurrentPin)
        val etPin          = view.findViewById<TextInputEditText>(R.id.etPin)
        val etPinConfirm   = view.findViewById<TextInputEditText>(R.id.etPinConfirm)

        tilCurrentPin.visibility = if (pinConfigured) View.VISIBLE else View.GONE
        tvIntro.text = if (pinConfigured) {
            "Ce PIN protège l'accès à l'application et la déconnexion de l'appareil de votre enfant."
        } else {
            "Aucun PIN n'est défini. Ce PIN protégera l'accès à l'application et la déconnexion " +
            "de l'appareil de votre enfant."
        }

        val dialog = AlertDialog.Builder(requireContext())
            .setTitle(if (pinConfigured) "Modifier le code PIN" else "Définir un code PIN")
            .setView(view)
            .setPositiveButton("Enregistrer", null)
            .setNegativeButton("Annuler", null)
            .create()

        dialog.setOnShowListener {
            val btn = dialog.getButton(AlertDialog.BUTTON_POSITIVE)
            btn.setOnClickListener {
                val current = etCurrentPin.text?.toString().orEmpty()
                val pin     = etPin.text?.toString().orEmpty()
                val confirm = etPinConfirm.text?.toString().orEmpty()

                tilCurrentPin.error = null
                tilPin.error        = null
                tilPinConfirm.error = null

                // ── Validation, champ par champ ──────────────────────────
                if (pinConfigured && current.isBlank()) {
                    tilCurrentPin.error = "Saisissez votre PIN actuel"
                    return@setOnClickListener
                }
                if (!pin.matches(Regex("^\\d{4,6}$"))) {
                    tilPin.error = "4 à 6 chiffres"
                    return@setOnClickListener
                }
                if (pinConfigured && pin == current) {
                    tilPin.error = "Le nouveau PIN doit être différent de l'actuel"
                    return@setOnClickListener
                }
                if (confirm != pin) {
                    tilPinConfirm.error = "Les codes ne correspondent pas"
                    return@setOnClickListener
                }

                btn.isEnabled = false
                viewLifecycleOwner.lifecycleScope.launch {
                    try {
                        ParentApiClient.service.setPin(
                            SetPinRequest(pin = pin, current_pin = current.ifBlank { null })
                        )
                        Toast.makeText(
                            requireContext(),
                            if (pinConfigured) "PIN modifié" else "PIN enregistré",
                            Toast.LENGTH_SHORT
                        ).show()
                        dialog.dismiss()
                    } catch (e: HttpException) {
                        btn.isEnabled = true
                        when (e.code()) {
                            403  -> tilCurrentPin.error = "PIN actuel incorrect"
                            400  -> tilCurrentPin.error = "PIN actuel requis"
                            else -> tilPin.error = "Erreur serveur (${e.code()})"
                        }
                    } catch (e: Exception) {
                        btn.isEnabled = true
                        tilPin.error = "Serveur injoignable"
                    }
                }
            }
        }

        dialog.show()
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
