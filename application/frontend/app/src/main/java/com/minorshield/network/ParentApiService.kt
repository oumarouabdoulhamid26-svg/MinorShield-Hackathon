package com.minorshield.network

import retrofit2.http.*

interface ParentApiService {

    // ── Auth ─────────────────────────────────────────────────────────

    @POST("api/v1/auth/register")
    suspend fun register(@Body req: RegisterRequest): TokenResponse

    @POST("api/v1/auth/login")
    suspend fun login(@Body req: LoginRequest): TokenResponse

    @GET("api/v1/auth/me")
    suspend fun getProfile(): ParentProfile

    @PUT("api/v1/auth/me")
    suspend fun updateProfile(@Body req: UpdateProfileRequest): ParentProfile

    @POST("api/v1/auth/pin")
    suspend fun setPin(@Body req: SetPinRequest)

    @POST("api/v1/auth/verify-email")
    suspend fun verifyEmail(@Body req: VerifyEmailRequest)

    @POST("api/v1/auth/resend-code")
    suspend fun resendCode()

    @POST("api/v1/auth/verify-pin")
    suspend fun verifyPin(@Body req: VerifyPinRequest): VerifyPinResponse

    @POST("api/v1/auth/fcm-token")
    suspend fun updateFcmToken(@Body req: UpdateFcmTokenRequest)

    @GET("api/v1/auth/notifications")
    suspend fun getNotifPrefs(): NotificationPrefs

    @PUT("api/v1/auth/notifications")
    suspend fun updateNotifPrefs(@Body req: NotificationPrefs)

    // ── Enfants ───────────────────────────────────────────────────────

    @POST("api/v1/children/pair")
    suspend fun generatePairing(@Body req: PairingRequest): PairingResponse

    @GET("api/v1/children")
    suspend fun getChildren(): ChildListResponse

    @DELETE("api/v1/children/{childId}")
    suspend fun deleteChild(@Path("childId") childId: String)

    @PUT("api/v1/children/{childId}")
    suspend fun updateChild(@Path("childId") childId: String, @Body req: ChildUpdateRequest)

    @POST("api/v1/children/{childId}/unlock")
    suspend fun unlockChild(@Path("childId") childId: String)

    @POST("api/v1/children/{childId}/warning-limit")
    suspend fun setWarningLimit(@Path("childId") childId: String, @Body req: WarningLimitRequest)

    @POST("api/v1/children/{childId}/reset-warnings")
    suspend fun resetWarnings(@Path("childId") childId: String)

    @POST("api/v1/children/{childId}/regenerate-code")
    suspend fun regenerateCode(@Path("childId") childId: String): PairingResponse

    @POST("api/v1/children/{childId}/disconnect")
    suspend fun disconnectChild(@Path("childId") childId: String): PairingResponse

    // ── Historique ────────────────────────────────────────────────────

    @GET("api/v1/children/{childId}/detections")
    suspend fun getDetections(
        @Path("childId") childId : String,
        @Query("page")   page    : Int = 1,
        @Query("page_size") pageSize: Int = 50
    ): DetectionHistoryResponse

    // ── Statistiques ──────────────────────────────────────────────────

    @GET("api/v1/children/{childId}/stats")
    suspend fun getStats(
        @Path("childId") childId: String,
        @Query("period") period : String = "week"
    ): ChildStatsResponse

    // ── Paiement ──────────────────────────────────────────────────────

    @POST("api/v1/payment/initiate")
    suspend fun initiatePayment(@Body req: PaymentInitiateRequest): PaymentInitiateResponse

    @GET("api/v1/payment/status")
    suspend fun getSubscriptionStatus(): SubscriptionStatusResponse
}
