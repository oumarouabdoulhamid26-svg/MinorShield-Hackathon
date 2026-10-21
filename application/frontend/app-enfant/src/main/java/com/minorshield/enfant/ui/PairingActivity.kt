package com.minorshield.enfant.ui

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.minorshield.enfant.databinding.EnfantActivityPairingBinding
import com.minorshield.enfant.network.ChildApiClient
import com.minorshield.enfant.network.RegisterRequest
import com.minorshield.enfant.utils.ChildPreferencesManager
import kotlinx.coroutines.launch
import retrofit2.HttpException
import java.io.IOException

class PairingActivity : AppCompatActivity() {

    private lateinit var binding: EnfantActivityPairingBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = EnfantActivityPairingBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.btnPair.setOnClickListener {
            val code = binding.etPairingCode.text.toString().trim()
            if (code.length < 6) {
                binding.tilPairingCode.error = "Le code doit contenir 6 chiffres"
                return@setOnClickListener
            }
            binding.tilPairingCode.error = null

            doPairing(code)
        }
    }

    private fun doPairing(code: String) {
        binding.btnPair.isEnabled = false
        binding.progressPairing.visibility = View.VISIBLE

        lifecycleScope.launch {
            try {
                val resp = ChildApiClient.service.register(
                    RegisterRequest(
                        pairing_code = code,
                        device_model = "${android.os.Build.MANUFACTURER} ${android.os.Build.MODEL}",
                    )
                )

                val prefs = ChildPreferencesManager(this@PairingActivity)
                prefs.childId   = resp.child_id
                prefs.childName = resp.child_name
                prefs.parentId  = resp.parent_id

                startActivity(Intent(this@PairingActivity, MainActivity::class.java))
                finish()
            } catch (e: Exception) {
                val message = when (e) {
                    is HttpException -> "Erreur serveur (${e.code()}) : ${e.response()?.errorBody()?.string() ?: e.message()}"
                    is IOException -> "Serveur inaccessible : vérifie l'adresse et que le téléphone est sur le même réseau (${e.message})"
                    else -> "Erreur inattendue : ${e.message}"
                }
                Toast.makeText(this@PairingActivity, message, Toast.LENGTH_LONG).show()
            } finally {
                binding.btnPair.isEnabled = true
                binding.progressPairing.visibility = View.GONE
            }
        }
    }
}
