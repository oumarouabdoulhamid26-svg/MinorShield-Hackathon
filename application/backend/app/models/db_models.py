
# app/models/db_models.py
# Modèles SQLAlchemy : Parent, Child, Detection.

import uuid
from datetime import datetime

from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


def _uuid():
    return str(uuid.uuid4())


class Parent(Base):
    __tablename__ = "parents"

    id            = Column(String, primary_key=True, default=_uuid)
    email         = Column(String, unique=True, nullable=False, index=True)
    name          = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)
    pin_hash      = Column(String, nullable=True)
    phone         = Column(String, nullable=True)
    fcm_token     = Column(String, nullable=True)
    # Préférences de notification (pilotées par les interrupteurs des Réglages).
    notif_on_detection  = Column(Boolean, default=True)
    notif_daily_summary = Column(Boolean, default=True)
    # Vérification de l'adresse e-mail (code à 6 chiffres envoyé par e-mail).
    email_verified          = Column(Boolean, default=False)
    verification_code       = Column(String, nullable=True)
    verification_expires_at = Column(DateTime, nullable=True)
    created_at    = Column(DateTime, default=datetime.utcnow)

    children = relationship("Child", back_populates="parent", cascade="all, delete-orphan")


class Child(Base):
    __tablename__ = "children"

    id                 = Column(String, primary_key=True, default=_uuid)
    parent_id          = Column(String, ForeignKey("parents.id"), nullable=False, index=True)
    name               = Column(String, nullable=False)
    age                = Column(Integer, nullable=True)
    # Mots/textes supplémentaires jugés sensibles par CE parent, pour CET enfant
    # uniquement (un par ligne ou séparés par des virgules).
    custom_keywords    = Column(Text, nullable=True)
    # Intensité de blocage adaptée à l'âge : "moyen" | "eleve" | "tres_eleve".
    # Plus l'intensité est haute, plus le seuil de détection est bas (bloque plus tôt).
    block_intensity    = Column(String, default="eleve")
    pairing_code       = Column(String, nullable=True, index=True)
    pairing_expires_at = Column(DateTime, nullable=True)
    device_fcm_token   = Column(String, nullable=True)
    # Modèle de l'appareil ("Xiaomi 25028RN03A"), envoyé lors de la liaison
    device_model       = Column(String, nullable=True)
    # Date de liaison effective de l'appareil (≠ created_at, qui est la date
    # de génération du code d'appairage)
    paired_at          = Column(DateTime, nullable=True)
    is_active          = Column(Boolean, default=True)
    # Blocage TOTAL (quota d'avertissements épuisé) : seul le parent débloque.
    is_locked          = Column(Boolean, default=False)
    # ── Système d'avertissements progressif ──────────────────────────
    # Nombre d'avertissements autorisés avant blocage total (réglé par le parent).
    warning_limit      = Column(Integer, default=3)
    # Avertissements consommés depuis le dernier reset.
    warnings_used      = Column(Integer, default=0)
    # Date (YYYY-MM-DD) du dernier reset, pour la remise à zéro quotidienne.
    warnings_reset_day = Column(String, nullable=True)
    # Surveillance réellement opérationnelle sur l'appareil (capture + overlay
    # autorisés). Rafraîchi par le heartbeat de l'app enfant.
    protection_active  = Column(Boolean, default=False)
    # Détail des briques, pour distinguer une protection complète d'une
    # protection partielle plutôt qu'un simple booléen.
    capture_active     = Column(Boolean, default=False)
    overlay_allowed    = Column(Boolean, default=False)
    usage_access       = Column(Boolean, default=False)
    last_seen_at       = Column(DateTime, nullable=True)
    created_at         = Column(DateTime, default=datetime.utcnow)

    parent     = relationship("Parent", back_populates="children")
    detections = relationship("Detection", back_populates="child", cascade="all, delete-orphan")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id              = Column(String, primary_key=True, default=_uuid)
    parent_id       = Column(String, ForeignKey("parents.id"), nullable=False, index=True, unique=True)
    plan            = Column(String, nullable=False)          # MONTHLY | ANNUAL
    transaction_ref = Column(String, nullable=True, index=True)
    transaction_id  = Column(String, nullable=True)
    amount          = Column(Integer, nullable=True)
    phone           = Column(String, nullable=True)
    is_active       = Column(Boolean, default=False)
    expires_at      = Column(DateTime, nullable=True)
    created_at      = Column(DateTime, default=datetime.utcnow)
    updated_at      = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    parent = relationship("Parent", backref="subscription")


class Detection(Base):
    __tablename__ = "detections"

    id             = Column(Integer, primary_key=True, autoincrement=True)
    child_id       = Column(String, ForeignKey("children.id"), nullable=False, index=True)
    request_id     = Column(String, nullable=False)
    nsfw_score     = Column(Float, nullable=False)
    image_score    = Column(Float, nullable=False)
    text_score     = Column(Float, nullable=False)
    label          = Column(String, nullable=False)
    category       = Column(String, nullable=True)
    extracted_text = Column(Text, nullable=True)
    app_package    = Column(String, nullable=True)
    # Nom lisible de l'app ("WhatsApp"), résolu sur l'appareil enfant : le
    # parent ne peut pas le déduire, ces apps ne sont pas installées chez lui.
    app_name       = Column(String, nullable=True)
    timestamp      = Column(DateTime, default=datetime.utcnow, index=True)

    child = relationship("Child", back_populates="detections")
