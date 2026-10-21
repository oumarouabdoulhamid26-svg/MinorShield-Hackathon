package com.minorshield.ui.adapters

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.minorshield.R
import com.minorshield.databinding.ItemDetectionBinding
import com.minorshield.network.DetectionItem
import java.text.SimpleDateFormat
import java.util.*

/**
 * @param showSensitiveContent n'activer QUE dans l'historique. Le contenu
 *   sensible (texte extrait par OCR) ne doit apparaître nulle part ailleurs :
 *   cet adaptateur est aussi utilisé par le tableau de bord, visible d'un
 *   simple coup d'œil sur l'écran d'accueil.
 */
class DetectionAdapter(
    private var items: List<DetectionItem>,
    private val showSensitiveContent: Boolean = false,
) : RecyclerView.Adapter<DetectionAdapter.VH>() {

    private companion object {
        const val COLLAPSED_LINES = 4
    }

    inner class VH(val binding: ItemDetectionBinding) : RecyclerView.ViewHolder(binding.root)

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int) =
        VH(ItemDetectionBinding.inflate(LayoutInflater.from(parent.context), parent, false))

    override fun getItemCount() = items.size

    override fun onBindViewHolder(holder: VH, position: Int) {
        val item = items[position]
        with(holder.binding) {
            tvDetectionLabel.text = item.displayLabel
            tvDetectionApp.text = item.displayApp

            val score = ((item.nsfw_score ?: item.image_score ?: item.text_score ?: 0f) * 100).toInt()
            progressScore.progress = score
            tvScore.text = "$score%"

            val ctx = root.context
            val color = when {
                score >= 80 -> ctx.getColor(R.color.status_blocked)
                score >= 50 -> ctx.getColor(R.color.status_elevated)
                else -> ctx.getColor(R.color.status_medium)
            }
            progressScore.progressTintList = android.content.res.ColorStateList.valueOf(color)
            tvScore.setTextColor(color)

            // Contenu sensible : historique uniquement, et seulement s'il y a
            // effectivement du texte extrait.
            // Le texte OCR brut contient souvent des retours à la ligne et des
            // espaces multiples : on le normalise pour un rendu propre.
            val sensitiveText = item.extracted_text
                ?.replace(Regex("\\s+"), " ")
                ?.trim()
                .orEmpty()

            if (showSensitiveContent && sensitiveText.isNotEmpty()) {
                sensitiveContainer.visibility = View.VISIBLE
                tvExtractedText.text = sensitiveText
                tvExtractedText.maxLines = COLLAPSED_LINES

                // "Voir plus" seulement si le texte dépasse réellement.
                tvExtractedText.post {
                    val truncated = tvExtractedText.layout?.let {
                        it.getEllipsisCount(it.lineCount - 1) > 0
                    } ?: false
                    tvExpandHint.visibility = if (truncated) View.VISIBLE else View.GONE
                }

                val toggle = View.OnClickListener {
                    val expanded = tvExtractedText.maxLines != COLLAPSED_LINES
                    tvExtractedText.maxLines = if (expanded) COLLAPSED_LINES else Int.MAX_VALUE
                    tvExpandHint.text = if (expanded) "Voir plus" else "Voir moins"
                }
                sensitiveContainer.setOnClickListener(toggle)
                tvExpandHint.setOnClickListener(toggle)
            } else {
                sensitiveContainer.visibility = View.GONE
            }

            tvDetectionTime.text = com.minorshield.utils.DateUtils.formatTime(item.timestamp)
        }
    }

    fun update(newItems: List<DetectionItem>) {
        items = newItems
        notifyDataSetChanged()
    }
}
