from fastapi import FastAPI
from app.routers import orders, products, users, auth
from app.database import engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Order Service", version="1.0.0")
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
