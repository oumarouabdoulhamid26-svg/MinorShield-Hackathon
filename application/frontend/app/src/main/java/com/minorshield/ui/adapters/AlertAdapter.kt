package com.minorshield.ui.adapters

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.minorshield.databinding.ItemAlertBinding
import com.minorshield.network.DetectionItem

class AlertAdapter(
    private val items: MutableList<DetectionItem>,
    // Le bouton "Débloquer à distance" n'a de sens que si l'enfant est
    // ACTUELLEMENT bloqué (avertissements épuisés) : sinon il n'y a rien à
    // débloquer, on masque le bouton.
    private val showUnlock: Boolean = false,
    private val onUnlock: (Int) -> Unit = {},
) : RecyclerView.Adapter<AlertAdapter.VH>() {

    inner class VH(val binding: ItemAlertBinding) : RecyclerView.ViewHolder(binding.root)

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int) =
        VH(ItemAlertBinding.inflate(LayoutInflater.from(parent.context), parent, false))

    override fun getItemCount() = items.size

    override fun onBindViewHolder(holder: VH, position: Int) {
        val item = items[position]
        with(holder.binding) {
            tvAlertTitle.text = item.displayLabel
            tvAlertChild.text = item.displayApp
            val score = ((item.nsfw_score ?: 0f) * 100).toInt()
            tvAlertScore.text = "$score%"
            tvAlertTime.text = com.minorshield.utils.DateUtils.formatDateTime(item.timestamp)

            btnUnlockAlert.visibility = if (showUnlock) View.VISIBLE else View.GONE
            btnUnlockAlert.setOnClickListener {
                val pos = holder.adapterPosition
                if (pos != RecyclerView.NO_POSITION) onUnlock(pos)
            }
        }
    }

    /** Retire l'alerte débloquée de la liste (elle "disparaît"). */
    fun removeAt(position: Int) {
        if (position in items.indices) {
            items.removeAt(position)
            notifyItemRemoved(position)
        }
    }
}
