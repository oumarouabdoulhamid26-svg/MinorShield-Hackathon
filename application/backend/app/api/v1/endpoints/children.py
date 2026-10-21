
# app/api/v1/endpoints/children.py
# Endpoints : appairage, liste enfants, historique détections.

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth_jwt import get_current_parent_id
from app.core.security import verify_api_key
from app.schemas.children import (
    PairingRequest, PairingResponse,
    ChildRegisterRequest, ChildRegisterResponse,
    ChildListResponse, HeartbeatRequest,
    IncidentResponse, WarningLimitRequest, ChildUpdateRequest,
)
from app.schemas.auth import VerifyPinRequest, VerifyPinResponse
from app.schemas.history import DetectionHistoryResponse
from app.schemas.stats import ChildStatsResponse
from app.services.children_service import (
    create_pairing, register_child_device, list_children, delete_child,
    lock_child, unlock_child, get_lock_status, unpair_device, verify_child_pin,
    record_heartbeat, register_incident, set_warning_limit, reset_warnings,
    regenerate_pairing_code, disconnect_child_device, update_child,
)
from app.services.history_service import get_history
from app.services.stats_service import get_stats

router = APIRouter(prefix="/children", tags=["Enfants"])


# ── Endpoints parent (JWT) ────────────────────────────────────────────

@router.post(
    "/pair",
    response_model=PairingResponse,
    summary="Générer un code d'appairage pour un enfant",
    status_code=201,
)
def generate_pairing(
    req      : PairingRequest,
    parent_id: str = Depends(get_current_parent_id),
    db       : Session = Depends(get_db),
):
    return create_pairing(db, parent_id, req)


@router.get(
    "",
    response_model=ChildListResponse,
    summary="Lister tous les enfants du parent",
)
def get_children(
    parent_id: str = Depends(get_current_parent_id),
    db       : Session = Depends(get_db),
):
    return list_children(db, parent_id)


@router.get(
    "/{child_id}/detections",
    response_model=DetectionHistoryResponse,
    summary="Historique des détections d'un enfant",
)
def get_detections(
    child_id : str,
    page     : int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    parent_id: str = Depends(get_current_parent_id),
    db       : Session = Depends(get_db),
):
    return get_history(db, parent_id, child_id, page, page_size)


@router.put(
    "/{child_id}",
    summary="Modifier les réglages d'un enfant (âge, intensité, mots sensibles)",
    status_code=204,
)
def edit_child(
    child_id : str,
    req      : ChildUpdateRequest,
    parent_id: str = Depends(get_current_parent_id),
    db       : Session = Depends(get_db),
):
    update_child(db, parent_id, child_id, req.age, req.block_intensity, req.custom_keywords)


@router.delete(
    "/{child_id}",
    summary="Supprimer un enfant",
    status_code=204,
)
def remove_child(
    child_id : str,
    parent_id: str = Depends(get_current_parent_id),
    db       : Session = Depends(get_db),
):
    delete_child(db, parent_id, child_id)


@router.get(
    "/{child_id}/stats",
    response_model=ChildStatsResponse,
    summary="Statistiques agrégées d'un enfant (dashboard + graphiques)",
)
def get_child_stats(
    child_id : str,
    period   : str = Query("week", pattern="^(day|week|month)$"),
    parent_id: str = Depends(get_current_parent_id),
    db       : Session = Depends(get_db),
):
    return get_stats(db, parent_id, child_id, period)


# ── Déblocage à distance ──────────────────────────────────────────────

@router.post(
    "/{child_id}/unlock",
    summary="Débloquer l'overlay sur le téléphone de l'enfant",
    status_code=200,
)
def unlock_child_overlay(
    child_id : str,
    parent_id: str = Depends(get_current_parent_id),
    db       : Session = Depends(get_db),
):
    unlock_child(db, parent_id, child_id)
    return {"message": "Déblocage envoyé"}


