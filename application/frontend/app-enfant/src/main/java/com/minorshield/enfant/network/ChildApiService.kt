package com.minorshield.enfant.network

import okhttp3.MultipartBody
import okhttp3.RequestBody
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.Multipart
import retrofit2.http.POST
import retrofit2.http.Part
import retrofit2.http.Path

interface ChildApiService {

    @POST("api/v1/children/register")
    suspend fun register(@Body req: RegisterRequest): RegisterResponse

    @POST("api/v1/children/{childId}/lock")
    suspend fun lockChild(@Path("childId") childId: String)

    @POST("api/v1/children/{childId}/incident")
    suspend fun reportIncident(@Path("childId") childId: String): IncidentResponse

    @POST("api/v1/children/{childId}/unpair")
    suspend fun unpairDevice(@Path("childId") childId: String)

    @POST("api/v1/children/{childId}/verify-pin")
    suspend fun verifyPin(@Path("childId") childId: String, @Body req: VerifyPinRequest): VerifyPinResponse

    @GET("api/v1/children/{childId}/lock-status")
    suspend fun getLockStatus(@Path("childId") childId: String): LockStatusResponse

    @POST("api/v1/children/{childId}/heartbeat")
    suspend fun sendHeartbeat(@Path("childId") childId: String, @Body req: HeartbeatRequest)

    @Multipart
    @POST("api/v1/detect")
    suspend fun detect(
        @Part image     : MultipartBody.Part,
        @Part("child_id")    childId    : RequestBody,
        @Part("app_package") appPackage : RequestBody,
        @Part("app_name")    appName    : RequestBody,
    ): DetectionResponse
}
