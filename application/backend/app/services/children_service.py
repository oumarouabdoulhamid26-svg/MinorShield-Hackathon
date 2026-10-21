
# app/services/children_service.py
# Appairage parent↔enfant et gestion des enfants.

import random
import string
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.db_models import Child, Detection, Parent
from app.schemas.children import (
    PairingRequest, PairingResponse,
    ChildRegisterRequest, ChildRegisterResponse,
    ChildResponse, ChildListResponse,
)
from app.schemas.auth import VerifyPinResponse
from app.services.auth_service import verify_password

PAIRING_CODE_LENGTH = 6
PAIRING_EXPIRY_HOURS = 24

# Intensité de blocage → seuil de détection. Plus l'intensité est élevée (enfant
# jeune), plus le seuil est BAS → on bloque plus tôt. La vitesse d'analyse n'est
# jamais affectée : seul ce qui est jugé "sensible" change selon l'âge.
BLOCK_INTENSITY_THRESHOLDS = {
    "moyen":      0.80,   # ado plus âgé : ne bloque que le contenu franchement explicite
    "eleve":      0.65,   # défaut
    "tres_eleve": 0.50,   # jeune enfant : bloque dès le moindre doute
}
DEFAULT_INTENSITY = "eleve"


def intensity_threshold(intensity: str | None) -> float:
    return BLOCK_INTENSITY_THRESHOLDS.get(
        intensity or DEFAULT_INTENSITY,
        BLOCK_INTENSITY_THRESHOLDS[DEFAULT_INTENSITY],
    )

# Au-delà de ce délai sans signal de l'app enfant, la protection est
# considérée comme inactive (app fermée, tuée par l'OS, téléphone éteint...).
HEARTBEAT_TIMEOUT_MINUTES = 5


def _random_code() -> str:
    return "".join(random.choices(string.digits, k=PAIRING_CODE_LENGTH))


def create_pairing(db: Session, parent_id: str, req: PairingRequest) -> PairingResponse:
    code    = _random_code()
    expires = datetime.utcnow() + timedelta(hours=PAIRING_EXPIRY_HOURS)

    child = Child(
        parent_id          = parent_id,
        name               = req.name,
        age                = req.age,
        pairing_code       = code,
        pairing_expires_at = expires,
        is_active          = False,
    )
    db.add(child)
    db.commit()
    db.refresh(child)

    return PairingResponse(
        child_id     = child.id,
        child_name   = child.name,
        pairing_code = code,
        expires_in   = PAIRING_EXPIRY_HOURS * 3600,
    )


def regenerate_pairing_code(db: Session, parent_id: str, child_id: str) -> PairingResponse:
    """Génère un nouveau code d'appairage pour un enfant pas encore lié."""
    child = db.query(Child).filter(Child.id == child_id, Child.parent_id == parent_id).first()
    if child is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enfant introuvable.")
    if child.is_active:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cet appareil est déjà lié : aucun code nécessaire."
        )

    child.pairing_code       = _random_code()
    child.pairing_expires_at = datetime.utcnow() + timedelta(hours=PAIRING_EXPIRY_HOURS)
    db.commit()
    db.refresh(child)

    return PairingResponse(
        child_id     = child.id,
        child_name   = child.name,
        pairing_code = child.pairing_code,
        expires_in   = PAIRING_EXPIRY_HOURS * 3600,
    )


def register_child_device(db: Session, req: ChildRegisterRequest) -> ChildRegisterResponse:
    child = (
        db.query(Child)
        .filter(Child.pairing_code == req.pairing_code, Child.is_active == False)
        .first()
    )

    if child is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Code d'appairage invalide ou déjà utilisé."
        )

    if datetime.utcnow() > child.pairing_expires_at:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Code d'appairage expiré. Demandez un nouveau code au parent."
        )

    child.is_active          = True
    child.pairing_code       = None
    child.pairing_expires_at = None
    child.device_fcm_token   = req.device_fcm_token
    child.device_model       = req.device_model
    child.paired_at          = datetime.utcnow()
    db.commit()
    db.refresh(child)

    return ChildRegisterResponse(
        child_id   = child.id,
        child_name = child.name,
        parent_id  = child.parent_id,
    )


def _is_protection_live(child: Child) -> bool:
    """
    La protection n'est réellement active que si l'app enfant l'a confirmée
    ET qu'elle a donné signe de vie récemment. Sans ce contrôle de fraîcheur,
    un appareil éteint ou une app tuée apparaîtrait encore comme protégé.
    """
    if not child.protection_active or child.last_seen_at is None:
        return False
    age = datetime.utcnow() - child.last_seen_at
    return age <= timedelta(minutes=HEARTBEAT_TIMEOUT_MINUTES)


