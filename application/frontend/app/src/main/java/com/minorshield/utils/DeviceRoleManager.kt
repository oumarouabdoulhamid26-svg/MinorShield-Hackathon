package com.minorshield.utils

import android.content.Context

/**
 * Rôle de l'appareil : parent (supervision) ou enfant (protégé).
 *
 * Le choix est fait UNE SEULE FOIS, au tout premier démarrage qui suit
 * l'installation, et il est DÉFINITIF : il n'existe volontairement aucun
 * moyen d'en changer depuis l'application. Un enfant ne doit pas pouvoir
 * repasser l'appareil en mode parent pour désactiver la protection.
 *
 * Seule une désinstallation/réinstallation efface ce choix (les
 * SharedPreferences sont supprimées avec l'application).
 *
 * Ce rôle vit dans son propre fichier de préférences : effacer la session
 * du parent (déconnexion) ne doit jamais réinitialiser le rôle.
 */
enum class DeviceRole { PARENT, ENFANT }

class DeviceRoleManager(context: Context) {

    private val prefs = context.applicationContext
        .getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)

    companion object {
        private const val PREFS_NAME = "minorshield_device_role"
        private const val KEY_ROLE   = "device_role"
    }

    /** Rôle choisi, ou null tant que l'utilisateur n'a pas choisi. */
    val role: DeviceRole?
        get() = when (prefs.getString(KEY_ROLE, null)) {
            "PARENT" -> DeviceRole.PARENT
            "ENFANT" -> DeviceRole.ENFANT
            else     -> null
        }

    val isChosen: Boolean get() = role != null

    /**
     * Fixe le rôle de l'appareil. Sans effet si un rôle a déjà été choisi :
     * le premier choix fait foi, définitivement.
     *
     * @return true si le rôle vient d'être enregistré, false s'il l'était déjà.
     */
    fun chooseOnce(newRole: DeviceRole): Boolean {
        if (isChosen) return false
        prefs.edit().putString(KEY_ROLE, newRole.name).commit()
        return true
    }
}
