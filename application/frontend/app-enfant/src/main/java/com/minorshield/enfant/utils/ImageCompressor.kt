package com.minorshield.enfant.utils

import android.graphics.Bitmap
import android.graphics.Matrix
import java.io.ByteArrayOutputStream

object ImageCompressor {

    // 1280px (au lieu de 640) : à 640, le texte d'un écran ~1080×2400 devenait
    // illisible pour l'OCR (texte extrait bruité/incomplet dans l'historique).
    // NudeNet n'est PAS affecté : le backend redimensionne lui-même l'image à
    // 640 pour l'analyse visuelle (image_service._resize_image). On envoie donc
    // une image nette pour l'OCR sans ralentir la détection d'images.
    private const val MAX_DIMENSION = 1280
    private const val JPEG_QUALITY  = 80

    fun compress(bitmap: Bitmap): ByteArray {
        val scaled = scaleBitmap(bitmap)
        val output = ByteArrayOutputStream()
        scaled.compress(Bitmap.CompressFormat.JPEG, JPEG_QUALITY, output)
        if (scaled != bitmap) scaled.recycle()
        return output.toByteArray()
    }

    private fun scaleBitmap(bitmap: Bitmap): Bitmap {
        val w = bitmap.width
        val h = bitmap.height
        if (w <= MAX_DIMENSION && h <= MAX_DIMENSION) return bitmap
        val scale  = MAX_DIMENSION.toFloat() / maxOf(w, h)
        val matrix = Matrix().apply { postScale(scale, scale) }
        return Bitmap.createBitmap(bitmap, 0, 0, w, h, matrix, true)
    }
}
