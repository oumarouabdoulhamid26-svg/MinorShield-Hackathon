package com.minorshield.utils

import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.TimeZone

/**
 * Le backend horodate en UTC (datetime.utcnow, format ISO sans fuseau).
 * Il faut donc parser en UTC puis formater en heure locale — sinon l'heure
 * affichée est décalée du décalage horaire de l'appareil.
 */
object DateUtils {

    private fun parseUtc(iso: String): Date? = runCatching {
        SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss", Locale.US).apply {
            timeZone = TimeZone.getTimeZone("UTC")
        }.parse(iso.substringBefore("."))   // ignore les fractions de seconde
    }.getOrNull()

    /** "14/07 15:32" en heure locale. */
    fun formatDateTime(iso: String?): String {
        if (iso == null) return ""
        val d = parseUtc(iso) ?: return iso
        return SimpleDateFormat("dd/MM HH:mm", Locale.getDefault()).format(d)
    }

    /** "15:32" en heure locale. */
    fun formatTime(iso: String?): String {
        if (iso == null) return ""
        val d = parseUtc(iso) ?: return iso
        return SimpleDateFormat("HH:mm", Locale.getDefault()).format(d)
    }
}