@router.post(
    "/{child_id}/warning-limit",
    summary="Régler le nombre d'avertissements autorisés (parent)",
    status_code=204,
)
def update_warning_limit(
    child_id : str,
    req      : WarningLimitRequest,
    parent_id: str = Depends(get_current_parent_id),
    db       : Session = Depends(get_db),
):
    set_warning_limit(db, parent_id, child_id, req.limit)


@router.post(
    "/{child_id}/reset-warnings",
    summary="Remettre à zéro le compteur d'avertissements (parent)",
    status_code=200,
)
def reset_child_warnings(
    child_id : str,
    parent_id: str = Depends(get_current_parent_id),
    db       : Session = Depends(get_db),
):
    reset_warnings(db, parent_id, child_id)
    return {"message": "Avertissements réinitialisés"}


@router.post(
    "/{child_id}/regenerate-code",
    response_model=PairingResponse,
    summary="Générer un nouveau code d'appairage (parent)",
)
def regenerate_code(
    child_id : str,
    parent_id: str = Depends(get_current_parent_id),
    db       : Session = Depends(get_db),
):
    return regenerate_pairing_code(db, parent_id, child_id)


@router.post(
    "/{child_id}/disconnect",
    response_model=PairingResponse,
    summary="Déconnecter à distance l'appareil de l'enfant (parent)",
)
def disconnect_child(
    child_id : str,
    parent_id: str = Depends(get_current_parent_id),
    db       : Session = Depends(get_db),
):
    return disconnect_child_device(db, parent_id, child_id)


# ── Endpoints enfant (API Key) ────────────────────────────────────────

@router.post(
    "/{child_id}/lock",
    summary="Signaler un contenu bloqué (app enfant)",
    status_code=200,
)
def lock_child_overlay(
    child_id: str,
    db      : Session = Depends(get_db),
    api_key : str = Depends(verify_api_key),
):
    lock_child(db, child_id)
    return {"message": "Verrouillage enregistré"}


@router.post(
    "/{child_id}/incident",
    response_model=IncidentResponse,
    summary="Signaler un contenu sensible et faire avancer les avertissements (app enfant)",
)
def report_incident(
    child_id: str,
    db      : Session = Depends(get_db),
    api_key : str = Depends(verify_api_key),
):
    return register_incident(db, child_id)


@router.get(
    "/{child_id}/lock-status",
    summary="Vérifier si l'overlay doit être affiché (polling app enfant)",
)
def check_lock_status(
    child_id: str,
    db      : Session = Depends(get_db),
    api_key : str = Depends(verify_api_key),
):
    return get_lock_status(db, child_id)


@router.post(
    "/{child_id}/unpair",
    summary="Déconnecter cet appareil enfant (app enfant)",
    status_code=200,
)
def unpair_child_device(
    child_id: str,
    db      : Session = Depends(get_db),
    api_key : str = Depends(verify_api_key),
):
    unpair_device(db, child_id)
    return {"message": "Appareil déconnecté"}


@router.post(
    "/{child_id}/heartbeat",
    summary="Signaler l'état de la surveillance (app enfant)",
    description="Envoyé périodiquement par l'app enfant pour indiquer si la protection est opérationnelle.",
    status_code=204,
)
def child_heartbeat(
    child_id: str,
    req     : HeartbeatRequest,
    db      : Session = Depends(get_db),
    api_key : str = Depends(verify_api_key),
):
    record_heartbeat(
        db, child_id, req.protection_active,
        req.capture_active, req.overlay_allowed, req.usage_access,
    )


@router.post(
    "/{child_id}/verify-pin",
    response_model=VerifyPinResponse,
    summary="Vérifier le PIN parent avant déconnexion (app enfant)",
)
def verify_pin(
    child_id: str,
    req     : VerifyPinRequest,
    db      : Session = Depends(get_db),
    api_key : str = Depends(verify_api_key),
):
    return verify_child_pin(db, child_id, req.pin)


@router.post(
    "/register",
    response_model=ChildRegisterResponse,
    summary="Enregistrer l'appareil enfant via code d'appairage",
    description="Appelé par l'app enfant au premier lancement. Nécessite la clé API.",
)
def register_device(
    req    : ChildRegisterRequest,
    db     : Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    return register_child_device(db, req)
