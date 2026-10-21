package com.minorshield.ui.fragments

import android.app.AlertDialog
import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import com.minorshield.databinding.FragmentAccueilBinding
import com.minorshield.network.ChildResponse
import com.minorshield.network.ParentApiClient
import com.minorshield.R
import com.minorshield.ui.ChildDetailActivity
import com.minorshield.ui.MainActivity
import com.minorshield.ui.adapters.ChildAdapter
import com.minorshield.ui.adapters.DetectionAdapter
import com.minorshield.ui.pairing.PairingActivity
import com.minorshield.utils.ParentPreferencesManager
import kotlinx.coroutines.launch

class AccueilFragment : Fragment() {

    private var _binding: FragmentAccueilBinding? = null
    private val binding get() = _binding!!

    private lateinit var prefs: ParentPreferencesManager
    private lateinit var childAdapter: ChildAdapter
    private lateinit var detectionAdapter: DetectionAdapter
    private val pulseAnims = mutableListOf<android.animation.AnimatorSet>()

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        _binding = FragmentAccueilBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        prefs = ParentPreferencesManager(requireContext())

        // Affiche le nom ou l'email (prefix) comme fallback
        val displayName = prefs.name.ifBlank {
            prefs.email.substringBefore("@").replace(".", " ").ifBlank { "Administrateur" }
        }
        binding.tvParentName.text = displayName

        setupRecyclers()

        binding.btnAddChild.setOnClickListener {
            startActivity(Intent(requireContext(), PairingActivity::class.java))
        }

        binding.btnNotifications.setOnClickListener {
            (activity as? MainActivity)?.navigateToTab(R.id.nav_alertes)
        }
        binding.btnProfile.setOnClickListener {
            (activity as? MainActivity)?.navigateToTab(R.id.nav_reglages)
        }

        startProtectionPulse()
    }

    /** Bulles animées (expansion + fondu, en boucle) derrière le bouclier de la
     *  carte "Protection active" — deux bulles décalées pour un effet de
     *  propagation. */
    private fun startProtectionPulse() {
        pulse(binding.protectionPulse, startDelay = 0L)
        pulse(binding.protectionPulse2, startDelay = 900L)
    }

    private fun pulse(v: android.view.View, startDelay: Long) {
        val sx = android.animation.ObjectAnimator.ofFloat(v, "scaleX", 0.8f, 2.4f)
        val sy = android.animation.ObjectAnimator.ofFloat(v, "scaleY", 0.8f, 2.4f)
        val al = android.animation.ObjectAnimator.ofFloat(v, "alpha", 0.9f, 0f)
        // 5 pulsations à chaque ouverture de l'écran, puis arrêt (4 répétitions
        // en plus de la première lecture = 5 au total).
        listOf(sx, sy, al).forEach {
            it.repeatCount = 4
            it.repeatMode  = android.animation.ValueAnimator.RESTART
        }
        val set = android.animation.AnimatorSet().apply {
            duration       = 1800
            this.startDelay = startDelay
            interpolator   = android.view.animation.AccelerateDecelerateInterpolator()
            playTogether(sx, sy, al)
            start()
        }
        pulseAnims.add(set)
    }

    override fun onResume() {
        super.onResume()
        // Recharge à chaque retour sur l'écran (ex: après appairage d'un enfant)
        loadData()
    }

    private fun setupRecyclers() {
        childAdapter = ChildAdapter(
            items    = emptyList(),
            onClick  = { child ->
                // Le tap sélectionne l'enfant (pour Historique/Alertes) ET ouvre
                // sa fiche : avant, il ne se passait rien de visible.
                prefs.selectedChildId = child.id
                startActivity(
                    Intent(requireContext(), ChildDetailActivity::class.java)
                        .putExtra(ChildDetailActivity.EXTRA_CHILD_ID, child.id)
                )
            },
            onDelete = { child -> confirmDeleteChild(child) },
        )
        binding.rvChildren.layoutManager = LinearLayoutManager(requireContext())
        binding.rvChildren.adapter = childAdapter

        // Tableau de bord : pas de contenu sensible (showSensitiveContent = false).
        // Il reste visible en permanence sur l'écran d'accueil.
        detectionAdapter = DetectionAdapter(emptyList())
        binding.rvRecentDetections.layoutManager = LinearLayoutManager(requireContext())
        binding.rvRecentDetections.adapter = detectionAdapter
    }

    private fun loadData() {
        viewLifecycleOwner.lifecycleScope.launch {
            try {
                val children = ParentApiClient.service.getChildren().children
                childAdapter.update(children)
                binding.emptyChildren.visibility = if (children.isEmpty()) View.VISIBLE else View.GONE

                if (children.isNotEmpty()) {
                    // Sélectionne le premier enfant par défaut et le PERSISTE.
                    // Sans ça, les onglets Historique et Alertes n'ont aucun
                    // enfant à afficher tant que le parent n'a pas tapé
                    // manuellement sur une fiche — ils restaient vides.
                    // On corrige aussi le cas d'un enfant sélectionné supprimé.
                    if (prefs.selectedChildId.isBlank() ||
                        children.none { it.id == prefs.selectedChildId }
                    ) {
                        prefs.selectedChildId = children.first().id
                    }
                    val childId = prefs.selectedChildId
                    val history = ParentApiClient.service.getDetections(childId, 1, 5)
                    detectionAdapter.update(history.detections)
                    binding.emptyDetections.visibility = if (history.detections.isEmpty()) View.VISIBLE else View.GONE

                    // Pastille sur la cloche s'il y a au moins une alerte sérieuse.
                    val hasAlerts = history.detections.any { (it.nsfw_score ?: 0f) > 0.8f }
                    binding.notificationDot.visibility = if (hasAlerts) View.VISIBLE else View.GONE
                } else {
                    binding.notificationDot.visibility = View.GONE
                }
            } catch (_: Exception) {
                if (_binding != null) binding.emptyChildren.visibility = View.VISIBLE
            }
        }
    }

    private fun confirmDeleteChild(child: ChildResponse) {
        AlertDialog.Builder(requireContext())
            .setTitle("Supprimer ${child.name} ?")
            .setMessage("L'appareil sera dissocié et tout son historique de détections sera définitivement supprimé.")
            .setPositiveButton("Supprimer") { _, _ -> deleteChild(child) }
            .setNegativeButton("Annuler", null)
            .show()
    }

    private fun deleteChild(child: ChildResponse) {
        viewLifecycleOwner.lifecycleScope.launch {
            try {
                ParentApiClient.service.deleteChild(child.id)
                if (prefs.selectedChildId == child.id) prefs.selectedChildId = ""
                loadData()
            } catch (e: Exception) {
                if (_binding != null) {
                    Toast.makeText(requireContext(), "Échec de la suppression : ${e.message}", Toast.LENGTH_SHORT).show()
                }
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        pulseAnims.forEach { it.cancel() }
        pulseAnims.clear()
        _binding = null
    }
}
