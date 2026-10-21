package com.minorshield.utils

import android.content.Context
import androidx.appcompat.app.AppCompatDelegate
import androidx.core.os.LocaleListCompat

/**
 * Langue de l'interface : français, anglais, ou celle du téléphone.
 *
 * On s'appuie sur AppCompatDelegate (API « per-app language ») : Android
 * recrée les activités et recharge les ressources tout seul, et le choix
 * survit au redémarrage. Sur Android 13+, la langue apparaît aussi dans les
 * réglages système de l'application.
 */
object LocaleManager {

    private const val PREFS_NAME = "minorshield_locale"
    private const val KEY_LANG   = "app_language"

    /** Valeur stockée pour « suivre la langue du téléphone ». */
    const val SYSTEM = "system"

    /** Langues proposées : code -> libellé affiché (dans la langue elle-même). */
    val SUPPORTED = linkedMapOf(
        SYSTEM to "Système / System",
        "fr"   to "Français",
        "en"   to "English",
    )

    private fun prefs(context: Context) =
        context.applicationContext.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)

    /** Code de langue enregistré ([SYSTEM] par défaut). */
    fun current(context: Context): String =
        prefs(context).getString(KEY_LANG, SYSTEM) ?: SYSTEM

    fun currentLabel(context: Context): String =
        SUPPORTED[current(context)] ?: SUPPORTED.getValue(SYSTEM)

    /**
     * Applique une langue et la mémorise. Les activités visibles sont
     * recréées par le système pour recharger les textes.
     */
    fun apply(context: Context, code: String) {
        prefs(context).edit().putString(KEY_LANG, code).apply()
        AppCompatDelegate.setApplicationLocales(
            if (code == SYSTEM) LocaleListCompat.getEmptyLocaleList()
            else LocaleListCompat.forLanguageTags(code)
        )
    }

    /**
     * Restaure la langue choisie au démarrage du process.
     * À appeler depuis Application.onCreate().
     */
    fun restore(context: Context) {
        val code = current(context)
        if (code != SYSTEM) {
            AppCompatDelegate.setApplicationLocales(LocaleListCompat.forLanguageTags(code))
        }
    }
}