def _protection_level(child: Child) -> str:
    """
    Traduit l'état réel des briques de surveillance en un niveau lisible :

    - inactive : aucun signal récent (app fermée, tuée, téléphone éteint)
    - degraded : la capture ou le blocage manque → rien ne peut être bloqué
    - partial  : protection opérationnelle, mais l'app consultée reste inconnue
    - complete : les trois briques fonctionnent
    """
    if not _is_protection_live(child):
        return "inactive"
    if not (child.capture_active and child.overlay_allowed):
        return "degraded"
    return "complete" if child.usage_access else "partial"


def record_heartbeat(
    db               : Session,
    child_id         : str,
    protection_active: bool,
    capture_active   : bool | None = None,
    overlay_allowed  : bool | None = None,
    usage_access     : bool | None = None,
) -> None:
    child = db.query(Child).filter(Child.id == child_id).first()
    if child is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enfant introuvable.")

    child.protection_active = protection_active
    # Repli sur protection_active si l'app enfant n'envoie pas encore le détail
    child.capture_active  = capture_active if capture_active is not None else protection_active
    child.overlay_allowed = overlay_allowed if overlay_allowed is not None else protection_active
    if usage_access is not None:
        child.usage_access = usage_access
    child.last_seen_at = datetime.utcnow()
    db.commit()


def list_children(db: Session, parent_id: str) -> ChildListResponse:
    children = db.query(Child).filter(Child.parent_id == parent_id).all()

    result = []
    for c in children:
        # On ne compte QUE le contenu inapproprié (label == "nsfw") : le sain
        # ne doit pas gonfler le nombre affiché au parent.
        count = db.query(Detection).filter(
            Detection.child_id == c.id,
            Detection.label == "nsfw",
        ).count()
        last  = (
            db.query(Detection)
            .filter(Detection.child_id == c.id, Detection.label == "nsfw")
            .order_by(Detection.timestamp.desc())
            .first()
        )
        result.append(ChildResponse(
            id               = c.id,
            name             = c.name,
            age              = c.age,
            is_active        = c.is_active,
            created_at       = c.created_at.isoformat(),
            detections_count = count,
            last_detection   = last.timestamp.isoformat() if last else None,
            protection_active= _is_protection_live(c),
            last_seen_at     = c.last_seen_at.isoformat() if c.last_seen_at else None,
            device_model     = c.device_model,
            paired_at        = c.paired_at.isoformat() if c.paired_at else None,
            protection_level = _protection_level(c),
            is_locked        = bool(c.is_locked),
            warning_limit    = _effective_warning_limit(c),
            warnings_used    = c.warnings_used or 0,
            pairing_code     = c.pairing_code,
            pairing_expires_at = c.pairing_expires_at.isoformat() if c.pairing_expires_at else None,
            block_intensity  = c.block_intensity or DEFAULT_INTENSITY,
            custom_keywords  = c.custom_keywords,
        ))

    return ChildListResponse(children=result, total=len(result))


def update_child(
    db             : Session,
    parent_id      : str,
    child_id       : str,
    age            : int | None,
    block_intensity: str | None,
    custom_keywords: str | None,
) -> None:
    """Met à jour les réglages par enfant : âge, intensité, mots sensibles perso."""
    child = db.query(Child).filter(Child.id == child_id, Child.parent_id == parent_id).first()
    if child is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enfant introuvable.")

    if age is not None:
        child.age = age
    if block_intensity is not None:
        if block_intensity not in BLOCK_INTENSITY_THRESHOLDS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Intensité invalide (moyen | eleve | tres_eleve).",
            )
        child.block_intensity = block_intensity
    if custom_keywords is not None:
        child.custom_keywords = custom_keywords.strip() or None

    db.commit()


def delete_child(db: Session, parent_id: str, child_id: str) -> None:
    child = db.query(Child).filter(Child.id == child_id, Child.parent_id == parent_id).first()
    if child is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enfant introuvable.")
    db.delete(child)
    db.commit()


def lock_child(db: Session, child_id: str) -> None:
    child = db.query(Child).filter(Child.id == child_id).first()
    if child is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enfant introuvable.")
    child.is_locked = True
    db.commit()


def unlock_child(db: Session, parent_id: str, child_id: str) -> None:
    child = db.query(Child).filter(Child.id == child_id, Child.parent_id == parent_id).first()
    if child is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enfant introuvable.")
    child.is_locked = False
    # Débloquer sans remettre le compteur à zéro re-bloquerait l'enfant au
    # prochain contenu sensible. Le déblocage parent redonne donc les avertissements.
    child.warnings_used = 0
    child.warnings_reset_day = _today_str()
    db.commit()


# ── Système d'avertissements ─────────────────────────────────────────────────

def _today_str() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d")


def _effective_warning_limit(child: Child) -> int:
    """Limite d'avertissements : None → défaut 3. 0 signifie « illimité »
    (jamais de blocage sur quota) et est conservé tel quel — d'où le test
    explicite sur None plutôt qu'un `or 3` qui écraserait le 0."""
    return 3 if child.warning_limit is None else child.warning_limit


