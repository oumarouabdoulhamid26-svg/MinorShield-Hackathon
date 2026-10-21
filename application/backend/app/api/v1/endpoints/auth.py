
# app/api/v1/endpoints/auth.py
# Endpoints d'authentification pour les comptes parent.

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth_jwt import get_current_parent, get_current_parent_id
from app.schemas.auth import (
    RegisterRequest, LoginRequest, TokenResponse, ParentResponse,
    SetPinRequest, VerifyPinRequest, VerifyPinResponse, UpdateFcmTokenRequest,
    NotificationPrefs, UpdateProfileRequest, VerifyEmailRequest,
)
from app.services.auth_service import (
    register_parent, login_parent, set_parent_pin, verify_parent_pin,
    update_fcm_token, update_notif_prefs, update_profile,
    verify_email, resend_verification,
)

router = APIRouter(prefix="/auth", tags=["Authentification"])


@router.post(
    "/register",
    response_model=TokenResponse,
    summary="Créer un compte parent",
    status_code=201,
)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    return register_parent(db, req)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Connexion compte parent",
)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    return login_parent(db, req)


@router.get(
    "/me",
    response_model=ParentResponse,
    summary="Profil du parent connecté",
)
def me(parent=Depends(get_current_parent)):
    return ParentResponse(
        id             = parent.id,
        email          = parent.email,
        name           = parent.name,
        phone          = parent.phone,
        created_at     = parent.created_at.isoformat(),
        pin_configured = bool(parent.pin_hash),
        email_verified = bool(parent.email_verified),
    )


@router.post(
    "/verify-email",
    summary="Vérifier l'adresse e-mail avec le code reçu",
    status_code=204,
)
def verify_email_endpoint(
    req      : VerifyEmailRequest,
    parent_id: str = Depends(get_current_parent_id),
    db       : Session = Depends(get_db),
):
    verify_email(db, parent_id, req.code)


@router.post(
    "/resend-code",
    summary="Renvoyer un code de vérification par e-mail",
    status_code=204,
)
def resend_code_endpoint(
    parent_id: str = Depends(get_current_parent_id),
    db       : Session = Depends(get_db),
):
    resend_verification(db, parent_id)


@router.put(
    "/me",
    response_model=ParentResponse,
    summary="Modifier le profil du parent (nom, email)",
)
def update_me(
    req      : UpdateProfileRequest,
    parent_id: str = Depends(get_current_parent_id),
    db       : Session = Depends(get_db),
):
    parent = update_profile(db, parent_id, req.name, req.email)
    return ParentResponse(
        id             = parent.id,
        email          = parent.email,
        name           = parent.name,
        phone          = parent.phone,
        created_at     = parent.created_at.isoformat(),
        pin_configured = bool(parent.pin_hash),
    )


@router.post(
    "/pin",
    summary="Définir ou changer le PIN parent",
    description="Le PIN est demandé à l'enfant avant toute déconnexion de son appareil.",
    status_code=204,
)
def set_pin(
    req      : SetPinRequest,
    parent_id: str = Depends(get_current_parent_id),
    db       : Session = Depends(get_db),
):
    set_parent_pin(db, parent_id, req.pin, req.current_pin)


@router.post(
    "/fcm-token",
    summary="Enregistrer le token FCM de l'appareil parent",
    status_code=204,
)
def set_fcm_token(
    req      : UpdateFcmTokenRequest,
    parent_id: str = Depends(get_current_parent_id),
    db       : Session = Depends(get_db),
):
    update_fcm_token(db, parent_id, req.fcm_token)


@router.get(
    "/notifications",
    response_model=NotificationPrefs,
    summary="Lire les préférences de notification du parent",
)
def get_notifications(parent=Depends(get_current_parent)):
    return NotificationPrefs(
        on_detection  = parent.notif_on_detection  is not False,
        daily_summary = parent.notif_daily_summary is not False,
    )


@router.put(
    "/notifications",
    summary="Mettre à jour les préférences de notification du parent",
    status_code=204,
)
def put_notifications(
    req      : NotificationPrefs,
    parent_id: str = Depends(get_current_parent_id),
    db       : Session = Depends(get_db),
):
    update_notif_prefs(db, parent_id, req.on_detection, req.daily_summary)


@router.post(
    "/verify-pin",
    response_model=VerifyPinResponse,
    summary="Vérifier le PIN parent (déverrouillage de l'app parent)",
)
def verify_pin(
    req      : VerifyPinRequest,
    parent_id: str = Depends(get_current_parent_id),
    db       : Session = Depends(get_db),
):
    return verify_parent_pin(db, parent_id, req.pin)
