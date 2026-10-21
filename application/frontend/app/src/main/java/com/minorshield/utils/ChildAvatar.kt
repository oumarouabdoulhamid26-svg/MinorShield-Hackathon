package com.minorshield.utils

import android.graphics.drawable.GradientDrawable
import kotlin.math.abs

/**
 * Avatar généré à partir du prénom : initiale + couleur stable.
 *
 * Aucune photo n'est stockée : la couleur est dérivée du nom, donc un même
 * enfant garde toujours la même, sans donnée personnelle supplémentaire.
 */
object ChildAvatar {

    /** Palette lisible sur fond clair, avec du blanc en surimpression. */
    private val COLORS = listOf(
        0xFF00897B.toInt(), // teal
        0xFF1D3461.toInt(), // navy
        0xFF6A4C93.toInt(), // violet
        0xFFC1666B.toInt(), // rouge doux
        0xFF2E7D32.toInt(), // vert
        0xFFE65100.toInt(), // orange
        0xFF00695C.toInt(), // teal foncé
        0xFF4527A0.toInt(), // indigo
    )

    fun initialOf(name: String): String =
        name.trim().firstOrNull()?.uppercase() ?: "?"

    /** Couleur déterministe : le même prénom donne toujours la même. */
    fun colorOf(name: String): Int {
        val key = name.trim().lowercase()
        if (key.isEmpty()) return COLORS.first()
        return COLORS[abs(key.hashCode()) % COLORS.size]
    }

    /** Cercle plein coloré, à poser en fond de l'initiale. */
    fun circleFor(name: String): GradientDrawable = GradientDrawable().apply {
        shape = GradientDrawable.OVAL
        setColor(colorOf(name))
    }
}
