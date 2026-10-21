package com.minorshield.ui

import android.content.Intent
import android.os.Bundle
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.google.firebase.messaging.FirebaseMessaging
import com.minorshield.databinding.ActivityLoginBinding
import com.minorshield.network.LoginRequest
import com.minorshield.network.ParentApiClient
import com.minorshield.network.UpdateFcmTokenRequest
import com.minorshield.utils.ParentPreferencesManager
import kotlinx.coroutines.launch
import kotlinx.coroutines.tasks.await
import retrofit2.HttpException

/**
 * Connexion d'un parent déjà inscrit (email + mot de passe).
 *
 * À ne pas confondre avec [PinLoginActivity], qui ne fait que déverrouiller
 * une session déjà ouverte : sans passer ici, l'appareil n'a aucun token JWT
 * et toutes les requêtes au backend échouent.
 */
class LoginActivity : AppCompatActivity() {

    private lateinit var binding: ActivityLoginBinding
    private lateinit var prefs: ParentPreferencesManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityLoginBinding.inflate(layoutInflater)
        setContentView(binding.root)

        prefs = ParentPreferencesManager(this)

        // Pré-remplit le dernier email utilisé sur cet appareil
        binding.etEmail.setText(prefs.email)

        binding.btnLogin.setOnClickListener { login() }
        binding.tvNoAccount.setOnClickListener {
            startActivity(Intent(this, RegisterActivity::class.java))
            finish()
        }
    }

    private fun login() {
        val email    = binding.etEmail.text.toString().trim()
        val password = binding.etPassword.text.toString()

        if (!validate(email, password)) return

        setLoading(true)
        binding.tvError.visibility = View.GONE

        lifecycleScope.launch {
            try {
                val response = ParentApiClient.service.login(LoginRequest(email, password))
                prefs.saveSession(response.access_token, response.parent_id, response.email)
                ParentApiClient.setToken(response.access_token)
                registerFcmToken()

                // Vérification e-mail retirée : on accède directement à l'app.
                startActivity(Intent(this@LoginActivity, MainActivity::class.java)
                    .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK))
                finish()
            } catch (e: Exception) {
                setLoading(false)
                showError(
                    when {
                        e is HttpException && e.code() == 401 -> "Email ou mot de passe incorrect."
                        e is HttpException -> "Erreur serveur (${e.code()})."
                        else -> "Serveur injoignable — vérifiez l'adresse dans les réglages."
                    }
                )
            }
        }
    }

    private fun validate(email: String, password: String): Boolean {
        var ok = true
        if (email.isBlank() || !android.util.Patterns.EMAIL_ADDRESS.matcher(email).matches()) {
            binding.tilEmail.error = "Email invalide"; ok = false
        } else binding.tilEmail.error = null

        if (password.isBlank()) {
            binding.tilPassword.error = "Mot de passe requis"; ok = false
        } else binding.tilPassword.error = null

        return ok
    }

    /** Remonte le token FCM — sans bloquer la connexion en cas d'échec. */
    private suspend fun registerFcmToken() {
        try {
            val token = FirebaseMessaging.getInstance().token.await()
            prefs.fcmToken = token
            ParentApiClient.service.updateFcmToken(UpdateFcmTokenRequest(token))
        } catch (_: Exception) {
        }
    }

    private fun setLoading(loading: Boolean) {
        binding.progressBar.visibility = if (loading) View.VISIBLE else View.GONE
        binding.btnLogin.isEnabled = !loading
    }

    private fun showError(msg: String) {
        binding.tvError.visibility = View.VISIBLE
        binding.tvError.text = msg
    }
}
