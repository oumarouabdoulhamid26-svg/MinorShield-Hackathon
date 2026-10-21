package com.minorshield.enfant.utils

import android.content.Context

class ChildPreferencesManager(context: Context) {

    private val prefs = context.getSharedPreferences("child_prefs", Context.MODE_PRIVATE)

    var childId: String?
        get() = prefs.getString("child_id", null)
        set(v) = prefs.edit().putString("child_id", v).apply()

    var childName: String?
        get() = prefs.getString("child_name", null)
        set(v) = prefs.edit().putString("child_name", v).apply()

    var parentId: String?
        get() = prefs.getString("parent_id", null)
        set(v) = prefs.edit().putString("parent_id", v).apply()

    var serverUrl: String?
        get() = prefs.getString("server_url", null)
        set(v) = prefs.edit().putString("server_url", v).apply()

    var isLocked: Boolean
        get() = prefs.getBoolean("is_locked", false)
        set(v) = prefs.edit().putBoolean("is_locked", v).apply()

    /** True tant que la boucle de capture d'écran tourne réellement. */
    var isCaptureRunning: Boolean
        get() = prefs.getBoolean("capture_running", false)
        set(v) = prefs.edit().putBoolean("capture_running", v).apply()

    /** True tant qu'un écran d'avertissement (dismissible) est affiché :
     *  met la capture en pause pour ne pas re-décompter le même contenu. */
    var warningActive: Boolean
        get() = prefs.getBoolean("warning_active", false)
        set(v) = prefs.edit().putBoolean("warning_active", v).apply()

    /**
     * Instant (epoch ms) jusqu'auquel aucune analyse ne doit re-verrouiller
     * l'appareil, après un déblocage par le parent. Sans ce délai, le contenu
     * encore affiché serait re-détecté et l'appareil re-verrouillé aussitôt.
     */
    var graceUntil: Long
        get() = prefs.getLong("grace_until", 0L)
        set(v) = prefs.edit().putLong("grace_until", v).apply()

    val isPaired: Boolean get() = childId != null

    fun clear() = prefs.edit().clear().apply()

    /**
     * Efface l'appairage et l'état de surveillance, mais CONSERVE l'URL du
     * serveur : sans elle, l'écran de liaison repartirait sur une adresse par
     * défaut et l'enfant ne pourrait pas se ré-appairer sans la ressaisir.
     */
    fun clearPairingKeepingServer() {
        prefs.edit()
            .remove("child_id")
            .remove("child_name")
            .remove("parent_id")
            .remove("is_locked")
            .remove("capture_running")
            .remove("grace_until")
            .apply()
    }
}
