from pydantic import BaseModel
from typing import Optional, List


class SupplierCreate(BaseModel):
    name: str
    supplier_code: str
    contact_email: Optional[str] = None
    payment_terms_days: int = 30
    lead_time_days: int = 7


class ProductCreate(BaseModel):
    name: str
    category: str
    unit_price: float
    cost_price: float
    unit_of_measure: str
    reorder_point: int
    reorder_quantity: int
    supplier_id: int


class StockUpdateRequest(BaseModel):
    movement_type: str
    quantity: int
    reference_number: Optional[str] = None
    notes: Optional[str] = None


class POItemCreate(BaseModel):
    product_id: int
    quantity_ordered: int
    unit_cost: float


class PurchaseOrderCreate(BaseModel):
    supplier_id: int
    order_date: str
    expected_delivery: str
    items: List[POItemCreate]


class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str


class LoginRequest(BaseModel):
    email: str
    password: str

class StockUpdateRequest(BaseModel):
    movement_type: str
    quantity: int
    reference_number: Optional[str] = None
    notes: Optional[str] = None

class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str


class LoginRequest(BaseModel):
    email: str
    password: str