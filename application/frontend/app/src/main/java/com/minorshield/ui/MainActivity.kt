package com.minorshield.ui

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.Fragment
import com.google.android.material.bottomnavigation.BottomNavigationView
import com.minorshield.R
import com.minorshield.databinding.ActivityMainBinding
import com.minorshield.ui.fragments.AccueilFragment
import com.minorshield.ui.fragments.AlertesFragment
import com.minorshield.ui.fragments.HistoriqueFragment
import com.minorshield.ui.fragments.ReglagesFragment

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        if (savedInstanceState == null) {
            loadFragment(AccueilFragment())
        }

        binding.bottomNav.setOnItemSelectedListener { item ->
            val fragment: Fragment = when (item.itemId) {
                R.id.nav_accueil -> AccueilFragment()
                R.id.nav_historique -> HistoriqueFragment()
                R.id.nav_alertes -> AlertesFragment()
                R.id.nav_reglages -> ReglagesFragment()
                else -> AccueilFragment()
            }
            loadFragment(fragment)
            true
        }
    }

    private fun loadFragment(fragment: Fragment) {
        supportFragmentManager.beginTransaction()
            .replace(R.id.fragmentContainer, fragment)
            .commit()
    }

    /** Permet à un fragment de basculer vers un autre onglet (ex: la cloche
     *  du tableau de bord ouvre l'onglet Alertes). */
    fun navigateToTab(itemId: Int) {
        binding.bottomNav.selectedItemId = itemId
    }
}
