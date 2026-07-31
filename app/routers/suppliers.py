from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Supplier, Product
from app.schemas import SupplierCreate

router = APIRouter(
    prefix="/api/v1/suppliers",
    tags=["Suppliers"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("")
def create_supplier(data: SupplierCreate, db: Session = Depends(get_db)):
    supplier = Supplier(
        name=data.name,
        supplier_code=data.supplier_code,
        contact_email=data.contact_email,
        payment_terms_days=data.payment_terms_days,
        lead_time_days=data.lead_time_days
    )

    db.add(supplier)
    db.commit()
    db.refresh(supplier)

    return supplier


@router.get("")
def get_suppliers(db: Session = Depends(get_db)):
    return db.query(Supplier).all()


@router.get("/{supplier_id}/catalog")
def supplier_catalog(
    supplier_id: int,
    db: Session = Depends(get_db)
):
    products = (
        db.query(Product)
        .filter(Product.supplier_id == supplier_id)
        .all()
    )

    return products