from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import StockAlert

router = APIRouter(
    prefix="/api/v1/stock",
    tags=["Stock"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/low-alerts")
def get_low_alerts(
    db: Session = Depends(get_db)
):
    alerts = (
        db.query(StockAlert)
        .filter(
            StockAlert.is_resolved == False
        )
        .all()
    )

    result = []

    for alert in alerts:
        result.append({
            "id": alert.id,
            "product_id": alert.product_id,
            "alert_type": alert.alert_type,
            "message": alert.message,
            "is_resolved": alert.is_resolved
        })

    return result