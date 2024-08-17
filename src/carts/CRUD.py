from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
from typing import List
from src.carts.models import Cart
from src.carts.schemas import AddToCart
from src.products.CRUD import _get_product


def add_to_cart(req_body: AddToCart, user_id: str, db: Session):
    product = _get_product(req_body.product_id, db=db)

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Product Not found")

    new_cart_item = Cart(user_id=user_id,
                         measurement=req_body.measurements,
                         product_id=product.id)

    db.add(new_cart_item)
    db.commit()
    db.refresh(new_cart_item)
    return new_cart_item


def get_cart(id: str, db: Session) -> Cart:
    cart = db.query(Cart).filter(id == Cart.id).one_or_none()
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart Not found")
    return cart


def remove_cart(cart_id: str, db: Session):

    cart = db.query(Cart).filter(Cart.id == cart_id).one_or_none()
    db.delete(cart)
    db.commit()
    return True
