package com.minorshield.ui.fragments

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import com.minorshield.databinding.FragmentAlertesBinding
import com.minorshield.network.ParentApiClient
import com.minorshield.ui.adapters.AlertAdapter
import com.minorshield.utils.ParentPreferencesManager
import kotlinx.coroutines.launch

class AlertesFragment : Fragment() {

    private var _binding: FragmentAlertesBinding? = null
    private val binding get() = _binding!!

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        _binding = FragmentAlertesBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        val prefs = ParentPreferencesManager(requireContext())
        val childId = prefs.selectedChildId.ifBlank { null }

        if (childId == null) {
            binding.emptyAlerts.visibility = View.VISIBLE
            binding.rvAlerts.visibility = View.GONE
            return
        }

        viewLifecycleOwner.lifecycleScope.launch {
            try {
                // Le déblocage à distance n'est proposé que si l'enfant est
                // actuellement bloqué (avertissements épuisés).
                val isLocked = ParentApiClient.service.getChildren().children
                    .firstOrNull { it.id == childId }?.is_locked == true

                val resp = ParentApiClient.service.getDetections(childId, 1, 100)
                val alerts = resp.detections.filter { it.nsfw_score > 0.8f }.toMutableList()
                if (_binding == null) return@launch

                if (alerts.isEmpty()) {
                    binding.emptyAlerts.visibility = View.VISIBLE
                    binding.rvAlerts.visibility = View.GONE
                } else {
                    binding.emptyAlerts.visibility = View.GONE
                    binding.rvAlerts.visibility = View.VISIBLE
                    binding.rvAlerts.layoutManager = LinearLayoutManager(requireContext())
                    lateinit var adapter: AlertAdapter
                    adapter = AlertAdapter(alerts, showUnlock = isLocked) { position ->
                        unlockChild(childId) { adapter.removeAt(position) }
                    }
                    binding.rvAlerts.adapter = adapter
                }
            } catch (_: Exception) {
                if (_binding != null) binding.emptyAlerts.visibility = View.VISIBLE
            }
        }
    }

    /** Débloque l'enfant puis, en cas de succès, retire l'alerte concernée. */
    private fun unlockChild(childId: String, onSuccess: () -> Unit) {
        viewLifecycleOwner.lifecycleScope.launch {
            try {
                ParentApiClient.service.unlockChild(childId)
                if (isAdded) Toast.makeText(requireContext(), "Appareil débloqué avec succès", Toast.LENGTH_SHORT).show()
                onSuccess()
            } catch (_: Exception) {
                if (isAdded) Toast.makeText(requireContext(), "Erreur : vérifiez la connexion au serveur", Toast.LENGTH_SHORT).show()
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
