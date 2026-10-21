from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.db_models import Subscription

PLAN_DURATIONS = {
    "MONTHLY": 30,
    "ANNUAL" : 365,
}

PLAN_AMOUNTS = {
    "MONTHLY": 1000,   # XAF
    "ANNUAL" : 10000,  # XAF
}


def get_or_create_subscription(db: Session, parent_id: str) -> Subscription:
    sub = db.query(Subscription).filter_by(parent_id=parent_id).first()
    if not sub:
        sub = Subscription(parent_id=parent_id, plan="MONTHLY", is_active=False)
        db.add(sub)
        db.commit()
        db.refresh(sub)
    return sub


def get_subscription_status(db: Session, parent_id: str) -> dict:
    sub = db.query(Subscription).filter_by(parent_id=parent_id).first()
    if not sub or not sub.is_active:
        return {"is_active": False, "plan": None, "expires_at": None, "days_remaining": 0}

    now  = datetime.utcnow()
    if sub.expires_at and sub.expires_at < now:
        sub.is_active = False
        db.commit()
        return {"is_active": False, "plan": None, "expires_at": None, "days_remaining": 0}

    days = (sub.expires_at - now).days if sub.expires_at else 0
    return {
        "is_active"    : True,
        "plan"         : sub.plan,
        "expires_at"   : sub.expires_at,
        "days_remaining": days,
    }


def activate_subscription(db: Session, parent_id: str, plan: str,
                           transaction_ref: str, transaction_id: str,
                           amount: int, phone: str) -> Subscription:
    sub = get_or_create_subscription(db, parent_id)
    days = PLAN_DURATIONS.get(plan, 30)

    sub.plan            = plan
    sub.transaction_ref = transaction_ref
    sub.transaction_id  = transaction_id
    sub.amount          = amount
    sub.phone           = phone
    sub.is_active       = True
    sub.expires_at      = datetime.utcnow() + timedelta(days=days)
    sub.updated_at      = datetime.utcnow()

    db.commit()
    db.refresh(sub)
    return sub


def find_subscription_by_ref(db: Session, ref: str):
    return db.query(Subscription).filter_by(transaction_ref=ref).first()
