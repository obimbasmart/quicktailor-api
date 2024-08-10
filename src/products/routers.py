from fastapi import APIRouter, Depends
from src.tailors.dependencies import get_current_tailor
from src.auth.dependencies import get_current_user
from src.products.schemas import ProductUpload, ProductUpdate, ProductListItem, ProductItem, ProductTailorItem, CreateCustomCode
from src.auth.schemas import BaseResponse
from src.products.CRUD import _get_products, _create_product, _get_product, _update_product, _delete_product, _create_custom_code
from dependencies import get_db
from typing import List
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/products",
    tags=["product"],
)


@router.post('', response_model=BaseResponse)
def create_product(req_body: ProductUpload,
                   tailor=Depends(get_current_tailor),
                   db=Depends(get_db)):
    new_product = _create_product(req_body, tailor.id, db)
    return JSONResponse(status_code=201, content={'message': 'success', "id": new_product.id})


@router.get('', response_model=List[ProductListItem])
def get_products(current_user=Depends(get_current_user),
                 db=Depends(get_db)):
    products = _get_products(db)
    return products


@router.get('/{product_id}', response_model=ProductItem)
def get_product(product_id: str,
                current_user=Depends(get_current_user),
                db=Depends(get_db)):
    products = _get_product(product_id, db)
    return products


@router.put('/{product_id}', response_model=BaseResponse)
def delete_product(product_id: str,
                   req_body: ProductUpdate,
                   tailor=Depends(get_current_tailor),
                   db=Depends(get_db)):
    product = _update_product(product_id, req_body, db)
    return {"message": "Update successfull"}


@router.delete('/{product_id}', response_model=BaseResponse)
def delete_product(product_id: str,
                   tailor=Depends(get_current_tailor),
                   db=Depends(get_db)):
    product = _delete_product(product_id, tailor, db)
    return {"message": "Product deleted successfully"}


@router.get('/{product_id}/tailor', response_model=ProductTailorItem)
def get_product_tailor_info(product_id: str,
                            current_user=Depends(get_current_user),
                            db=Depends(get_db)):
    product = _get_product(product_id, db)
    return product.tailor


# TODO: Complete
@router.get('/{product_id}/reviews', response_model=None)
def get_product_reviews(product_id: str,
                        current_user=Depends(get_current_user),
                        db=Depends(get_db)):
    product = _get_product(product_id, db)
    # return product.reviews
    return {"message": "This is it sucess"}


@router.post('/{product_id}/customization-code', response_model=None)
def create_custom_code(product_id: str,
                       req_body: CreateCustomCode,
                       tailor=Depends(get_current_tailor),
                       db=Depends(get_db)):
    code = _create_custom_code(product_id, tailor.id, req_body, db)
    return {"message": "success", "code": code}
