package com.minorshield.utils

import android.content.Context
import android.content.SharedPreferences

class ParentPreferencesManager(context: Context) {

    private val prefs: SharedPreferences =
        context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)

    companion object {
        private const val PREFS_NAME       = "minorshield_parent"
        private const val KEY_TOKEN        = "jwt_token"
        private const val KEY_PARENT_ID    = "parent_id"
        private const val KEY_EMAIL        = "email"
        private const val KEY_NAME         = "name"
        private const val KEY_PHONE        = "phone"
        private const val KEY_SELECTED_CHILD = "selected_child_id"
        private const val KEY_SERVER_URL   = "server_url"
        private const val KEY_FCM_TOKEN    = "fcm_token"
        private const val KEY_ONBOARDING_DONE = "onboarding_done"

        // Modèle d'adresse LAN (à adapter par l'utilisateur au 1er lancement).
        // 10.0.2.2 = loopback de l'émulateur uniquement — inutile sur un vrai
        // téléphone, où il faut l'IP réelle de la machine qui héberge le backend.
        const val DEFAULT_SERVER_URL = "http://192.168.1.10:8081/"
    }

    var jwtToken: String
        get() = prefs.getString(KEY_TOKEN, "") ?: ""
        set(v) { prefs.edit().putString(KEY_TOKEN, v).apply() }

    var parentId: String
        get() = prefs.getString(KEY_PARENT_ID, "") ?: ""
        set(v) { prefs.edit().putString(KEY_PARENT_ID, v).apply() }

    var email: String
        get() = prefs.getString(KEY_EMAIL, "") ?: ""
        set(v) { prefs.edit().putString(KEY_EMAIL, v).apply() }

    var name: String
        get() = prefs.getString(KEY_NAME, "") ?: ""
        set(v) { prefs.edit().putString(KEY_NAME, v).apply() }

    var phone: String
        get() = prefs.getString(KEY_PHONE, "") ?: ""
        set(v) { prefs.edit().putString(KEY_PHONE, v).apply() }

    var selectedChildId: String
        get() = prefs.getString(KEY_SELECTED_CHILD, "") ?: ""
        set(v) { prefs.edit().putString(KEY_SELECTED_CHILD, v).apply() }

    var serverUrl: String
        get() = prefs.getString(KEY_SERVER_URL, DEFAULT_SERVER_URL) ?: DEFAULT_SERVER_URL
        set(v) { prefs.edit().putString(KEY_SERVER_URL, v).apply() }

    /** Token FCM de cet appareil — remonté au backend pour les notifications push. */
    var fcmToken: String
        get() = prefs.getString(KEY_FCM_TOKEN, "") ?: ""
        set(v) { prefs.edit().putString(KEY_FCM_TOKEN, v).apply() }

    var isOnboardingDone: Boolean
        get() = prefs.getBoolean(KEY_ONBOARDING_DONE, false)
        set(v) { prefs.edit().putBoolean(KEY_ONBOARDING_DONE, v).apply() }

    val isLoggedIn: Boolean get() = jwtToken.isNotBlank()

    fun saveSession(token: String, parentId: String, email: String) {
        prefs.edit()
            .putString(KEY_TOKEN, token)
            .putString(KEY_PARENT_ID, parentId)
            .putString(KEY_EMAIL, email)
            .apply()
    }

    fun logout() {
        prefs.edit()
            .remove(KEY_TOKEN)
            .remove(KEY_PARENT_ID)
            .remove(KEY_SELECTED_CHILD)
            .apply()
    }
}
