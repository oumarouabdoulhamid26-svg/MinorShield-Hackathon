
# app/schemas/stats.py

from pydantic import BaseModel
from typing import Optional


class AppStat(BaseModel):
    app_package: str
    # Nom lisible à afficher au parent ("WhatsApp"). Jamais le package technique.
    app_name   : str
    count      : int
    percentage : float


class DayStat(BaseModel):
    date : str  # YYYY-MM-DD
    count: int


class ChildStatsResponse(BaseModel):
    child_id       : str
    child_name     : str
    period         : str        # day | week | month
    total          : int
    blocked        : int
    ignored        : int
    efficacy_pct   : float      # blocked / total * 100
    by_app         : list[AppStat]
    by_day         : list[DayStat]
