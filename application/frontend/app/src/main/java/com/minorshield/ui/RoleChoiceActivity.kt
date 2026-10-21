package com.minorshield.ui

import android.content.Intent
import android.os.Bundle
import androidx.activity.OnBackPressedCallback
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import com.minorshield.databinding.ActivityRoleChoiceBinding
import com.minorshield.utils.DeviceRole
import com.minorshield.utils.DeviceRoleManager

/**
 * Choix du rôle de l'appareil, au tout premier démarrage.
 *
 * Le choix est définitif (voir [DeviceRoleManager]) : on demande donc une
 * confirmation explicite avant de l'enregistrer, et on empêche de quitter
 * l'écran sans avoir choisi (retour arrière neutralisé).
 */
class RoleChoiceActivity : AppCompatActivity() {

    private lateinit var binding: ActivityRoleChoiceBinding
    private lateinit var roles: DeviceRoleManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityRoleChoiceBinding.inflate(layoutInflater)
        setContentView(binding.root)

        roles = DeviceRoleManager(this)

        // Sécurité : si un rôle existe déjà (retour arrière, relance…), on ne
        // repropose jamais le choix.
        roles.role?.let { route(it); return }

        binding.cardParent.setOnClickListener {
            confirm(
                DeviceRole.PARENT,
                "Configurer en mode parent ?",
                "Cet appareil servira à superviser vos enfants et à recevoir les alertes.",
            )
        }
        binding.cardEnfant.setOnClickListener {
            confirm(
                DeviceRole.ENFANT,
                "Configurer en mode enfant ?",
                "Cet appareil sera protégé et surveillé. Il devra être associé au compte du parent.",
            )
        }

        // Tant qu'aucun rôle n'est choisi, l'application ne peut pas démarrer :
        // le retour arrière ne doit pas permettre de contourner cet écran.
        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() { /* volontairement bloqué */ }
        })
    }

    private fun confirm(role: DeviceRole, title: String, message: String) {
        AlertDialog.Builder(this)
            .setTitle(title)
            .setMessage("$message\n\nCe choix est définitif : il ne pourra plus être modifié sans désinstaller l'application.")
            .setPositiveButton("Confirmer") { _, _ ->
                roles.chooseOnce(role)
                route(role)
            }
            .setNegativeButton("Annuler", null)
            .show()
    }

    private fun route(role: DeviceRole) {
        val next = when (role) {
            DeviceRole.PARENT -> Intent(this, OnboardingActivity::class.java)
            DeviceRole.ENFANT -> Intent(this, com.minorshield.enfant.ui.SplashActivity::class.java)
        }
        startActivity(next.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK))
        finish()
    }
}
