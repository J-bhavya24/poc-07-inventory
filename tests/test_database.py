from app.models import (
    Product,
    StockLevel,
    PurchaseOrder
)


def test_product_model():
    p = Product()

    p.sku = "SKU-GRO-9999"

    assert p.sku == "SKU-GRO-9999"


def test_stock_level():
    s = StockLevel()

    s.quantity_on_hand = 100
    s.quantity_reserved = 20

    assert s.quantity_available == 80


def test_po_model():
    po = PurchaseOrder()

    po.po_number = "PO-2026-9999"

    assert po.po_number == "PO-2026-9999"