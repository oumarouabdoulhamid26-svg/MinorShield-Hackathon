
# app/services/auth_service.py
# Gestion des comptes parent : inscription et connexion.

import random
from datetime import datetime, timedelta

import bcrypt
from sqlalchemy.orm import Session

from app.models.db_models import Parent

VERIFICATION_TTL_MINUTES = 15


def _generate_code() -> str:
    return f"{random.randint(0, 999999):06d}"


def _issue_verification(db: Session, parent: Parent) -> None:
    """Génère un code, l'enregistre et l'envoie par e-mail. Si la vérification
    est désactivée ou le SMTP absent, le compte est auto-vérifié."""
    from app.core.config import settings
    from app.services.email_service import send_verification_email, smtp_configured

    if not (settings.EMAIL_VERIFICATION_ENABLED and smtp_configured()):
        parent.email_verified = True
        parent.verification_code = None
        parent.verification_expires_at = None
        db.commit()
        return

    code = _generate_code()
    parent.email_verified = False
    parent.verification_code = code
    parent.verification_expires_at = datetime.utcnow() + timedelta(minutes=VERIFICATION_TTL_MINUTES)
    db.commit()
    send_verification_email(parent.email, code, parent.name)


def verify_email(db: Session, parent_id: str, code: str) -> None:
    from fastapi import HTTPException, status
    parent = db.query(Parent).filter(Parent.id == parent_id).first()
    if parent is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compte introuvable.")
    if parent.email_verified:
        return
    if not parent.verification_code or parent.verification_expires_at is None:
        raise HTTPException(status_code=400, detail="Aucun code en attente. Demandez un nouveau code.")
    if datetime.utcnow() > parent.verification_expires_at:
        raise HTTPException(status_code=410, detail="Code expiré. Demandez un nouveau code.")
    if code.strip() != parent.verification_code:
        raise HTTPException(status_code=403, detail="Code incorrect.")
    parent.email_verified = True
    parent.verification_code = None
    parent.verification_expires_at = None
    db.commit()


def resend_verification(db: Session, parent_id: str) -> None:
    from fastapi import HTTPException, status
    parent = db.query(Parent).filter(Parent.id == parent_id).first()
    if parent is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compte introuvable.")
    if not parent.email_verified:
        _issue_verification(db, parent)
from app.schemas.auth import (
    RegisterRequest, LoginRequest, TokenResponse, VerifyPinResponse,
)
from app.core.auth_jwt import create_access_token


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def update_fcm_token(db: Session, parent_id: str, token: str) -> None:
    """Enregistre le token FCM de l'appareil du parent (notifications push)."""
    from fastapi import HTTPException, status
    parent = db.query(Parent).filter(Parent.id == parent_id).first()
    if parent is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compte introuvable.")
    parent.fcm_token = token
    db.commit()


def verify_parent_pin(db: Session, parent_id: str, pin: str) -> VerifyPinResponse:
    """Vérifie le PIN du parent connecté (déverrouillage de l'app parent)."""
    parent = db.query(Parent).filter(Parent.id == parent_id).first()
    if parent is None or not parent.pin_hash:
        # Aucun PIN configuré → l'app laissera passer et invitera à en définir un.
        return VerifyPinResponse(valid=False, pin_configured=False)

    return VerifyPinResponse(valid=verify_password(pin, parent.pin_hash), pin_configured=True)


def set_parent_pin(
    db         : Session,
    parent_id  : str,
    pin        : str,
    current_pin: str | None = None,
) -> None:
    """
    Définit le PIN parent.

    Si un PIN existe déjà, le PIN actuel est exigé et vérifié : la simple
    possession d'une session ouverte ne doit pas suffire à le remplacer.
    """
    from fastapi import HTTPException, status
    parent = db.query(Parent).filter(Parent.id == parent_id).first()
    if parent is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compte introuvable.")

    if parent.pin_hash:
        if not current_pin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le PIN actuel est requis pour le modifier.",
            )
        if not verify_password(current_pin, parent.pin_hash):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="PIN actuel incorrect.",
            )

    parent.pin_hash = hash_password(pin)
    db.commit()


def update_notif_prefs(db: Session, parent_id: str, on_detection: bool, daily_summary: bool) -> None:
    """Met à jour les préférences de notification du parent."""
    from fastapi import HTTPException, status
    parent = db.query(Parent).filter(Parent.id == parent_id).first()
    if parent is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compte introuvable.")
    parent.notif_on_detection  = on_detection
    parent.notif_daily_summary = daily_summary
    db.commit()


def update_profile(db: Session, parent_id: str, name: str | None, email: str):
    """Met à jour le nom et l'email du parent. L'email doit rester unique."""
    from fastapi import HTTPException, status
    parent = db.query(Parent).filter(Parent.id == parent_id).first()
    if parent is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compte introuvable.")

    email = email.strip().lower()
    if email != parent.email:
        taken = db.query(Parent).filter(Parent.email == email, Parent.id != parent_id).first()
        if taken:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Un compte existe déjà avec cet email.",
            )
        parent.email = email

    parent.name = (name or "").strip() or None
    db.commit()
    db.refresh(parent)
    return parent


def register_parent(db: Session, req: RegisterRequest) -> TokenResponse:
    existing = db.query(Parent).filter(Parent.email == req.email).first()
    if existing:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un compte existe déjà avec cet email."
        )

    parent = Parent(
        email         = req.email,
        name          = req.name,
        password_hash = hash_password(req.password),
        phone         = req.phone,
        fcm_token     = req.fcm_token,
    )
    db.add(parent)
    db.commit()
    db.refresh(parent)

    # Génère et envoie le code de vérification (ou auto-vérifie si SMTP absent).
    _issue_verification(db, parent)

    token = create_access_token(parent.id)
    return TokenResponse(
        access_token=token,
        parent_id=parent.id,
        email_verified=bool(parent.email_verified),
        email=parent.email
    )


def login_parent(db: Session, req: LoginRequest) -> TokenResponse:
    from fastapi import HTTPException, status
    parent = db.query(Parent).filter(Parent.email == req.email).first()
    if not parent or not verify_password(req.password, parent.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect."
        )

    token = create_access_token(parent.id)
    return TokenResponse(
        access_token=token,
        parent_id=parent.id,
        email=parent.email,
        email_verified=bool(parent.email_verified),
    )
