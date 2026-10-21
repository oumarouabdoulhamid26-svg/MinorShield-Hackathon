package com.minorshield.notification

import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage
import com.minorshield.utils.ParentPreferencesManager

class MinorShieldMessagingService : FirebaseMessagingService() {

    override fun onNewToken(token: String) {
        super.onNewToken(token)
        ParentPreferencesManager(this).fcmToken = token
    }

    override fun onMessageReceived(remoteMessage: RemoteMessage) {
        super.onMessageReceived(remoteMessage)

        // Le backend envoie titre/corps dans le payload "notification".
        val title = remoteMessage.notification?.title ?: return
        val body  = remoteMessage.notification?.body ?: ""
        ParentNotifier(this).notifyAlert(title, body)
    }
}
