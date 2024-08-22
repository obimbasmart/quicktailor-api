from sqlalchemy.orm import Session
from src.orders.models import Order
from exceptions import not_found_exception
from fastapi import Depends
from dependencies import get_db


def get_order_by_id(order_id: str, db: Session = Depends(get_db)):
    
    order = db.query(Order).filter(order_id==Order.id).one_or_none()
    if not order:
        raise not_found_exception('Order')
    return order
