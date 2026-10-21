package com.minorshield.ui.pairing

import android.os.Bundle
import android.view.View
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.minorshield.R
import com.minorshield.network.PairingRequest
import com.minorshield.network.ParentApiClient
import kotlinx.coroutines.launch

class PairingActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_pairing)

        val etName = findViewById<EditText>(R.id.etChildName)
        val btnGenerate = findViewById<Button>(R.id.btnGenerateCode)
        val tvCode = findViewById<TextView>(R.id.tvPairingCode)
        val tvExpiry = findViewById<TextView>(R.id.tvExpiry)
        val progress = findViewById<ProgressBar>(R.id.progressBar)
        val tvError = findViewById<TextView>(R.id.tvError)
        val btnDone = findViewById<Button>(R.id.btnDone)

        btnDone.setOnClickListener { finish() }

        val etAge = findViewById<EditText>(R.id.etChildAge)

        btnGenerate.setOnClickListener {
            val name = etName.text.toString().trim()
            if (name.isEmpty()) {
                etName.error = "Entrez le prénom de l'enfant"
                return@setOnClickListener
            }

            val ageText = etAge.text.toString().trim()
            val age     = ageText.toIntOrNull()
            if (ageText.isNotEmpty() && (age == null || age !in 1..17)) {
                etAge.error = "Âge entre 1 et 17 ans"
                return@setOnClickListener
            }
            progress.visibility = View.VISIBLE
            tvError.visibility = View.GONE
            btnGenerate.isEnabled = false

            lifecycleScope.launch {
                try {
                    val resp = ParentApiClient.service.generatePairing(PairingRequest(name, age))
                    tvCode.text = resp.pairing_code
                    tvExpiry.text = "Valide 24h — installez l'app Enfant et entrez ce code"
                    tvCode.visibility = View.VISIBLE
                    tvExpiry.visibility = View.VISIBLE
                    btnDone.visibility = View.VISIBLE
                    btnGenerate.visibility = View.GONE
                } catch (e: Exception) {
                    tvError.text = "Erreur : ${e.message}"
                    tvError.visibility = View.VISIBLE
                } finally {
                    progress.visibility = View.GONE
                    btnGenerate.isEnabled = true
                }
            }
        }
    }
}
