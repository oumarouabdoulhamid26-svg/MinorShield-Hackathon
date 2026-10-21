"""
Endpoints Monetbil — Système de paiement MinorShield.

Flux :
  1. POST /payment/initiate  (JWT)  → génère URL widget Monetbil
  2. Widget Monetbil → parent paie (MTN / Orange Money)
  3. POST /payment/notify    (Monetbil webhook) → active l'abonnement
  4. GET  /payment/status    (JWT)  → statut abonnement du parent
"""
import hashlib
import urllib.parse
import uuid

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.core.auth_jwt import get_current_parent_id
from app.core.config import settings
from app.core.database import get_db
from app.schemas.payment import (
    PaymentInitiateRequest,
    PaymentInitiateResponse,
    SubscriptionStatusResponse,
)
from app.services.subscription_service import (
    activate_subscription,
    find_subscription_by_ref,
    get_subscription_status,
    PLAN_AMOUNTS,
)

router = APIRouter(prefix="/payment", tags=["Paiement"])

MONETBIL_WIDGET_URL = "https://api.monetbil.com/widget/v2.1"


def _build_widget_url(plan: str, ref: str) -> str:
    amount   = PLAN_AMOUNTS.get(plan, 2000)
    notify   = f"{settings.PUBLIC_URL}/api/v1/payment/notify"
    return_u = f"{settings.PUBLIC_URL}/api/v1/payment/return"
    params   = (
        f"?amount={amount}"
        f"&ref={ref}"
        f"&currency=XAF"
        f"&return_url={urllib.parse.quote(return_u)}"
        f"&notify_url={urllib.parse.quote(notify)}"
        f"&country=CM"
        f"&lang=fr"
    )
    return f"{MONETBIL_WIDGET_URL}/{settings.MONETBIL_SERVICE_KEY}{params}"


# ── 1. Initier le paiement ────────────────────────────────────────────────────

@router.post(
    "/initiate",
    response_model=PaymentInitiateResponse,
    summary="Générer le lien de paiement Monetbil",
)
def initiate_payment(
    req      : PaymentInitiateRequest,
    parent_id: str = Depends(get_current_parent_id),
    db       : Session = Depends(get_db),
):
    plan   = req.plan.upper()
    ref    = f"MS_{plan[0]}_{uuid.uuid4().hex[:12].upper()}"
    amount = PLAN_AMOUNTS.get(plan, 2000)
    url    = _build_widget_url(plan, ref)

    # Pré-enregistrer la référence (plan en attente)
    from app.services.subscription_service import get_or_create_subscription
    sub = get_or_create_subscription(db, parent_id)
    sub.transaction_ref = ref
    sub.plan            = plan
    db.commit()

    return PaymentInitiateResponse(
        widget_url      = url,
        transaction_ref = ref,
        amount          = amount,
    )


# ── 2. Webhook Monetbil ───────────────────────────────────────────────────────

@router.post(
    "/notify",
    summary="Webhook Monetbil — activation abonnement (appelé par Monetbil)",
)
async def payment_notify(request: Request, db: Session = Depends(get_db)):
    body = await request.form()

    status         = body.get("status", "")
    payment_ref    = body.get("payment_ref", "")
    transaction_id = body.get("transaction_ID", "")
    phone          = body.get("phone", "")

    # Monetbil peut renvoyer le montant comme "2500" ou "2500.00" → parse robuste
    try:
        amount = int(float(body.get("amount", 0) or 0))
    except (TypeError, ValueError):
        amount = 0

    # Vérification de la signature Monetbil
    received_sign = body.get("sign", "")
    expected_sign = hashlib.sha1(
        f"{settings.MONETBIL_SERVICE_SECRET}{payment_ref}".encode()
    ).hexdigest()

    if received_sign and received_sign != expected_sign:
        return {"message": "Signature invalide"}

    if status.lower() != "success":
        return {"message": "Paiement non réussi"}

    sub = find_subscription_by_ref(db, payment_ref)
    if not sub:
        return {"message": "Référence introuvable"}

    # Idempotence : /notify et /return peuvent tous deux arriver pour le même
    # paiement — on n'active (et ne prolonge) qu'une seule fois.
    if sub.is_active and sub.transaction_ref == payment_ref:
        return {"message": "Abonnement déjà activé"}

    activate_subscription(
        db, sub.parent_id, sub.plan,
        payment_ref, transaction_id, amount, phone,
    )
    return {"message": "Abonnement activé"}


# ── 2bis. Page de retour navigateur ───────────────────────────────────────────

@router.get(
    "/return",
    response_class=HTMLResponse,
    summary="Page affichée dans le navigateur après le paiement Monetbil",
)
def payment_return(request: Request, db: Session = Depends(get_db)):
    # Monetbil redirige le navigateur du parent ici après le widget, en
    # ajoutant le résultat en paramètres (status, payment_ref...).
    # On active ici en complément du webhook /notify : utile quand le webhook
    # ne peut pas atteindre le serveur (test sur réseau local), car le
    # navigateur du téléphone, lui, joint bien la machine sur le LAN.
    params      = request.query_params
    status      = (params.get("status") or "").lower()
    payment_ref = params.get("payment_ref") or params.get("ref") or ""

    activated = False
    if status == "success" and payment_ref:
        sub = find_subscription_by_ref(db, payment_ref)
        if sub and not sub.is_active:
            try:
                amount = int(float(params.get("amount", 0) or 0))
            except (TypeError, ValueError):
                amount = 0
            activate_subscription(
                db, sub.parent_id, sub.plan, payment_ref,
                params.get("transaction_id", "") or params.get("transaction_ID", ""),
                amount, params.get("phone", ""),
            )
            activated = True
        elif sub and sub.is_active:
            activated = True

    message = (
        "Votre abonnement Premium est activé. Revenez dans l'application."
        if activated else
        "Vous pouvez revenir dans l'application MinorShield. Votre abonnement "
        "sera activé automatiquement dès confirmation."
    )
    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>MinorShield — Paiement</title>
        <style>
            body { font-family: -apple-system, Roboto, Arial, sans-serif;
                   background: #0A1628; color: #fff; margin: 0;
                   display: flex; min-height: 100vh; align-items: center;
                   justify-content: center; text-align: center; }
            .card { max-width: 360px; padding: 40px 28px; }
            .icon { font-size: 56px; margin-bottom: 16px; }
            h1 { font-size: 22px; margin: 0 0 12px; }
            p { color: #B0C4DE; font-size: 15px; line-height: 1.5; margin: 0; }
            .teal { color: #4DB6AC; }
        </style>
    </head>
    <body>
        <div class="card">
            <div class="icon">🛡️</div>
            <h1>Paiement traité</h1>
            <p class="teal">{message}</p>
        </div>
    </body>
    </html>
    """


# ── 3. Statut abonnement ──────────────────────────────────────────────────────

@router.get(
    "/status",
    response_model=SubscriptionStatusResponse,
    summary="Statut de l'abonnement du parent connecté",
)
def payment_status(
    parent_id: str = Depends(get_current_parent_id),
    db       : Session = Depends(get_db),
):
    return get_subscription_status(db, parent_id)
