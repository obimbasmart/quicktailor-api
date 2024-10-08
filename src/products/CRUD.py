from src.products.schemas import ProductUpload, CreateCustomCode
from sqlalchemy.orm import Session
from src.products.models.product import Product
from uuid import UUID
from typing import List
from src.products.models.product import Fabric, Category
from src.products.models.customization import Customization
from src.tailors.models import Tailor
from src.users.models import User
from exceptions import not_found_exception, access_denied_exception, bad_request_exception

def _create_product(product_data: ProductUpload, id: UUID, db: Session) -> Product:
    new_product = Product(**product_data.model_dump(exclude=["categories", "fabrics"]),
                          tailor_id=id)

    new_product.fabrics = get_fabric_objects(product_data.fabrics, db)
    new_product.categories = get_category_objects(product_data.categories, db)

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def get_product_by_ids(db: Session):
    return db.query(Product).all()


def get_product_by_id(id: str, db: Session):
    product = db.query(Product).filter(id == Product.id).one_or_none()
    if not product:
        raise not_found_exception('Product')
    return product


def _delete_product(id: str, tailor: Tailor, db: Session):
    product = db.query(Product).filter(id == Product.id).one_or_none()
    if not product:
        raise not_found_exception('product')

    if product.id not in [product.id for product in tailor.products]:
        raise access_denied_exception()

    try:
        db.delete(product)
        db.commit()
    except:
        raise bad_request_exception('Cannot delete: The product has dependent orders')
    
    return True


def _create_custom_code(product_id: str, tailor_id: str, req_body: CreateCustomCode, db: Session):
    user = db.query(User).filter(req_body.email == User.email).one_or_none()
    if not user:
        raise not_found_exception('customer')

    product = get_product_by_id(product_id, db)
    customCode = Customization(**req_body.model_dump(exclude=['customer_email']),
                               tailor_id=tailor_id,
                               product_id=product.id,
                               user_id=user.id)
    db.add(customCode)
    db.commit()
    return customCode.id[-8:]


def _update_product(product_id: str, req_body: ProductUpload, db: Session):
    product = get_product_by_id(product_id, db)
    if not product:
        raise not_found_exception('product')

    update_data = req_body.model_dump(
        exclude_unset=True, exclude=['fabrics', 'categories'])
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
