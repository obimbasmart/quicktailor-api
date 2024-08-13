from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
from typing import List
from src.carts.models import Cart
from src.carts.schemas import AddCart


def add_cart(user_id: str, cart_data: AddCart, db: Session):
    check_product_in_cart = db.query(Cart).filter(Cart.product_id == cart_data.product_id).one_or_none()
    if check_product_in_cart:
        raise HTTPException(status_code=409, detail="Product alrady in cart")
    new_cart = Cart(user_id = user_id, measurement=[cart_data.measurements], product_id= cart_data.product_id)
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    return  True


def get_cart(id: str, db:Session)-> Cart:
    cart = db.query(Cart).filter(id == Cart.id).one_or_none()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart Not found")
    return cart

def remove_cart(cart_id: str, db: Session):

    cart = db.query(Cart).filter(Cart.id == cart_id).one_or_none()
    db.delete(cart)
    db.commit()
    return True



