package com.minorshield.ui

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.minorshield.R
import com.minorshield.databinding.ActivityPinLoginBinding
import com.minorshield.network.ParentApiClient
import com.minorshield.network.VerifyPinRequest
import com.minorshield.utils.ParentPreferencesManager
import kotlinx.coroutines.launch
import retrofit2.HttpException

class PinLoginActivity : AppCompatActivity() {

    private lateinit var binding: ActivityPinLoginBinding
    private lateinit var prefs: ParentPreferencesManager
    private val pin = StringBuilder()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityPinLoginBinding.inflate(layoutInflater)
        setContentView(binding.root)

        prefs = ParentPreferencesManager(this)

        // Cet écran ne fait que déverrouiller une session existante. Sans token,
        // aucune vérification n'est possible : on renvoie vers la connexion
        // plutôt que d'enfermer l'utilisateur sur un écran sans issue.
        if (prefs.jwtToken.isBlank()) {
            goToLogin()
            return
        }

        ParentApiClient.setToken(prefs.jwtToken)

        setupKeypad()
        updateDots()

        // Échappatoire : PIN oublié → se reconnecter avec le mot de passe.
        binding.tvForgotPassword.setOnClickListener { goToLogin() }
    }

    private fun goToLogin() {
        startActivity(Intent(this, LoginActivity::class.java)
            .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK))
        finish()
    }

    private fun setupKeypad() {
        val keys = listOf(
            binding.key1, binding.key2, binding.key3,
            binding.key4, binding.key5, binding.key6,
            binding.key7, binding.key8, binding.key9,
            binding.key0
        )
        keys.forEachIndexed { i, btn ->
            val digit = if (i < 9) (i + 1).toString() else "0"
            btn.setOnClickListener { appendDigit(digit) }
        }
        binding.keyDelete.setOnClickListener { deleteDigit() }
    }

    private fun appendDigit(digit: String) {
        if (pin.length >= 6) return
        pin.append(digit)
        updateDots()
        if (pin.length == 6) verifyPin()
    }

    private fun deleteDigit() {
        if (pin.isNotEmpty()) {
            pin.deleteCharAt(pin.length - 1)
            updateDots()
        }
    }

    private fun updateDots() {
        val dots = listOf(
            binding.dot1, binding.dot2, binding.dot3,
            binding.dot4, binding.dot5, binding.dot6
        )
        dots.forEachIndexed { i, dot ->
            dot.setBackgroundResource(
                if (i < pin.length) R.drawable.dot_pin_filled else R.drawable.dot_pin_empty
            )
        }
    }

    private fun verifyPin() {
        val entered = pin.toString()
        setKeypadEnabled(false)
        binding.tvError.text = ""

        lifecycleScope.launch {
            try {
                // Le PIN est vérifié par le serveur (hashé en base) — il n'est
                // jamais stocké en clair sur l'appareil.
                val result = ParentApiClient.service.verifyPin(VerifyPinRequest(entered))
                when {
                    !result.pin_configured -> openMain()   // aucun PIN défini → accès libre
                    result.valid           -> openMain()
                    else                   -> showError("PIN incorrect. Réessayez.")
                }
            } catch (e: HttpException) {
                if (e.code() == 401) {
                    // Session expirée ou invalide → reconnexion, pas un blocage.
                    goToLogin()
                } else {
                    showError("Erreur serveur (${e.code()}). Réessayez.")
                }
            } catch (e: Exception) {
                showError("Vérification impossible — vérifiez la connexion au serveur.")
            }
        }
    }

    private fun openMain() {
        startActivity(Intent(this, MainActivity::class.java)
            .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK))
        finish()
    }

    private fun showError(message: String) {
        binding.tvError.text = message
        pin.clear()
        updateDots()
        setKeypadEnabled(true)
    }

    private fun setKeypadEnabled(enabled: Boolean) {
        listOf(
            binding.key1, binding.key2, binding.key3,
            binding.key4, binding.key5, binding.key6,
            binding.key7, binding.key8, binding.key9,
            binding.key0, binding.keyDelete
        ).forEach { it.isEnabled = enabled }
    }
}
