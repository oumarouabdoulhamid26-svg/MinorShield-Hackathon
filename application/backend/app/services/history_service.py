
# app/services/history_service.py
# Sauvegarde et lecture de l'historique des détections par enfant.

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.db_models import Child, Detection
from app.schemas.history import DetectionHistoryResponse, DetectionItem


def save_detection(
    db          : Session,
    child_id    : str,
    request_id  : str,
    nsfw_score  : float,
    image_score : float,
    text_score  : float,
    label       : str,
    category    : str | None,
    extracted_text: str | None,
    app_package : str | None,
    app_name    : str | None = None,
) -> None:
    child = db.query(Child).filter(Child.id == child_id, Child.is_active == True).first()
    if child is None:
        return  # child_id inconnu → on ignore silencieusement

    detection = Detection(
        child_id       = child_id,
        request_id     = request_id,
        nsfw_score     = nsfw_score,
        image_score    = image_score,
        text_score     = text_score,
        label          = label,
        category       = category,
        extracted_text = extracted_text,
        app_package    = app_package,
        app_name       = app_name,
    )
    db.add(detection)
    db.commit()


def get_history(
    db        : Session,
    parent_id : str,
    child_id  : str,
    page      : int = 1,
    page_size : int = 50,
) -> DetectionHistoryResponse:
    child = db.query(Child).filter(Child.id == child_id, Child.parent_id == parent_id).first()
    if child is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enfant introuvable ou accès non autorisé."
        )

    # L'historique ne liste QUE les contenus sensibles (label == "nsfw").
    # Les contenus sains sont conservés en base pour les statistiques, mais
    # surchargeraient inutilement la liste.
    base = db.query(Detection).filter(
        Detection.child_id == child_id,
        Detection.label == "nsfw",
    )

    total = base.count()
    rows  = (
        base
        .order_by(Detection.timestamp.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    items = [
        DetectionItem(
            id             = r.id,
            request_id     = r.request_id,
            nsfw_score     = r.nsfw_score,
            image_score    = r.image_score,
            text_score     = r.text_score,
            label          = r.label,
            category       = r.category,
            extracted_text = r.extracted_text,
            app_package    = r.app_package,
            app_name       = r.app_name,
            timestamp      = r.timestamp.isoformat(),
        )
        for r in rows
    ]

    return DetectionHistoryResponse(
        child_id   = child_id,
        child_name = child.name,
        detections = items,
        total      = total,
        page       = page,
        page_size  = page_size,
    )
