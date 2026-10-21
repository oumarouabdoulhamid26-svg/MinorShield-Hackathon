from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PaymentInitiateRequest(BaseModel):
    plan: str  # MONTHLY | ANNUAL


class PaymentInitiateResponse(BaseModel):
    widget_url     : str
    transaction_ref: str
    amount         : int
    currency       : str = "XAF"


class SubscriptionStatusResponse(BaseModel):
    is_active  : bool
    plan       : Optional[str]
    expires_at : Optional[datetime]
    days_remaining: int = 0
