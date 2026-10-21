package com.minorshield.ui

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import androidx.appcompat.app.AppCompatActivity
import com.minorshield.R
import com.minorshield.network.ParentApiClient
import com.minorshield.utils.DeviceRole
import com.minorshield.utils.DeviceRoleManager
import com.minorshield.utils.ParentPreferencesManager

/**
 * Point d'entrée unique de l'application (parent ET enfant).
 *
 * Aiguille selon le rôle choisi à l'installation :
 *  - aucun rôle  → écran de choix (une seule fois dans la vie de l'app) ;
 *  - ENFANT      → parcours enfant (appairage / protection) ;
 *  - PARENT      → parcours parent habituel.
 */
@SuppressLint("CustomSplashScreen")
class SplashActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_splash)

        val roles = DeviceRoleManager(this)
        val prefs = ParentPreferencesManager(this)

        // Le token n'a de sens que côté parent.
        if (roles.role == DeviceRole.PARENT && prefs.jwtToken.isNotBlank()) {
            ParentApiClient.setToken(prefs.jwtToken)
        }

        Handler(Looper.getMainLooper()).postDelayed({
            val next = when (roles.role) {
                null -> Intent(this, RoleChoiceActivity::class.java)

                DeviceRole.ENFANT ->
                    Intent(this, com.minorshield.enfant.ui.SplashActivity::class.java)

                DeviceRole.PARENT -> when {
                    !prefs.isOnboardingDone -> Intent(this, OnboardingActivity::class.java)
                    // Pas de session : si un compte a déjà servi sur cet appareil on
                    // propose la connexion, sinon l'inscription.
                    !prefs.isLoggedIn       ->
                        if (prefs.email.isNotBlank()) Intent(this, LoginActivity::class.java)
                        else Intent(this, RegisterActivity::class.java)
                    else                    -> Intent(this, PinLoginActivity::class.java)
                }
            }
            startActivity(next)
            finish()
        }, 2000L)
    }
}
