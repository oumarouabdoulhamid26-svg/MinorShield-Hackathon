package com.minorshield.enfant.network

data class RegisterRequest(
    val pairing_code    : String,
    val device_fcm_token: String? = null,
    // Permet au parent d'identifier le téléphone lié dans la fiche enfant
    val device_model    : String? = null,
)

data class RegisterResponse(
    val child_id  : String,
    val child_name: String,
    val parent_id : String,
)

data class LockStatusResponse(
    val is_locked: Boolean,
    // Catégorie du contenu ayant déclenché le blocage : nudite | violence | texte
    val reason   : String? = null,
    val warning_limit: Int = 3,
    val warnings_used: Int = 0,
)

data class IncidentResponse(
    val status       : String,   // "warning" | "blocked"
    val warnings_used: Int,
    val warning_limit: Int,
    val remaining    : Int,
)

data class HeartbeatRequest(
    val protection_active: Boolean,
    // Détail par brique : permet au parent de savoir CE QUI manque
    val capture_active   : Boolean? = null,
    val overlay_allowed  : Boolean? = null,
    val usage_access     : Boolean? = null,
)

data class VerifyPinRequest(
    val pin: String,
)

data class VerifyPinResponse(
    val valid         : Boolean,
    val pin_configured: Boolean,
)

data class DetectionResponse(
    val request_id    : String,
    val nsfw_score    : Float,
    val label         : String,
    val category      : String? = null,
    val image_score   : Float,
    val text_score    : Float,
    val extracted_text: String?,
    val processing_ms : Int,
    val timestamp     : String,
)
