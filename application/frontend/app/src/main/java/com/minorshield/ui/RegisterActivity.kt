package com.minorshield.ui

import android.content.Intent
import android.os.Bundle
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.google.firebase.messaging.FirebaseMessaging
import com.minorshield.databinding.ActivityRegisterBinding
import com.minorshield.network.ParentApiClient
import com.minorshield.network.RegisterRequest
import com.minorshield.network.UpdateFcmTokenRequest
import com.minorshield.utils.ParentPreferencesManager
import kotlinx.coroutines.launch
import kotlinx.coroutines.tasks.await

class RegisterActivity : AppCompatActivity() {

    private lateinit var binding: ActivityRegisterBinding
    private lateinit var prefs: ParentPreferencesManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityRegisterBinding.inflate(layoutInflater)
        setContentView(binding.root)

        prefs = ParentPreferencesManager(this)

        binding.btnCreateAccount.setOnClickListener { register() }
        binding.tvAlreadyAccount.setOnClickListener {
            // Un utilisateur déjà inscrit doit se connecter (email + mot de passe)
            // pour obtenir un token : l'écran PIN ne fait que déverrouiller une
            // session existante et ne peut pas authentifier.
            startActivity(Intent(this, LoginActivity::class.java))
            finish()
        }
    }

    private fun register() {
        val name     = binding.etName.text.toString().trim()
        val email    = binding.etEmail.text.toString().trim()
        val password = binding.etPassword.text.toString()
        val confirm  = binding.etConfirmPassword.text.toString()

        if (!validate(name, email, password, confirm)) return

        setLoading(true)
        lifecycleScope.launch {
            try {
                val response = ParentApiClient.service.register(
                    RegisterRequest(email = email, password = password, name = name)
                )
                prefs.saveSession(response.access_token, response.parent_id, response.email)
                prefs.name = name
                ParentApiClient.setToken(response.access_token)
                registerFcmToken()

                // Vérification e-mail retirée : on accède directement à l'app.
                startActivity(Intent(this@RegisterActivity, MainActivity::class.java)
                    .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK))
                finish()
            } catch (e: Exception) {
                setLoading(false)
                showError(e.message ?: "Erreur lors de la création du compte")
            }
        }
    }

    /**
     * Remonte le token FCM au backend pour permettre les alertes push.
     * Sans blocage : un échec ici ne doit pas empêcher la création du compte.
     */
    private suspend fun registerFcmToken() {
        try {
            val token = FirebaseMessaging.getInstance().token.await()
            prefs.fcmToken = token
            ParentApiClient.service.updateFcmToken(UpdateFcmTokenRequest(token))
        } catch (_: Exception) {
            // Firebase indisponible ou serveur injoignable — les alertes push
            // seront simplement inactives, le reste de l'app fonctionne.
        }
    }

    private fun validate(name: String, email: String, password: String, confirm: String): Boolean {
        var ok = true
        if (name.isBlank()) { binding.tilName.error = "Requis"; ok = false } else binding.tilName.error = null
        if (email.isBlank() || !android.util.Patterns.EMAIL_ADDRESS.matcher(email).matches()) {
            binding.tilEmail.error = "Email invalide"; ok = false
        } else binding.tilEmail.error = null
        if (password.length < 6) { binding.tilPassword.error = "Minimum 6 caractères"; ok = false } else binding.tilPassword.error = null
        if (password != confirm) { binding.tilConfirmPassword.error = "Les mots de passe ne correspondent pas"; ok = false } else binding.tilConfirmPassword.error = null
        return ok
    }

    private fun setLoading(loading: Boolean) {
        binding.progressBar.visibility = if (loading) View.VISIBLE else View.GONE
        binding.btnCreateAccount.isEnabled = !loading
    }

    private fun showError(msg: String) {
        binding.tvError.visibility = View.VISIBLE
        binding.tvError.text = msg
    }
}
