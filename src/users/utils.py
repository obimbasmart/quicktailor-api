from sqlalchemy.orm import Session
from fastapi import Depends, Body
from src.users.models import User
from src.tailors.dependencies import get_tailor_by_id
from src.tailors.schemas import  TailorListItem
from src.products.schemas import ProductItem
from src.products.CRUD import _get_product

def get_user_via_email(email: str, db: Session ) -> User:
    user = db.query(User).filter(email==User.email).one_or_none()
    return user

def get_tailors(tailors: list, db: Session):
    # Fetch tailor objects from the database
    tailors_get = [get_tailor_by_id(id, db) for id in tailors]

    # Convert each tailor object to a TailorListItem instance
    tailor_list = [TailorListItem(**tailor.__dict__) for tailor in tailors_get]


    return tailor_list

def get_products(products: list, db: Session):
    product_get = [_get_product(id, db) for id in products]

    product_list = [
    ProductItem(
        **{**product.__dict__, "fabrics": product.fabrics or [], "categories": product.categories or []}
    )
    for product in product_get
    ]

    return product_list

