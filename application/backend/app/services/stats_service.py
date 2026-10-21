
# app/services/stats_service.py
# Calcule les statistiques agrégées des détections d'un enfant.
# Utilisé par le dashboard et les graphiques de l'app parent.

from datetime import datetime, timedelta
from collections import Counter

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.db_models import Child, Detection
from app.schemas.stats import ChildStatsResponse, AppStat, DayStat


def _period_start(period: str) -> datetime:
    now = datetime.utcnow()
    if period == "day":
        return now.replace(hour=0, minute=0, second=0, microsecond=0)
    if period == "week":
        return (now - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
    # month
    return (now - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0)


def get_stats(
    db       : Session,
    parent_id: str,
    child_id : str,
    period   : str = "week",
) -> ChildStatsResponse:
    if period not in ("day", "week", "month"):
        raise HTTPException(status_code=400, detail="period doit être day, week ou month.")

    child = db.query(Child).filter(Child.id == child_id, Child.parent_id == parent_id).first()
    if child is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enfant introuvable ou accès non autorisé."
        )

    since = _period_start(period)
    # Statistiques sur le CONTENU INAPPROPRIÉ uniquement (label == "nsfw") :
    # le contenu sain n'est ni conservé ni comptabilisé.
    rows  = (
        db.query(Detection)
        .filter(
            Detection.child_id == child_id,
            Detection.timestamp >= since,
            Detection.label == "nsfw",
        )
        .all()
    )

    total   = len(rows)
    blocked = total
    ignored = 0
    efficacy_pct = 100.0 if total > 0 else 0.0

    # ── Applications concernées ──────────────────────────────────────
    # Uniquement les apps où un contenu SENSIBLE (nsfw) a été détecté — c'est
    # ce qui intéresse le parent, pas le temps d'écran anodin. On exclut les
    # détections sans app identifiée (non attribuables). Triées par fréquence.
    app_counts: Counter = Counter()
    for r in rows:
        if r.label != "nsfw":
            continue
        label = (r.app_name or "").strip()
        if not label:
            continue  # app non identifiée : inutile de l'afficher
        app_counts[(label, r.app_package or "")] += 1

    attributed = sum(app_counts.values())
    by_app = [
        AppStat(
            app_package = pkg,
            app_name    = label,
            count       = cnt,
            percentage  = round(cnt / attributed * 100, 1) if attributed > 0 else 0.0,
        )
        for (label, pkg), cnt in app_counts.most_common(10)
    ]

    # ── Détections par jour (graphique barres) ────────────────────────
    day_counts: dict[str, int] = {}
    for r in rows:
        day = r.timestamp.strftime("%Y-%m-%d")
        day_counts[day] = day_counts.get(day, 0) + 1

    # Remplir les jours sans détection avec 0
    num_days = {"day": 1, "week": 7, "month": 30}[period]
    by_day = []
    for i in range(num_days - 1, -1, -1):
        day = (datetime.utcnow() - timedelta(days=i)).strftime("%Y-%m-%d")
        by_day.append(DayStat(date=day, count=day_counts.get(day, 0)))

    return ChildStatsResponse(
        child_id     = child_id,
        child_name   = child.name,
        period       = period,
        total        = total,
        blocked      = blocked,
        ignored      = ignored,
        efficacy_pct = efficacy_pct,
        by_app       = by_app,
        by_day       = by_day,
    )
