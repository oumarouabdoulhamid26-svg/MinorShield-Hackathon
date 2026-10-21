# app/services/notification_service.py
# Décide QUAND et À QUI envoyer un push, selon les préférences du parent.
# S'appuie sur push_service pour l'envoi effectif (FCM).

from datetime import datetime
from loguru import logger
from sqlalchemy.orm import Session

from app.models.db_models import Parent, Child, Detection
from app.services.push_service import send_push


_CATEGORY_LABELS = {
    "nudite":   "image à caractère sexuel",
    "violence": "contenu violent",
    "texte":    "texte inapproprié",
}


def notify_parent_of_detection(db: Session, child_id: str, category: str | None) -> None:
    """
    Alerte le parent qu'un contenu sensible a été détecté sur l'appareil de son
    enfant — si l'option "alerter sur chaque détection" est active.
    """
    child = db.query(Child).filter(Child.id == child_id).first()
    if child is None:
        return
    parent = db.query(Parent).filter(Parent.id == child.parent_id).first()
    if parent is None or not parent.fcm_token:
        return
    # notif_on_detection peut être None sur d'anciennes lignes → défaut activé.
    if parent.notif_on_detection is False:
        return

    reason = _CATEGORY_LABELS.get(category or "", "contenu inapproprié")
    send_push(
        parent.fcm_token,
        title = "MinorShield — Alerte",
        body  = f"{child.name} : {reason} détecté(e).",
    )


def send_daily_summaries(db: Session) -> None:
    """
    Envoie à chaque parent (option "résumé quotidien" active) un récapitulatif
    des contenus bloqués aujourd'hui, tous enfants confondus.
    """
    start_of_day = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    parents = db.query(Parent).filter(Parent.fcm_token.isnot(None)).all()

    for parent in parents:
        if parent.notif_daily_summary is False:
            continue

        child_ids = [c.id for c in db.query(Child).filter(Child.parent_id == parent.id).all()]
        if not child_ids:
            continue

        blocked = (
            db.query(Detection)
            .filter(
                Detection.child_id.in_(child_ids),
                Detection.label == "nsfw",
                Detection.timestamp >= start_of_day,
            )
            .count()
        )

        if blocked == 0:
            body = "Aucun contenu inapproprié détecté aujourd'hui. 👍"
        elif blocked == 1:
            body = "1 contenu inapproprié bloqué aujourd'hui."
        else:
            body = f"{blocked} contenus inapropriés bloqués aujourd'hui."

        send_push(parent.fcm_token, title="MinorShield — Résumé du jour", body=body)

    logger.info(f"Résumés quotidiens envoyés ({len(parents)} parent(s) évalué(s))")
