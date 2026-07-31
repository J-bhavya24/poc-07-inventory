import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import (
    Product,
    StockLevel,
    StockMovement,
    PurchaseOrder
)

from datetime import date


engine = create_engine(
    "sqlite:///:memory:"
)

TestingSessionLocal = sessionmaker(
    bind=engine
)

Base.metadata.create_all(bind=engine)


def test_sku_unique():
    db = TestingSessionLocal()

    p1 = Product(
        sku="SKU-GRO-9999",
        name="Test1"
    )

    db.add(p1)
    db.commit()

    with pytest.raises(Exception):
        p2 = Product(
            sku="SKU-GRO-9999",
            name="Test2"
        )

        db.add(p2)
        db.commit()


def test_stock_movement_link():
    m = StockMovement(
        product_id=1,
        movement_type="receipt",
        quantity=50
    )

    assert m.product_id == 1


def test_po_unique():
    db = TestingSessionLocal()

    po1 = PurchaseOrder(
        po_number="PO-2026-9999",
        supplier_id=1,
        order_date=date.today()
    )

    db.add(po1)
    db.commit()

    with pytest.raises(Exception):
        po2 = PurchaseOrder(
            po_number="PO-2026-9999",
            supplier_id=1,
            order_date=date.today()
        )

        db.add(po2)
        db.commit()


def test_stock_level_unique():
    db = TestingSessionLocal()

    s1 = StockLevel(
        product_id=100,
        quantity_on_hand=50
    )

    db.add(s1)
    db.commit()

    with pytest.raises(Exception):
        s2 = StockLevel(
            product_id=100,
            quantity_on_hand=30
        )

        db.add(s2)
        db.commit()