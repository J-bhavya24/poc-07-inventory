from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import (
    Product,
    PurchaseOrder,
    StockAlert,
    StockLevel
)

router = APIRouter(
    prefix="/api/v1/dashboard",
    tags=["Dashboard"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("")
def dashboard(
    db: Session = Depends(get_db)
):
    total_products = (
        db.query(Product).count()
    )

    low_stock_count = (
        db.query(StockAlert)
        .filter(
            StockAlert.alert_type == "low_stock"
        )
        .count()
    )

    out_of_stock_count = (
        db.query(StockAlert)
        .filter(
            StockAlert.alert_type == "out_of_stock"
        )
        .count()
    )

    open_po_count = (
        db.query(PurchaseOrder)
        .count()
    )

    total_stock_value = 0

    products = (
        db.query(Product).all()
    )

    for product in products:

        stock = (
            db.query(StockLevel)
            .filter(
                StockLevel.product_id == product.id
            )
            .first()
        )

        if stock:
            total_stock_value += (
                stock.quantity_on_hand *
                product.cost_price
            )

    return {
        "total_products": total_products,
        "low_stock_count": low_stock_count,
        "out_of_stock_count": out_of_stock_count,
        "open_po_count": open_po_count,
        "total_stock_value": total_stock_value
    }