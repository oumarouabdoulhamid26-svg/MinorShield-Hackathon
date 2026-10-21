package com.minorshield.ui

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.graphics.Paint
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.lifecycle.lifecycleScope
import com.minorshield.R
import com.minorshield.databinding.ActivitySubscriptionBinding
import com.minorshield.network.SubscriptionPlan
import com.minorshield.utils.SubscriptionManager
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class SubscriptionActivity : AppCompatActivity() {

    private lateinit var binding: ActivitySubscriptionBinding
    private lateinit var subscriptionManager: SubscriptionManager

    private var selectedPlan: SubscriptionPlan = SubscriptionPlan.ANNUAL
    private var pendingRef: String? = null

    private val features = listOf(
        "Surveillance en temps réel illimitée",
        "Historique complet des détections (scores + texte OCR)",
        "Plages horaires de blocage configurables",
        "Gestion avancée des applications surveillées",
        "Alertes push immédiates sur votre smartphone",
        "Tableau de bord avec graphiques statistiques"
    )

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivitySubscriptionBinding.inflate(layoutInflater)
        setContentView(binding.root)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        title = getString(R.string.title_subscription)

        subscriptionManager = SubscriptionManager(this)

        setupFeatures()
        binding.tvAnnualOldPrice.paintFlags =
            binding.tvAnnualOldPrice.paintFlags or Paint.STRIKE_THRU_TEXT_FLAG
        renderStatusCard()
        refreshStatus()
        setupPlanSelection()
        setupPayButton()

        // Annuel sélectionné par défaut
        binding.rbAnnual.isChecked = true
        selectedPlan = SubscriptionPlan.ANNUAL
    }

    override fun onResume() {
        super.onResume()
        // Retour du navigateur après paiement Monetbil → vérifier automatiquement
        val ref = pendingRef
        if (ref != null) {
            verifyPayment(ref, auto = true)
        } else {
            refreshStatus()
        }
    }

    // ── Fonctionnalités ───────────────────────────────────────────────────────

    private fun setupFeatures() {
        val views = listOf(
            binding.feat1, binding.feat2, binding.feat3,
            binding.feat4, binding.feat5, binding.feat6
        )
        views.forEachIndexed { i, view ->
            view.tvFeatureText.text = features.getOrElse(i) { "" }
        }
    }

    // ── Statut ────────────────────────────────────────────────────────────────

    /** Rafraîchit le statut depuis le backend puis met à jour la carte. */
    private fun refreshStatus() {
        lifecycleScope.launch {
            subscriptionManager.refreshFromBackend()
            renderStatusCard()
        }
    }

    private fun renderStatusCard() {
        val status = subscriptionManager.currentStatus
        if (status.isActive) {
            val fmt    = SimpleDateFormat("dd/MM/yyyy", Locale.FRANCE)
            val expiry = fmt.format(Date(status.expiresAt))
            binding.tvStatusIcon.setImageResource(R.drawable.ic_shield_check)
            binding.tvStatusIcon.setColorFilter(ContextCompat.getColor(this, R.color.icon_green))
            binding.tvStatusTitle.text  = "Premium actif — ${status.plan?.label ?: ""}"
            binding.tvStatusDetail.text = "Expire le $expiry · ${status.daysRemaining} jours restants"
            binding.btnSubscribe.text   = "Renouveler l'abonnement"
        } else {
            binding.tvStatusIcon.setImageResource(R.drawable.ic_lock)
            binding.tvStatusIcon.setColorFilter(ContextCompat.getColor(this, R.color.text_hint))
            binding.tvStatusTitle.text  = "Plan gratuit"
            binding.tvStatusDetail.text = "Fonctionnalités limitées"
            binding.btnSubscribe.text   = "Payer avec MTN / Orange Money"
        }
    }

    // ── Sélection du plan ─────────────────────────────────────────────────────

    private fun setupPlanSelection() {
        binding.cardMonthly.setOnClickListener { selectPlan(SubscriptionPlan.MONTHLY) }
        binding.cardAnnual.setOnClickListener  { selectPlan(SubscriptionPlan.ANNUAL)  }
        binding.rbMonthly.setOnClickListener   { selectPlan(SubscriptionPlan.MONTHLY) }
        binding.rbAnnual.setOnClickListener    { selectPlan(SubscriptionPlan.ANNUAL)  }
    }

    private fun selectPlan(plan: SubscriptionPlan) {
        selectedPlan            = plan
        binding.rbMonthly.isChecked = plan == SubscriptionPlan.MONTHLY
        binding.rbAnnual.isChecked  = plan == SubscriptionPlan.ANNUAL
    }

    // ── Paiement ──────────────────────────────────────────────────────────────

    private fun setupPayButton() {
        binding.btnSubscribe.setOnClickListener { startPayment() }
    }

    private fun startPayment() {
        setLoading(true)
        showMessage("Génération du lien de paiement…", isError = false)

        lifecycleScope.launch {
            try {
                val resp = com.minorshield.network.ParentApiClient.service
                    .initiatePayment(com.minorshield.network.PaymentInitiateRequest(selectedPlan.name))

                pendingRef = resp.transaction_ref

                startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(resp.widget_url)))
                setLoading(false)
            } catch (e: Exception) {
                setLoading(false)
                showMessage("Erreur : impossible d'initialiser le paiement", isError = true)
            }
        }
    }

    private fun verifyPayment(ref: String, auto: Boolean = false) {
        setLoading(true)
        if (!auto) showMessage("Vérification du paiement en cours…", isError = false)

        lifecycleScope.launch {
            delay(if (auto) 4000L else 2000L)

            try {
                val active = subscriptionManager.refreshFromBackend()
                setLoading(false)
                renderStatusCard()
                if (active) {
                    pendingRef = null
                    showMessage("Paiement confirmé ! Abonnement Premium activé.", isError = false)
                } else {
                    if (!auto) showMessage("Paiement non confirmé. Vérifiez votre solde MTN / Orange.", isError = true)
                    else binding.tvMessage.visibility = View.GONE
                }
            } catch (e: Exception) {
                setLoading(false)
                showMessage("Erreur de vérification : ${e.message}", isError = true)
            }
        }
    }

    // ── UI Helpers ────────────────────────────────────────────────────────────

    private fun setLoading(loading: Boolean) {
        binding.progressBar.visibility = if (loading) View.VISIBLE else View.GONE
        binding.btnSubscribe.isEnabled  = !loading
    }

    private fun showMessage(msg: String, isError: Boolean) {
        binding.tvMessage.apply {
            visibility = View.VISIBLE
            text       = msg
            setTextColor(
                ContextCompat.getColor(
                    this@SubscriptionActivity,
                    if (isError) android.R.color.holo_red_dark else R.color.primary
                )
            )
        }
    }

    override fun onSupportNavigateUp(): Boolean {
        onBackPressedDispatcher.onBackPressed()
        return true
    }
}
