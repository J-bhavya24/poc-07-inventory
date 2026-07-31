from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Product, StockLevel
from app.schemas import ProductCreate
from app.services.inventory_service import generate_sku

from app.models import (
    Product,
    StockLevel,
    StockMovement
)

from app.schemas import (
    ProductCreate,
    StockUpdateRequest
)

from app.services.inventory_service import (
    generate_sku,
    check_stock_alerts
)

router = APIRouter(
    prefix="/api/v1/products",
    tags=["Products"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", status_code=201)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db)
):
    sku = generate_sku(data.category, db)

    product = Product(
        sku=sku,
        name=data.name,
        category=data.category,
        unit_price=data.unit_price,
        cost_price=data.cost_price,
        unit_of_measure=data.unit_of_measure,
        reorder_point=data.reorder_point,
        reorder_quantity=data.reorder_quantity,
        supplier_id=data.supplier_id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    stock = StockLevel(
        product_id=product.id,
        quantity_on_hand=0,
        quantity_reserved=0
    )

    db.add(stock)
    db.commit()

    return {
        "id": product.id,
        "sku": product.sku,
        "name": product.name,
        "category": product.category,
        "unit_price": product.unit_price,
        "cost_price": product.cost_price,
        "unit_of_measure": product.unit_of_measure,
        "reorder_point": product.reorder_point,
        "reorder_quantity": product.reorder_quantity,
        "supplier_id": product.supplier_id
    }


@router.get("")
def get_products(
    category: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product)

    if category:
        query = query.filter(Product.category == category)

    products = query.all()

    result = []

    for product in products:
        result.append({
            "id": product.id,
            "sku": product.sku,
            "name": product.name,
            "category": product.category,
            "unit_price": product.unit_price,
            "cost_price": product.cost_price,
            "supplier_id": product.supplier_id
        })

    return result


@router.get("/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    stock = (
        db.query(StockLevel)
        .filter(
            StockLevel.product_id == product_id
        )
        .first()
    )

    return {
        "id": product.id,
        "sku": product.sku,
        "name": product.name,
        "category": product.category,
        "unit_price": product.unit_price,
        "cost_price": product.cost_price,
        "stock_level": {
            "quantity_on_hand": stock.quantity_on_hand if stock else 0,
            "quantity_reserved": stock.quantity_reserved if stock else 0
        }
    }

@router.patch("/{product_id}/stock")
def update_stock(
    product_id: int,
    data: StockUpdateRequest,
    db: Session = Depends(get_db)
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    stock = (
        db.query(StockLevel)
        .filter(
            StockLevel.product_id == product_id
        )
        .first()
    )

    if not stock:
        stock = StockLevel(
            product_id=product_id,
            quantity_on_hand=0,
            quantity_reserved=0
        )

        db.add(stock)
        db.commit()
        db.refresh(stock)

    stock.quantity_on_hand += data.quantity

    movement = StockMovement(
        product_id=product_id,
        movement_type=data.movement_type,
        quantity=data.quantity,
        reference_number=data.reference_number,
        notes=data.notes
    )

    db.add(movement)

    check_stock_alerts(
        product,
        stock,
        db
    )

    db.commit()

    return {
        "message": "Stock updated",
        "product_id": product_id,
        "quantity_on_hand": stock.quantity_on_hand
    }