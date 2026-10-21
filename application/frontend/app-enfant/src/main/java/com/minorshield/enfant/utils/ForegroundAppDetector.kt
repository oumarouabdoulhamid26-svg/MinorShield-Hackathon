package com.minorshield.enfant.utils

import android.app.AppOpsManager
import android.app.usage.UsageEvents
import android.app.usage.UsageStatsManager
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.os.Process
import android.provider.Settings

/**
 * Identifie l'application actuellement au premier plan sur l'appareil enfant.
 *
 * Le nom lisible ("WhatsApp") est résolu ICI, sur le téléphone de l'enfant :
 * l'app parent ne peut pas le faire, ces applications ne sont pas installées
 * sur son appareil — elle ne recevrait qu'un identifiant technique.
 */
class ForegroundAppDetector(private val context: Context) {

    data class ForegroundApp(val packageName: String, val appName: String)

    companion object {
        /** Fenêtre pour capter un changement d'app récent (élargie : rester
         *  longtemps dans une app ne génère aucun nouvel événement). */
        private const val LOOKBACK_MS = 60_000L
        /** Fenêtre du repli par statistiques d'usage (app ouverte depuis un moment). */
        private const val USAGE_FALLBACK_MS = 5 * 60_000L

        /**
         * Cette permission ne peut pas être demandée par une popup classique :
         * l'utilisateur doit l'activer à la main dans les réglages Android.
         */
        fun hasUsageAccess(context: Context): Boolean {
            val appOps = context.getSystemService(Context.APP_OPS_SERVICE) as AppOpsManager
            val mode = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                appOps.unsafeCheckOpNoThrow(
                    AppOpsManager.OPSTR_GET_USAGE_STATS,
                    Process.myUid(), context.packageName
                )
            } else {
                @Suppress("DEPRECATION")
                appOps.checkOpNoThrow(
                    AppOpsManager.OPSTR_GET_USAGE_STATS,
                    Process.myUid(), context.packageName
                )
            }
            return mode == AppOpsManager.MODE_ALLOWED
        }

        fun usageAccessSettingsIntent(): Intent =
            Intent(Settings.ACTION_USAGE_ACCESS_SETTINGS)
    }

    /**
     * Retourne l'app au premier plan, ou null si la permission manque ou si
     * aucun événement récent n'est disponible.
     */
    fun current(): ForegroundApp? {
        if (!hasUsageAccess(context)) return null

        val usm = context.getSystemService(Context.USAGE_STATS_SERVICE) as? UsageStatsManager
            ?: return null

        val now = System.currentTimeMillis()

        // 1) Dernier changement d'app dans la fenêtre élargie
        var pkg = lastForegroundFromEvents(usm, now)

        // 2) Repli : app avec l'usage le plus récent (couvre le cas où l'enfant
        //    reste dans la même app sans en changer — aucun événement généré).
        if (pkg == null) {
            pkg = mostRecentFromUsageStats(usm, now)
        }

        val result = pkg ?: return null

        // On ignore notre propre app : ce n'est pas un contenu à surveiller.
        if (result == context.packageName) return null

        return ForegroundApp(packageName = result, appName = resolveAppName(result))
    }

    private fun lastForegroundFromEvents(usm: UsageStatsManager, now: Long): String? {
        val events = usm.queryEvents(now - LOOKBACK_MS, now)
        val event  = UsageEvents.Event()
        var last: String? = null
        while (events.hasNextEvent()) {
            events.getNextEvent(event)
            if (event.eventType == UsageEvents.Event.MOVE_TO_FOREGROUND) {
                last = event.packageName
            }
        }
        return last
    }

    private fun mostRecentFromUsageStats(usm: UsageStatsManager, now: Long): String? {
        val stats = usm.queryUsageStats(
            UsageStatsManager.INTERVAL_BEST,
            now - USAGE_FALLBACK_MS,
            now,
        ) ?: return null

        return stats
            .filter { it.lastTimeUsed > 0 && it.packageName != context.packageName }
            .maxByOrNull { it.lastTimeUsed }
            ?.packageName
    }

    /**
     * Traduit un package en nom lisible. En cas d'échec, on ne renvoie JAMAIS
     * le package technique (com.xxx.yyy) : il ne doit jamais atteindre le
     * parent. On renvoie une chaîne vide, que l'app parent affichera comme
     * « Application inconnue ».
     */
    private fun resolveAppName(packageName: String): String {
        val pm = context.packageManager
        return try {
            val info = pm.getApplicationInfo(packageName, 0)
            val label = pm.getApplicationLabel(info).toString()
            // Certaines apps renvoient leur propre package comme label : on filtre.
            if (label.isBlank() || label == packageName) "" else label
        } catch (_: Exception) {
            ""
        }
    }
}
