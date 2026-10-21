package com.minorshield.ui.fragments

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import com.github.mikephil.charting.data.BarData
import com.github.mikephil.charting.data.BarDataSet
import com.github.mikephil.charting.data.BarEntry
import com.google.android.material.tabs.TabLayout
import com.minorshield.R
import com.minorshield.databinding.FragmentHistoriqueBinding
import com.minorshield.network.ParentApiClient
import com.minorshield.ui.adapters.DetectionAdapter
import com.minorshield.utils.ParentPreferencesManager
import kotlinx.coroutines.launch

class HistoriqueFragment : Fragment() {

    private var _binding: FragmentHistoriqueBinding? = null
    private val binding get() = _binding!!

    private lateinit var prefs: ParentPreferencesManager
    private var currentPeriod = "week"
    private var childId: String? = null

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        _binding = FragmentHistoriqueBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        prefs = ParentPreferencesManager(requireContext())
        childId = prefs.selectedChildId.ifBlank { null }

        setupTabs()
        setupPeriodButtons()
        loadHistory()
    }

    private fun setupTabs() {
        binding.tabLayout.addOnTabSelectedListener(object : TabLayout.OnTabSelectedListener {
            override fun onTabSelected(tab: TabLayout.Tab?) {
                if (tab?.position == 0) {
                    binding.viewList.visibility = View.VISIBLE
                    binding.viewStats.visibility = View.GONE
                } else {
                    binding.viewList.visibility = View.GONE
                    binding.viewStats.visibility = View.VISIBLE
                    loadStats()
                }
            }
            override fun onTabUnselected(tab: TabLayout.Tab?) {}
            override fun onTabReselected(tab: TabLayout.Tab?) {}
        })
    }

    private fun setupPeriodButtons() {
        binding.btnPeriodDay.setOnClickListener { currentPeriod = "day"; loadStats() }
        binding.btnPeriodWeek.setOnClickListener { currentPeriod = "week"; loadStats() }
        binding.btnPeriodMonth.setOnClickListener { currentPeriod = "month"; loadStats() }
    }

    private fun loadHistory() {
        val id = childId ?: run {
            binding.emptyHistory.visibility = View.VISIBLE
            return
        }
        viewLifecycleOwner.lifecycleScope.launch {
            try {
                val resp = ParentApiClient.service.getDetections(id, 1, 50)
                // Seul écran autorisé à afficher le contenu sensible détecté
                val adapter = DetectionAdapter(resp.detections, showSensitiveContent = true)
                binding.rvHistory.layoutManager = LinearLayoutManager(requireContext())
                binding.rvHistory.adapter = adapter
                binding.emptyHistory.visibility = if (resp.detections.isEmpty()) View.VISIBLE else View.GONE
            } catch (_: Exception) {
                if (_binding != null) binding.emptyHistory.visibility = View.VISIBLE
            }
        }
    }

    private fun loadStats() {
        val id = childId ?: return
        viewLifecycleOwner.lifecycleScope.launch {
            try {
                val stats = ParentApiClient.service.getStats(id, currentPeriod)
                if (_binding == null) return@launch

                binding.tvTotalDetections.text = stats.total.toString()
                binding.tvEfficacy.text = "${stats.efficacy_pct.toInt()}%"

                val entries = stats.by_day.mapIndexed { i, day ->
                    BarEntry(i.toFloat(), day.count.toFloat())
                }
                val dataSet = BarDataSet(entries, "Détections").apply {
                    color = requireContext().getColor(R.color.teal)
                    setDrawValues(false)
                }
                binding.barChart.data = BarData(dataSet)
                binding.barChart.description.isEnabled = false
                binding.barChart.legend.isEnabled = false
                binding.barChart.invalidate()

                // Liste des applications concernées, peuplée à la main dans un
                // LinearLayout (toutes les apps, pas une seule).
                val container = binding.appStatsContainer
                container.removeAllViews()
                val rowInflater = LayoutInflater.from(requireContext())
                for (app in stats.by_app) {
                    val row = rowInflater.inflate(android.R.layout.simple_list_item_2, container, false)
                    row.findViewById<android.widget.TextView>(android.R.id.text1).text = app.app_name
                    row.findViewById<android.widget.TextView>(android.R.id.text2).text =
                        "${app.count} détections — ${app.percentage.toInt()}%"
                    container.addView(row)
                }
                binding.tvNoAppStats.visibility =
                    if (stats.by_app.isEmpty()) View.VISIBLE else View.GONE
            } catch (_: Exception) { }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
