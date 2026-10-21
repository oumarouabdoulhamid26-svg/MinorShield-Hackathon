package com.minorshield.enfant.service

import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.PixelFormat
import android.hardware.display.DisplayManager
import android.hardware.display.VirtualDisplay
import android.media.ImageReader
import android.media.projection.MediaProjection
import android.media.projection.MediaProjectionManager
import android.os.Handler
import android.os.Looper
import android.util.DisplayMetrics

class ChildScreenCaptureManager(private val context: Context) {

    private var mediaProjection: MediaProjection? = null
    private var imageReader    : ImageReader?     = null
    private var virtualDisplay : VirtualDisplay?  = null

    private val metrics: DisplayMetrics by lazy { context.resources.displayMetrics }

    private val projectionCallback = object : MediaProjection.Callback() {
        override fun onStop() {
            release()
        }
    }

    fun initialize(resultCode: Int, data: Intent, onReady: () -> Unit) {
        val mgr = context.getSystemService(Context.MEDIA_PROJECTION_SERVICE) as MediaProjectionManager
        val handler = Handler(Looper.getMainLooper())
        mediaProjection = mgr.getMediaProjection(resultCode, data)
        // Obligatoire depuis Android 14 : le callback doit être enregistré
        // AVANT createVirtualDisplay(), sinon MediaProjection lève une IllegalStateException.
        mediaProjection?.registerCallback(projectionCallback, handler)

        val w = metrics.widthPixels
        val h = metrics.heightPixels
        val d = metrics.densityDpi

        // 3 buffers (au lieu de 2) : pendant une vidéo à 30-60 fps, le
        // producteur remplit les tampons plus vite qu'on ne les consomme.
        // Un buffer de plus réduit les blocages et les images figées.
        imageReader    = ImageReader.newInstance(w, h, PixelFormat.RGBA_8888, 3)
        virtualDisplay = mediaProjection?.createVirtualDisplay(
            "MSChildCapture", w, h, d,
            DisplayManager.VIRTUAL_DISPLAY_FLAG_AUTO_MIRROR,
            imageReader?.surface, null,
            handler
        )
        onReady()
    }

    fun captureScreen(): Bitmap? {
        val image = imageReader?.acquireLatestImage() ?: return null
        return try {
            val planes     = image.planes
            val buffer     = planes[0].buffer
            val pixelStride = planes[0].pixelStride
            val rowStride  = planes[0].rowStride
            val rowPadding = rowStride - pixelStride * metrics.widthPixels

            val bmp = Bitmap.createBitmap(
                metrics.widthPixels + rowPadding / pixelStride,
                metrics.heightPixels,
                Bitmap.Config.ARGB_8888
            )
            bmp.copyPixelsFromBuffer(buffer)
            if (rowPadding > 0)
                Bitmap.createBitmap(bmp, 0, 0, metrics.widthPixels, metrics.heightPixels)
                    .also { bmp.recycle() }
            else bmp
        } finally {
            image.close()
        }
    }

    fun release() {
        mediaProjection?.unregisterCallback(projectionCallback)
        virtualDisplay?.release()
        imageReader?.close()
        mediaProjection?.stop()
        virtualDisplay  = null
        imageReader     = null
        mediaProjection = null
    }
}
