package com.minorshield.ui.adapters

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.minorshield.R
import com.minorshield.databinding.ItemChildBinding
import com.minorshield.network.ChildResponse
import com.minorshield.utils.ChildAvatar

class ChildAdapter(
    private var items: List<ChildResponse>,
    private val onClick: (ChildResponse) -> Unit,
    private val onDelete: (ChildResponse) -> Unit = {},
) : RecyclerView.Adapter<ChildAdapter.VH>() {

    inner class VH(val binding: ItemChildBinding) : RecyclerView.ViewHolder(binding.root)

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int) =
        VH(ItemChildBinding.inflate(LayoutInflater.from(parent.context), parent, false))

    override fun getItemCount() = items.size

    override fun onBindViewHolder(holder: VH, position: Int) {
        val child = items[position]
        with(holder.binding) {
            // Avatar : initiale + cercle coloré (design), photo par-dessus si définie.
            tvChildInitial.text = ChildAvatar.initialOf(child.name)
            avatarContainer.background = ChildAvatar.circleFor(child.name)
            val childFile = com.minorshield.utils.PhotoStorage.childFile(root.context, child.id)
            val hasPhoto = com.minorshield.utils.PhotoStorage.loadInto(ivChildAvatar, childFile)
            ivChildAvatar.visibility  = if (hasPhoto) View.VISIBLE else View.GONE
            tvChildInitial.visibility = if (hasPhoto) View.GONE else View.VISIBLE

            tvChildName.text = child.age?.let { "${child.name}, $it ans" } ?: child.name

            // On distingue « appairé » (is_active) de « réellement protégé »
            // (protection_active) : un appareil appairé dont les autorisations
            // ont sauté n'est plus protégé, et le parent doit le voir.
            val ctx = root.context
            when {
                !child.is_active -> {
                    tvChildStatus.text = "Non appairé"
                    tvChildStatus.setTextColor(ctx.getColor(R.color.text_secondary))
                    statusDot.setBackgroundResource(R.drawable.bg_status_dot_inactive)
                }
                child.protection_active -> {
                    tvChildStatus.text = "Protégé"
                    tvChildStatus.setTextColor(ctx.getColor(R.color.teal))
                    statusDot.setBackgroundResource(R.drawable.bg_active_badge)
                }
                else -> {
                    tvChildStatus.text = "Protection inactive"
                    tvChildStatus.setTextColor(ctx.getColor(R.color.accent_red))
                    statusDot.setBackgroundResource(R.drawable.bg_status_dot_alert)
                }
            }

            if (child.detections_count > 0) {
                tvDetectionCount.visibility = View.VISIBLE
                tvDetectionCount.text = "${child.detections_count} détections"
            } else {
                tvDetectionCount.visibility = View.GONE
            }

            root.setOnClickListener { onClick(child) }
            btnDeleteChild.setOnClickListener { onDelete(child) }
        }
    }

    fun update(newItems: List<ChildResponse>) {
        items = newItems
        notifyDataSetChanged()
    }
}
