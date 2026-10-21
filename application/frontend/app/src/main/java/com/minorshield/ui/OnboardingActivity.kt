package com.minorshield.ui

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.ImageView
import android.widget.LinearLayout
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.minorshield.R
import com.minorshield.databinding.ActivityOnboardingBinding
import com.minorshield.utils.ParentPreferencesManager

class OnboardingActivity : AppCompatActivity() {

    private lateinit var binding: ActivityOnboardingBinding
    private lateinit var prefs: ParentPreferencesManager
    private var currentPage = 0

    private val pages = listOf(
        Triple(R.drawable.ic_onboarding_surveillance, R.string.onboarding_1_title, R.string.onboarding_1_desc),
        Triple(R.drawable.ic_onboarding_ai,           R.string.onboarding_2_title, R.string.onboarding_2_desc),
        Triple(R.drawable.ic_onboarding_shield,       R.string.onboarding_3_title, R.string.onboarding_3_desc),
    )

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityOnboardingBinding.inflate(layoutInflater)
        setContentView(binding.root)

        prefs = ParentPreferencesManager(this)
        setupDots()
        showPage(0)

        binding.btnSkip.setOnClickListener { finishOnboarding() }
        binding.btnNext.setOnClickListener {
            if (currentPage < pages.size - 1) {
                showPage(currentPage + 1)
            } else {
                finishOnboarding()
            }
        }
    }

    private fun showPage(index: Int) {
        currentPage = index
        val (icon, title, desc) = pages[index]
        binding.ivOnboarding.setImageResource(icon)
        binding.tvTitle.setText(title)
        binding.tvDesc.setText(desc)
        updateDots(index)

        if (index == pages.size - 1) {
            binding.btnNext.setText(R.string.btn_start)
            binding.btnSkip.visibility = View.GONE
        } else {
            binding.btnNext.setText(R.string.btn_next)
            binding.btnSkip.visibility = View.VISIBLE
        }
    }

    private fun setupDots() {
        binding.dotsContainer.removeAllViews()
        repeat(pages.size) {
            val dot = ImageView(this).apply {
                layoutParams = LinearLayout.LayoutParams(10.dp, 10.dp).also {
                    it.marginEnd = 8.dp
                }
                setImageResource(R.drawable.dot_inactive)
            }
            binding.dotsContainer.addView(dot)
        }
    }

    private fun updateDots(active: Int) {
        repeat(pages.size) { i ->
            val dot = binding.dotsContainer.getChildAt(i) as? ImageView ?: return@repeat
            dot.setImageResource(if (i == active) R.drawable.dot_active else R.drawable.dot_inactive)
        }
    }

    private fun finishOnboarding() {
        prefs.isOnboardingDone = true
        startActivity(Intent(this, RegisterActivity::class.java))
        finish()
    }

    private val Int.dp get() = (this * resources.displayMetrics.density).toInt()
}
