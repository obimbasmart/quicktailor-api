from src.products.schemas import ProductUpload, CreateCustomCode
from sqlalchemy.orm import Session
from src.products.models.product import Product
from fastapi import HTTPException, status
from uuid import UUID
from typing import List
from src.products.models.product import Fabric, Category
from src.products.models.customization import CustomizationCode
from src.tailors.models import Tailor
from src.users.models import User


def _create_product(product_data: ProductUpload, id: UUID, db: Session) -> Product:
    new_product = Product(
        **product_data.model_dump(exclude=["categories", "fabrics"]), tailor_id=id)

    new_product.fabrics = get_fabric_objects(product_data.fabrics, db)
    new_product.categories = get_category_objects(product_data.categories, db)

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def _get_products(db: Session):
    return db.query(Product).all()


def _get_product(id: str, db: Session):
    product = db.query(Product).filter(id == Product.id).one_or_none()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Not found")
    return product


def _delete_product(id: str, tailor: Tailor, db: Session):
    product = db.query(Product).filter(id == Product.id).one_or_none()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Not found")


    if product.id not in [product.id for product in tailor.products]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    db.delete(product)
    db.commit()
    return True


def _create_custom_code(product_id: str, tailor_id: str, req_body: CreateCustomCode, db: Session):
    user = db.query(User).filter(req_body.email == User.email).one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer Not found")

    product = _get_product(product_id, db)
    customCode = CustomizationCode(
        **req_body.model_dump(exclude=['customer_email']), tailor_id=tailor_id, product_id=product.id, user_id=user.id)
    db.add(customCode)
    db.commit()
    return customCode.id[-8:]



def _update_product(product_id: str, req_body: ProductUpload, db: Session):
    product = _get_product(product_id, db)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Not found")

    update_data = req_body.model_dump(exclude_unset=True, exclude=['fabrics', 'categories'])
    [
        setattr(product, attr, val)
        for attr, val in update_data.items()
    ]

    if req_body.fabrics:
        product.fabrics += get_fabric_objects(req_body.fabrics, db)
    if req_body.categories:
        product.categories += get_category_objects(req_body.categories, db)

    db.commit()
    return product

def get_fabric_objects(names: List[str], db) -> List[Fabric]:
    fabric_objects = db.query(Fabric).filter(Fabric.name.in_(names)).all()
    return fabric_objects


def get_category_objects(names: List, db) -> List[Fabric]:
    category_objects = db.query(Category).filter(
        Category.name.in_(names)).all()
    return category_objects
