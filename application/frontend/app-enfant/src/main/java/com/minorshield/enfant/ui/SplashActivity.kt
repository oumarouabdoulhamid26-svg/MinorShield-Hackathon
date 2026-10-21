package com.minorshield.enfant.ui

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.minorshield.enfant.network.ChildApiClient
import com.minorshield.enfant.utils.ChildPreferencesManager
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

class SplashActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(com.minorshield.enfant.R.layout.enfant_activity_splash)

        val prefs = ChildPreferencesManager(this)

        lifecycleScope.launch {
            delay(1500)
            val next = if (prefs.isPaired) MainActivity::class.java else PairingActivity::class.java
            startActivity(Intent(this@SplashActivity, next))
            finish()
        }
    }
}
