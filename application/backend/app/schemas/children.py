
# app/schemas/children.py

from pydantic import BaseModel
from typing import Optional


class PairingRequest(BaseModel):
    name: str
    age : Optional[int] = None


class PairingResponse(BaseModel):
    child_id    : str
    child_name  : str
    pairing_code: str
    expires_in  : int  # secondes


class ChildRegisterRequest(BaseModel):
    pairing_code    : str
    device_fcm_token: Optional[str] = None
    # Modèle de l'appareil, pour que le parent identifie le téléphone lié
    device_model    : Optional[str] = None


class ChildRegisterResponse(BaseModel):
    child_id  : str
    child_name: str
    parent_id : str


class IncidentResponse(BaseModel):
    status       : str   # "warning" | "blocked"
    warnings_used: int
    warning_limit: int
    remaining    : int


class WarningLimitRequest(BaseModel):
    limit: int


class ChildUpdateRequest(BaseModel):
    """Mise à jour des réglages d'un enfant (tous les champs optionnels)."""
    age            : Optional[int] = None
    block_intensity: Optional[str] = None   # "moyen" | "eleve" | "tres_eleve"
    custom_keywords: Optional[str] = None   # mots sensibles perso (un par ligne / virgules)


class HeartbeatRequest(BaseModel):
    # True si la capture d'écran ET l'overlay sont opérationnels sur l'appareil
    protection_active: bool
    # Détail par brique — permet de dire au parent CE QUI manque, plutôt qu'un
    # simple "inactif". Optionnels : une ancienne app enfant n'les envoie pas.
    capture_active   : Optional[bool] = None
    overlay_allowed  : Optional[bool] = None
    usage_access     : Optional[bool] = None


class ChildResponse(BaseModel):
    id              : str
    name            : str
    age             : Optional[int] = None
    is_active       : bool
    created_at      : str
    detections_count: int = 0
    last_detection  : Optional[str] = None
    # Surveillance réellement active sur l'appareil (False si permissions
    # révoquées, app fermée, ou aucun signal récent)
    protection_active: bool = False
    last_seen_at     : Optional[str] = None
    # Système d'avertissements
    warning_limit    : int = 3
    warnings_used    : int = 0
    # Code d'appairage : présent tant que l'appareil n'est pas lié (None après).
    pairing_code     : Optional[str] = None
    pairing_expires_at: Optional[str] = None
    # ── Fiche détaillée ──────────────────────────────────────────────
    device_model     : Optional[str] = None
    paired_at        : Optional[str] = None
    # complete | partial | degraded | inactive — calculé côté serveur
    protection_level : str = "inactive"
    is_locked        : bool = False
    # Réglages personnalisés par enfant
    block_intensity  : str = "eleve"
    custom_keywords  : Optional[str] = None

    class Config:
        from_attributes = True


class ChildListResponse(BaseModel):
    children: list[ChildResponse]
    total   : int
