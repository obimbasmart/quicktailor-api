from sqlalchemy.orm import Session
from fastapi import Depends, Body, HTTPException
from dependencies import get_db
from src.users.models import User
from src.users.dependencies import get_current_user
from src.tailors.dependencies import get_current_tailor
from src.orders.models import Order

def get_tailor_order(order_id: str, tailor_id:str,  db: Session):
   
    order = db.query(Order).filter(order_id==Order.id, Order.tailor_id == tailor_id).one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="order not found")
    return order

def get_user_order(order_id: str, user_id: str, db: Session):
    
    order = db.query(Order).filter(order_id==Order.id, Order.user_id == user_id ).one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="order not found")
    return order

