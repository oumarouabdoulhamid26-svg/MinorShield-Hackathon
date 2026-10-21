package com.minorshield.enfant.service

import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.os.Build
import androidx.core.app.NotificationCompat
import com.minorshield.enfant.utils.ChildPreferencesManager

class BootReceiver : BroadcastReceiver() {

    companion object {
        private const val CHANNEL_ID = "ms_monitoring"
        private const val NOTIF_ID   = 3
    }

    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action != Intent.ACTION_BOOT_COMPLETED) return

        val prefs   = ChildPreferencesManager(context)
        val childId = prefs.childId ?: return

        // L'overlay de blocage peut redémarrer seul : il n'a besoin d'aucune
        // autorisation runtime, juste du childId.
        val overlayIntent = Intent(context, OverlayService::class.java).apply {
            putExtra(OverlayService.EXTRA_CHILD_ID, childId)
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            context.startForegroundService(overlayIntent)
        } else {
            context.startService(overlayIntent)
        }

        // La capture d'écran, elle, ne peut PAS redémarrer sans un nouveau
        // consentement MediaProjection (contrainte Android). On ne démarre donc
        // pas ChildMonitoringService ici : un démarrage sans jeton polluerait sa
        // file d'intents et tuerait le démarrage légitime qui suit. On se
        // contente de prévenir l'utilisateur de rouvrir l'application.
        notifyReopenRequired(context)
    }

    private fun notifyReopenRequired(context: Context) {
        val nm = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            nm.createNotificationChannel(
                NotificationChannel(
                    CHANNEL_ID, "Surveillance MinorShield",
                    NotificationManager.IMPORTANCE_LOW
                )
            )
        }

        val notification = NotificationCompat.Builder(context, CHANNEL_ID)
            .setContentTitle("MinorShield — Surveillance à réactiver")
            .setContentText("Ouvrez MinorShield pour réautoriser la capture d'écran")
            .setSmallIcon(android.R.drawable.ic_dialog_alert)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setAutoCancel(true)
            .build()

        try {
            nm.notify(NOTIF_ID, notification)
        } catch (_: SecurityException) {
            // POST_NOTIFICATIONS refusée — rien à faire de plus ici
        }
    }
}