def _reset_warnings_if_new_day(child: Child) -> None:
    """Remise à zéro quotidienne : si on a changé de jour, le compteur repart."""
    today = _today_str()
    if child.warnings_reset_day != today:
        child.warnings_used = 0
        child.warnings_reset_day = today


def register_incident(db: Session, child_id: str) -> dict:
    """
    Enregistre un contenu sensible détecté et fait avancer le système
    d'avertissements. Renvoie l'état à afficher à l'enfant.
    """
    child = db.query(Child).filter(Child.id == child_id).first()
    if child is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enfant introuvable.")

    _reset_warnings_if_new_day(child)

    # limite == 0 → « illimité » : on avertit toujours, on ne bloque jamais.
    limit = _effective_warning_limit(child)
    unlimited = (limit == 0)

    # Déjà bloqué : on reste bloqué (le parent seul débloque).
    if child.is_locked:
        db.commit()
        return {"status": "blocked", "warnings_used": limit,
                "warning_limit": limit, "remaining": 0}

    child.warnings_used = (child.warnings_used or 0) + 1

    if not unlimited and child.warnings_used >= limit:
        child.is_locked = True
        db.commit()
        return {"status": "blocked", "warnings_used": child.warnings_used,
                "warning_limit": limit, "remaining": 0}

    db.commit()
    remaining = 0 if unlimited else (limit - child.warnings_used)
    return {"status": "warning", "warnings_used": child.warnings_used,
            "warning_limit": limit, "remaining": remaining}


def set_warning_limit(db: Session, parent_id: str, child_id: str, limit: int) -> None:
    child = db.query(Child).filter(Child.id == child_id, Child.parent_id == parent_id).first()
    if child is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enfant introuvable.")
    # 0 (ou négatif) = illimité ; sinon on borne à un maximum raisonnable.
    child.warning_limit = 0 if limit <= 0 else min(limit, 99)
    db.commit()


def reset_warnings(db: Session, parent_id: str, child_id: str) -> None:
    child = db.query(Child).filter(Child.id == child_id, Child.parent_id == parent_id).first()
    if child is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enfant introuvable.")
    child.warnings_used = 0
    child.warnings_reset_day = _today_str()
    child.is_locked = False
    db.commit()


def verify_child_pin(db: Session, child_id: str, pin: str) -> VerifyPinResponse:
    child = db.query(Child).filter(Child.id == child_id).first()
    if child is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enfant introuvable.")

    parent = db.query(Parent).filter(Parent.id == child.parent_id).first()
    if parent is None or not parent.pin_hash:
        return VerifyPinResponse(valid=False, pin_configured=False)

    return VerifyPinResponse(valid=verify_password(pin, parent.pin_hash), pin_configured=True)


def unpair_device(db: Session, child_id: str) -> None:
    child = db.query(Child).filter(Child.id == child_id).first()
    if child is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enfant introuvable.")

    child.is_active          = False
    child.is_locked          = False
    child.protection_active  = False
    child.capture_active     = False
    child.overlay_allowed    = False
    child.usage_access       = False
    child.last_seen_at       = None
    child.paired_at          = None
    child.device_model       = None
    child.device_fcm_token   = None
    child.pairing_code       = _random_code()
    child.pairing_expires_at = datetime.utcnow() + timedelta(hours=PAIRING_EXPIRY_HOURS)
    db.commit()


def disconnect_child_device(db: Session, parent_id: str, child_id: str) -> PairingResponse:
    """
    Déconnexion à distance par le parent : rompt la liaison avec l'appareil de
    l'enfant sans supprimer l'enfant ni son historique. Un nouveau code
    d'appairage est généré pour permettre de relier un appareil plus tard.
    """
    child = db.query(Child).filter(Child.id == child_id, Child.parent_id == parent_id).first()
    if child is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enfant introuvable.")

    # unpair_device réinitialise l'état de l'appareil ET génère un nouveau code.
    unpair_device(db, child_id)
    db.refresh(child)

    return PairingResponse(
        child_id     = child.id,
        child_name   = child.name,
        pairing_code = child.pairing_code,
        expires_in   = PAIRING_EXPIRY_HOURS * 3600,
    )


def get_lock_status(db: Session, child_id: str) -> dict:
    child = db.query(Child).filter(Child.id == child_id).first()
    if child is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enfant introuvable.")

    # On renvoie aussi la raison du blocage : l'écran de l'enfant peut ainsi
    # expliquer ce qui a été détecté, au lieu d'un message générique.
    reason = None
    if child.is_locked:
        last = (
            db.query(Detection)
            .filter(Detection.child_id == child_id, Detection.label == "nsfw")
            .order_by(Detection.timestamp.desc())
            .first()
        )
        reason = last.category if last else None

    return {
        "is_locked"    : child.is_locked,
        "reason"       : reason,
        "warning_limit": _effective_warning_limit(child),
        "warnings_used": child.warnings_used or 0,
    }
