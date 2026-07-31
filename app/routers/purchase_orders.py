from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import SessionLocal

from app.models import (
    PurchaseOrder,
    POItem,
    StockLevel,
    StockMovement
)

from app.schemas import PurchaseOrderCreate

from app.services.inventory_service import (
    generate_po_number
)

router = APIRouter(
    prefix="/api/v1/orders",
    tags=["Purchase Orders"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", status_code=201)
def create_order(
    data: PurchaseOrderCreate,
    db: Session = Depends(get_db)
):
    po_number = generate_po_number(db)

    po = PurchaseOrder(
        po_number=po_number,
        supplier_id=data.supplier_id,
        status="draft",
        total_amount=0,
        order_date=datetime.strptime(
            data.order_date,
            "%Y-%m-%d"
        ).date(),
        expected_delivery=datetime.strptime(
            data.expected_delivery,
            "%Y-%m-%d"
        ).date()
    )

    db.add(po)
    db.commit()
    db.refresh(po)

    total_amount = 0

    for item in data.items:

        po_item = POItem(
            po_id=po.id,
            product_id=item.product_id,
            quantity_ordered=item.quantity_ordered,
            quantity_received=0,
            unit_cost=item.unit_cost
        )

        db.add(po_item)

        total_amount += (
            item.quantity_ordered *
            item.unit_cost
        )

    po.total_amount = total_amount

    db.commit()

    return {
        "id": po.id,
        "po_number": po.po_number,
        "status": po.status,
        "total_amount": po.total_amount
    }


@router.get("")
def get_orders(
    db: Session = Depends(get_db)
):
    orders = db.query(
        PurchaseOrder
    ).all()

    result = []

    for order in orders:
        result.append({
            "id": order.id,
            "po_number": order.po_number,
            "supplier_id": order.supplier_id,
            "status": order.status,
            "total_amount": order.total_amount
        })

    return result


@router.get("/{order_id}")
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    po = (
        db.query(PurchaseOrder)
        .filter(
            PurchaseOrder.id == order_id
        )
        .first()
    )

    if not po:
        return {
            "message": "Order not found"
        }

    items = (
        db.query(POItem)
        .filter(
            POItem.po_id == po.id
        )
        .all()
    )

    item_list = []

    for item in items:
        item_list.append({
            "id": item.id,
            "product_id": item.product_id,
            "quantity_ordered": item.quantity_ordered,
            "quantity_received": item.quantity_received,
            "unit_cost": item.unit_cost
        })

    return {
        "id": po.id,
        "po_number": po.po_number,
        "supplier_id": po.supplier_id,
        "status": po.status,
        "total_amount": po.total_amount,
        "items": item_list
    }


@router.patch("/{order_id}/receive")
def receive_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    po = (
        db.query(PurchaseOrder)
        .filter(
            PurchaseOrder.id == order_id
        )
        .first()
    )

    if not po:
        return {
            "message": "Order not found"
        }

    po_items = (
        db.query(POItem)
        .filter(
            POItem.po_id == po.id
        )
        .all()
    )

    for item in po_items:

        stock = (
            db.query(StockLevel)
            .filter(
                StockLevel.product_id ==
                item.product_id
            )
            .first()
        )

        if stock:
            stock.quantity_on_hand += (
                item.quantity_ordered
            )

        movement = StockMovement(
            product_id=item.product_id,
            movement_type="receipt",
            quantity=item.quantity_ordered,
            reference_number=po.po_number,
            notes="Purchase Order Received"
        )

        db.add(movement)

        item.quantity_received = (
            item.quantity_ordered
        )

    po.status = "received"

    db.commit()

    return {
        "message": "Purchase order received",
        "order_id": po.id,
        "status": po.status
    }