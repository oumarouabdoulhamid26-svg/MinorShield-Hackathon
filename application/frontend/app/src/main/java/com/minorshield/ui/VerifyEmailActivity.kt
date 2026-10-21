package com.minorshield.ui

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.minorshield.databinding.ActivityVerifyEmailBinding
import com.minorshield.network.ParentApiClient
import com.minorshield.network.VerifyEmailRequest
import com.minorshield.utils.ParentPreferencesManager
import kotlinx.coroutines.launch
import retrofit2.HttpException

/**
 * Vérification de l'adresse e-mail : l'utilisateur saisit le code à 6 chiffres
 * reçu par e-mail. On y arrive après une inscription (ou une connexion) dont le
 * compte n'est pas encore vérifié.
 */
class VerifyEmailActivity : AppCompatActivity() {

    private lateinit var binding: ActivityVerifyEmailBinding
    private lateinit var prefs: ParentPreferencesManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityVerifyEmailBinding.inflate(layoutInflater)
        setContentView(binding.root)

        prefs = ParentPreferencesManager(this)
        binding.tvEmailInfo.text =
            "Un code à 6 chiffres a été envoyé à ${prefs.email}. Saisissez-le pour activer votre compte."

        binding.btnVerify.setOnClickListener { verify() }
        binding.tvResend.setOnClickListener { resend() }
    }

    private fun verify() {
        val code = binding.etCode.text?.toString()?.trim().orEmpty()
        if (code.length != 6) {
            showError("Saisissez le code à 6 chiffres.")
            return
        }
        setLoading(true)
        binding.tvError.visibility = View.GONE

        lifecycleScope.launch {
            try {
                ParentApiClient.service.verifyEmail(VerifyEmailRequest(code))
                startActivity(Intent(this@VerifyEmailActivity, MainActivity::class.java)
                    .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK))
                finish()
            } catch (e: HttpException) {
                setLoading(false)
                showError(
                    when (e.code()) {
                        403  -> "Code incorrect."
                        410  -> "Code expiré. Renvoyez un nouveau code."
                        400  -> "Aucun code en attente. Renvoyez un code."
                        else -> "Erreur serveur (${e.code()})."
                    }
                )
            } catch (e: Exception) {
                setLoading(false)
                showError("Serveur injoignable — vérifiez la connexion.")
            }
        }
    }

    private fun resend() {
        setLoading(true)
        lifecycleScope.launch {
            try {
                ParentApiClient.service.resendCode()
                setLoading(false)
                Toast.makeText(this@VerifyEmailActivity, "Nouveau code envoyé par e-mail", Toast.LENGTH_SHORT).show()
            } catch (e: Exception) {
                setLoading(false)
                Toast.makeText(this@VerifyEmailActivity, "Échec de l'envoi — réessayez", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun setLoading(loading: Boolean) {
        binding.progressBar.visibility = if (loading) View.VISIBLE else View.GONE
        binding.btnVerify.isEnabled = !loading
    }

    private fun showError(msg: String) {
        binding.tvError.visibility = View.VISIBLE
        binding.tvError.text = msg
    }
}
