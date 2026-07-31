from fastapi import FastAPI

from app.database import Base, engine
import app.models

from app.routers.products import router as products_router
from app.routers.suppliers import router as suppliers_router
from app.routers.stock import router as stock_router
from app.routers.purchase_orders import router as orders_router
from app.routers.dashboard import router as dashboard_router
from app.routers.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="POC-07 Inventory Management System"
)

app.include_router(products_router)
app.include_router(suppliers_router)


@app.get("/")
def home():
    return {
        "message": "POC-07 Inventory System Running"
    }

app.include_router(stock_router)
app.include_router(orders_router)
app.include_router(dashboard_router)
app.include_router(auth_router)