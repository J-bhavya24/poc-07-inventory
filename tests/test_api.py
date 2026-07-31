import requests

BASE_URL = "http://127.0.0.1:8000"


def test_products():
    response = requests.get(
        f"{BASE_URL}/api/v1/products"
    )

    assert response.status_code == 200


def test_product_details():
    response = requests.get(
        f"{BASE_URL}/api/v1/products/1"
    )

    assert response.status_code == 200


def test_low_alerts():
    response = requests.get(
        f"{BASE_URL}/api/v1/stock/low-alerts"
    )

    assert response.status_code == 200


def test_supplier_catalog():
    response = requests.get(
        f"{BASE_URL}/api/v1/suppliers/1/catalog"
    )

    assert response.status_code == 200


def test_dashboard():
    response = requests.get(
        f"{BASE_URL}/api/v1/dashboard"
    )

    assert response.status_code == 200