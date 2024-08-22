from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.carts.models import CartItem
from src.carts.schemas import AddToCart
from src.products.CRUD import get_product_by_id
from src.users.models import User
from exceptions import not_found_exception
from typing import List


def add_to_cart(user: User, req_body: AddToCart,  db: Session):
    product = get_product_by_id(req_body.product_id, db=db)

    new_cart_item = CartItem(user_id=user.id,
                             measurements=req_body.measurements.model_dump(),
                             product_id=product.id)

    db.add(new_cart_item)
    db.commit()
    db.refresh(new_cart_item)
    return new_cart_item

def get_cart_item(id: str, db: Session) -> CartItem:
    cart = db.query(CartItem).filter(id == CartItem.id).one_or_none()
    if not cart:
        raise not_found_exception('Cart item')
    return cart


def delete_cart_item(cart_id: str, user: User, db: Session):

    cart_item = get_cart_item(cart_id, db)

    in_cart = cart_item.id in [item.id for item in user.cart]

    if not in_cart:
        raise not_found_exception('Cart item')
    
    db.delete(cart_item)
    db.commit()
    return True

def clear_items_in_cart(cart: List[str], db: Session):
    cart_items = [get_cart_item(item, db) for item in cart]
    
    [
        db.delete(item)
        for item in cart_items
    ]

    db.commit()
    return True
