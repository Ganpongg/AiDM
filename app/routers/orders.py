from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Order, OrderItem, Product, OrderStatus
from app.schemas import OrderCreate, OrderOut
from app import auth_utils

router = APIRouter()

@router.post("/", response_model=OrderOut)
def create_order(order_in: OrderCreate, db: Session = Depends(get_db),
                 current_user=Depends(auth_utils.get_current_user)):
    total = 0.0
    items = []
    for item in order_in.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name}")
        product.stock -= item.quantity
        total += product.price * item.quantity
        items.append(OrderItem(product_id=product.id, quantity=item.quantity, unit_price=product.price))
    order = Order(user_id=current_user.id, shipping_address=order_in.shipping_address,
                  total_amount=total, items=items)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

@router.get("/", response_model=List[OrderOut])
def list_orders(db: Session = Depends(get_db),
                current_user=Depends(auth_utils.get_current_user)):
    return db.query(Order).filter(Order.user_id == current_user.id).all()

@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db),
              current_user=Depends(auth_utils.get_current_user)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.patch("/{order_id}/cancel", response_model=OrderOut)
def cancel_order(order_id: int, db: Session = Depends(get_db),
                 current_user=Depends(auth_utils.get_current_user)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status not in (OrderStatus.pending, OrderStatus.confirmed):
        raise HTTPException(status_code=400, detail="Cannot cancel order in current status")
    order.status = OrderStatus.cancelled
    for item in order.items:
        item.product.stock += item.quantity
    db.commit()
    db.refresh(order)
    return order
