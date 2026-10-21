package com.minorshield.network

import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

object ParentApiClient {

    // ── URL du backend hébergé (Railway) ─────────────────────────────
    // Adresse fixe : plus de champ à saisir dans l'app. Pour changer de
    // serveur, modifier cette seule constante (et celle de l'app enfant),
    // puis recompiler. Doit se terminer par "/".
    private const val BASE_URL = "https://minorshield.nolate.cm/"

    @Volatile private var token   = ""
    @Volatile private var _service: ParentApiService? = null

    val service: ParentApiService
        get() = _service ?: buildService().also { _service = it }

    fun setToken(jwt: String) {
        if (jwt != token) {
            token    = jwt
            _service = null
        }
    }

    fun clearToken() {
        token    = ""
        _service = null
    }

    private fun buildService(): ParentApiService {
        val client = OkHttpClient.Builder()
            .connectTimeout(15, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .addInterceptor { chain ->
                val req = chain.request().newBuilder()
                    .apply { if (token.isNotBlank()) addHeader("Authorization", "Bearer $token") }
                    .build()
                chain.proceed(req)
            }
            .addInterceptor(HttpLoggingInterceptor().apply {
                level = HttpLoggingInterceptor.Level.BASIC
            })
            .build()

        return Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(client)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ParentApiService::class.java)
    }
}
