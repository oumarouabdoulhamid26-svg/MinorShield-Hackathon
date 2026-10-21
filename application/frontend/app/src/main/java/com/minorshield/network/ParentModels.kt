package com.minorshield.network

// ── Auth ─────────────────────────────────────────────────────────────

data class RegisterRequest(
    val email    : String,
    val password : String,
    val name     : String? = null,
    val phone    : String? = null,
    val fcm_token: String? = null
)

data class UpdateProfileRequest(
    val name : String?,
    val email: String,
)

data class LoginRequest(
    val email   : String,
    val password: String
)

data class SetPinRequest(
    val pin: String,
    // Requis par le serveur dès qu'un PIN existe déjà
    val current_pin: String? = null,
)

data class UpdateFcmTokenRequest(val fcm_token: String)

data class NotificationPrefs(
    val on_detection : Boolean = true,
    val daily_summary: Boolean = true,
)

data class VerifyPinRequest(val pin: String)

data class VerifyPinResponse(
    val valid         : Boolean,
    val pin_configured: Boolean,
)

data class TokenResponse(
    val access_token  : String,
    val token_type    : String,
    val parent_id     : String,
    val email         : String,
    val email_verified: Boolean = true,
)

data class VerifyEmailRequest(val code: String)

data class ParentProfile(
    val id        : String,
    val email     : String,
    val name      : String? = null,
    val phone     : String?,
    val created_at: String,
    val pin_configured: Boolean = false,
    val email_verified: Boolean = false,
)

// ── Enfants ───────────────────────────────────────────────────────────

data class PairingRequest(
    val name: String,
    val age : Int? = null,
)

data class PairingResponse(
    val child_id    : String,
    val child_name  : String,
    val pairing_code: String,
    val expires_in  : Int
)

data class ChildResponse(
    val id              : String,
    val name            : String,
    val age             : Int? = null,
    val is_active       : Boolean,
    val created_at      : String,
    val detections_count: Int,
    val last_detection  : String?,
    // Surveillance réellement opérationnelle sur l'appareil de l'enfant
    val protection_active: Boolean = false,
    val last_seen_at     : String? = null,
    val device_model     : String? = null,
    val paired_at        : String? = null,
    // complete | partial | degraded | inactive
    val protection_level : String = "inactive",
    val is_locked        : Boolean = false,
    val warning_limit    : Int = 3,
    val warnings_used    : Int = 0,
    val pairing_code     : String? = null,
    val pairing_expires_at: String? = null,
    // Réglages personnalisés par enfant
    val block_intensity  : String = "eleve",   // moyen | eleve | tres_eleve
    val custom_keywords  : String? = null,
)

data class WarningLimitRequest(val limit: Int)

data class ChildUpdateRequest(
    val age            : Int? = null,
    val block_intensity: String? = null,
    val custom_keywords: String? = null,
)

data class ChildListResponse(
    val children: List<ChildResponse>,
    val total   : Int
)

// ── Historique ────────────────────────────────────────────────────────

data class DetectionItem(
    val id            : Int,
    val request_id    : String,
    val nsfw_score    : Float,
    val image_score   : Float,
    val text_score    : Float,
    val label         : String,
    val category      : String? = null,
    val extracted_text: String?,
    val app_package   : String?,
    val app_name      : String? = null,
    val timestamp     : String
) {
    /**
     * Nom d'application à afficher. On ne montre JAMAIS le package technique
     * (ex: "com.whatsapp") : il est illisible pour un parent.
     */
    val displayApp: String
        get() = app_name?.takeIf { it.isNotBlank() } ?: "Application inconnue"

    /** Libellé lisible de la raison du blocage, affiché au parent. */
    val displayLabel: String
        get() = when {
            label != "nsfw"      -> "Contenu sain"
            category == "nudite"   -> "Nudité détectée"
            category == "violence" -> "Contenu violent détecté"
            category == "texte"    -> "Texte inapproprié détecté"
            else                   -> "Contenu inapproprié"
        }
}

data class DetectionHistoryResponse(
    val child_id  : String,
    val child_name: String,
    val detections: List<DetectionItem>,
    val total     : Int,
    val page      : Int,
    val page_size : Int
)

// ── Paiement / Abonnement ────────────────────────────────────────────

data class PaymentInitiateRequest(val plan: String)

data class PaymentInitiateResponse(
    val widget_url     : String,
    val transaction_ref: String,
    val amount         : Int,
    val currency       : String,
)

data class SubscriptionStatusResponse(
    val is_active    : Boolean,
    val plan         : String?,
    val expires_at   : String?,
    val days_remaining: Int,
)

enum class SubscriptionPlan(val label: String, val amountXAF: Int, val durationDays: Int) {
    MONTHLY("Mensuel",  1_000,  30),
    ANNUAL ("Annuel", 10_000, 365),
}

data class SubscriptionStatus(
    val isActive      : Boolean,
    val plan          : SubscriptionPlan?,
    val expiresAt     : Long,
    val transactionRef: String,
) {
    val daysRemaining: Int
        get() = maxOf(0, ((expiresAt - System.currentTimeMillis()) / 86_400_000L).toInt())
}

// ── Statistiques ──────────────────────────────────────────────────────

data class AppStat(
    val app_package: String,
    val app_name   : String = "Application inconnue",
    val count      : Int,
    val percentage : Float
)

data class DayStat(
    val date : String,
    val count: Int
)

data class ChildStatsResponse(
    val child_id    : String,
    val child_name  : String,
    val period      : String,
    val total       : Int,
    val blocked     : Int,
    val ignored     : Int,
    val efficacy_pct: Float,
    val by_app      : List<AppStat>,
    val by_day      : List<DayStat>
)
