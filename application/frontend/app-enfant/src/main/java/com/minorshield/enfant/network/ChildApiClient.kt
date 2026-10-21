package com.minorshield.enfant.network

import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

object ChildApiClient {

    // Clé API partagée — doit correspondre à API_KEY dans Server/.env
    const val API_KEY = "CHANGE_ME"

    // ── URL du backend hébergé (Railway) ─────────────────────────────
    // Adresse fixe : plus de champ à saisir. Pour changer de serveur,
    // modifier cette seule constante (et celle de l'app parent), puis
    // recompiler. Doit se terminer par "/".
    private const val BASE_URL = "https://minorshield.nolate.cm/"

    @Volatile private var _service: ChildApiService? = null

    val service: ChildApiService
        get() = _service ?: buildService().also { _service = it }

    private fun buildService(): ChildApiService {
        val client = OkHttpClient.Builder()
            .connectTimeout(15, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .addInterceptor { chain ->
                val req = chain.request().newBuilder()
                    .addHeader("X-API-Key", API_KEY)
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
            .create(ChildApiService::class.java)
    }
}
