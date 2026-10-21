package com.minorshield

import android.app.Application
import com.minorshield.network.ParentApiClient
import com.minorshield.utils.LocaleManager
import com.minorshield.utils.ParentPreferencesManager

class MinorShieldApp : Application() {

    override fun onCreate() {
        super.onCreate()

        // Langue choisie par l'utilisateur (français / anglais / système).
        // À restaurer avant toute activité, sinon le premier écran s'affiche
        // dans la langue du téléphone puis change brutalement.
        LocaleManager.restore(this)

        // Restaure l'URL du serveur et le token JWT AVANT toute activité.
        // Android (surtout MIUI/Xiaomi) peut tuer le process puis recréer
        // directement MainActivity au retour dans l'app, SANS repasser par
        // SplashActivity. Sans cette restauration ici, ParentApiClient
        // retombe sur son URL par défaut (10.0.2.2 = émulateur, injoignable
        // depuis un vrai téléphone) avec un token vide, et tous les appels
        // du parent échouent ("serveur injoignable", profil et listes vides).
        // onCreate() de l'Application, lui, s'exécute toujours en premier.
        val prefs = ParentPreferencesManager(this)
        if (prefs.jwtToken.isNotBlank()) {
            ParentApiClient.setToken(prefs.jwtToken)
        }

        // Le statut d'abonnement est rafraîchi depuis le backend dans les écrans
        // concernés (Réglages, Abonnement), une fois le token JWT disponible.
    }
}
