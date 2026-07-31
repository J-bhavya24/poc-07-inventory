from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class Category(str, enum.Enum):
    grocery = "grocery"
    electronics = "electronics"
    clothing = "clothing"
    household = "household"
    personal_care = "personal_care"


class MovementType(str, enum.Enum):
    receipt = "receipt"
    sale = "sale"
    adjustment = "adjustment"
    transfer = "transfer"
    returnm = "return"


class POStatus(str, enum.Enum):
    draft = "draft"
    submitted = "submitted"
    acknowledged = "acknowledged"
    received = "received"
    cancelled = "cancelled"


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    supplier_code = Column(String(20), unique=True)
    contact_email = Column(String(200))
    payment_terms_days = Column(Integer, default=30)
    lead_time_days = Column(Integer, default=7)
    is_active = Column(Boolean, default=True)

    products = relationship("Product", back_populates="supplier")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(20), unique=True)
    name = Column(String(200), nullable=False)

    category = Column(Enum(Category))
    unit_price = Column(Float)
    cost_price = Column(Float)

    unit_of_measure = Column(String(20))
    reorder_point = Column(Integer, default=10)
    reorder_quantity = Column(Integer, default=50)

    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    created_at = Column(DateTime, server_default=func.now())

    supplier = relationship("Supplier", back_populates="products")


class StockLevel(Base):
    __tablename__ = "stock_levels"

    id = Column(Integer, primary_key=True)

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        unique=True
    )

    quantity_on_hand = Column(Integer, default=0)
    quantity_reserved = Column(Integer, default=0)

    @property
    def quantity_available(self):
        return max(
            0,
            self.quantity_on_hand - self.quantity_reserved
        )


class StockMovement(Base):
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True)

    product_id = Column(
        Integer,
        ForeignKey("products.id")
    )

    movement_type = Column(Enum(MovementType))
    quantity = Column(Integer)

    reference_number = Column(String(50))
    notes = Column(String(500))

    recorded_at = Column(
        DateTime,
        server_default=func.now()
    )

    recorded_by = Column(
        String(100),
        default="system"
    )


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True)

    po_number = Column(
        String(20),
        unique=True
    )

    supplier_id = Column(
        Integer,
        ForeignKey("suppliers.id")
    )

    status = Column(
        Enum(POStatus),
        default=POStatus.draft
    )

    total_amount = Column(Float, default=0.0)

    order_date = Column(Date)
    expected_delivery = Column(Date)
    received_date = Column(Date, nullable=True)


class POItem(Base):
    __tablename__ = "po_items"

    id = Column(Integer, primary_key=True)

    po_id = Column(
        Integer,
        ForeignKey("purchase_orders.id")
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id")
    )

    quantity_ordered = Column(Integer)
    unit_cost = Column(Float)

    quantity_received = Column(
        Integer,
        nullable=True
    )


class StockAlert(Base):
    __tablename__ = "stock_alerts"

    id = Column(Integer, primary_key=True)

    product_id = Column(
        Integer,
        ForeignKey("products.id")
    )

    alert_type = Column(String(50))
    message = Column(String(500))

    is_resolved = Column(
        Boolean,
        default=False
    )

    triggered_at = Column(
        DateTime,
        server_default=func.now()
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    email = Column(
        String(200),
        unique=True
    )

    hashed_password = Column(String(200))

    full_name = Column(String(100))

    role = Column(
        String(50),
        default="staff"
    )

    is_active = Column(
        Boolean,
        default=True
    )