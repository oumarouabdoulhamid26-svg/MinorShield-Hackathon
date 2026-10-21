package com.minorshield.utils

import android.content.Context
import android.net.Uri
import android.widget.ImageView
import com.bumptech.glide.Glide
import com.bumptech.glide.load.engine.DiskCacheStrategy
import com.bumptech.glide.signature.ObjectKey
import java.io.File

/**
 * Stockage LOCAL des photos de profil (parent + enfants), sur l'appareil parent.
 *
 * Choix volontaire du local : le backend ne stocke pas d'images (confidentialité,
 * STORE_IMAGES=false) et le disque Railway est éphémère. Les photos servent à
 * personnaliser l'affichage côté parent — le local répond parfaitement à ce besoin.
 */
object PhotoStorage {

    fun parentFile(context: Context): File =
        File(context.filesDir, "parent_avatar.jpg")

    fun childFile(context: Context, childId: String): File =
        File(context.filesDir, "child_${childId}.jpg")

    /** Copie l'image choisie (URI du sélecteur système) vers [target]. */
    fun copyFrom(context: Context, uri: Uri, target: File): Boolean = try {
        context.contentResolver.openInputStream(uri)?.use { input ->
            target.outputStream().use { output -> input.copyTo(output) }
        }
        target.exists() && target.length() > 0
    } catch (e: Exception) {
        false
    }

    /**
     * Charge la photo dans un ImageView (recadrée en cercle) si elle existe.
     * Retourne true si une photo a été affichée, false sinon (à l'appelant
     * d'afficher son avatar par défaut dans ce cas).
     */
    fun loadInto(imageView: ImageView, file: File): Boolean {
        if (!file.exists() || file.length() == 0L) return false
        Glide.with(imageView)
            .load(file)
            // La signature (date de modif) force Glide à recharger après un
            // changement de photo, malgré le même chemin de fichier.
            .signature(ObjectKey(file.lastModified().toString()))
            .diskCacheStrategy(DiskCacheStrategy.NONE)
            .skipMemoryCache(true)
            .circleCrop()
            .into(imageView)
        return true
    }
}
