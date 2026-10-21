package com.minorshield.utils

import android.content.Context
import android.content.SharedPreferences
import com.minorshield.network.ParentApiClient
import com.minorshield.network.SubscriptionPlan
import com.minorshield.network.SubscriptionStatus
import java.text.SimpleDateFormat
import java.util.Locale

/**
 * Cache local du statut d'abonnement, dont la source de vérité est le backend
 * (`GET /api/v1/payment/status`). On met ce cache à jour via [refreshFromBackend]
 * pour que l'UI (label Premium, carte de statut) reflète l'état réel du serveur.
 */
class SubscriptionManager(context: Context) {

    private val prefs: SharedPreferences =
        context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)

    companion object {
        private const val PREFS_NAME = "minorshield_subscription"

        private const val KEY_IS_PREMIUM = "isPremium"
        private const val KEY_PLAN       = "plan"
        private const val KEY_EXPIRES_AT = "expiresAt"
    }

    // ── Statut abonnement (lecture locale, rafraîchi depuis le backend) ────────

    val isPremium: Boolean
        get() {
            if (!prefs.getBoolean(KEY_IS_PREMIUM, false)) return false
            val expiresAt = prefs.getLong(KEY_EXPIRES_AT, 0L)
            if (expiresAt > 0L && System.currentTimeMillis() > expiresAt) {
                revokeLocally()
                return false
            }
            return true
        }

    val currentStatus: SubscriptionStatus
        get() {
            val plan = prefs.getString(KEY_PLAN, null)
                ?.let { runCatching { SubscriptionPlan.valueOf(it) }.getOrNull() }
            return SubscriptionStatus(
                isActive       = isPremium,
                plan           = plan,
                expiresAt      = prefs.getLong(KEY_EXPIRES_AT, 0L),
                transactionRef = "",
            )
        }

    // ── Synchronisation avec le backend ───────────────────────────────────────

    /**
     * Interroge le backend et met à jour le cache local.
     * Retourne true si l'abonnement est actif côté serveur.
     */
    suspend fun refreshFromBackend(): Boolean {
        return try {
            val status = ParentApiClient.service.getSubscriptionStatus()
            if (status.is_active) {
                val plan = status.plan
                    ?.let { runCatching { SubscriptionPlan.valueOf(it) }.getOrNull() }
                    ?: SubscriptionPlan.MONTHLY
                cacheActive(plan, parseIsoToMillis(status.expires_at))
                true
            } else {
                revokeLocally()
                false
            }
        } catch (e: Exception) {
            // Serveur injoignable → on garde le cache local existant
            isPremium
        }
    }

    // ── Cache local ───────────────────────────────────────────────────────────

    private fun cacheActive(plan: SubscriptionPlan, expiresAtMillis: Long) {
        prefs.edit()
            .putBoolean(KEY_IS_PREMIUM, true)
            .putString(KEY_PLAN, plan.name)
            .putLong(KEY_EXPIRES_AT, expiresAtMillis)
            .apply()
    }

    private fun revokeLocally() {
        prefs.edit()
            .putBoolean(KEY_IS_PREMIUM, false)
            .remove(KEY_EXPIRES_AT)
            .apply()
    }

    private fun parseIsoToMillis(iso: String?): Long {
        if (iso.isNullOrBlank()) return 0L
        // Le backend renvoie un ISO sans fuseau, ex: 2026-08-15T12:00:00(.123456)
        val clean = iso.substringBefore(".").removeSuffix("Z")
        return runCatching {
            SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss", Locale.US)
                .parse(clean)?.time ?: 0L
        }.getOrDefault(0L)
    }
}
