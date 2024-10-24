from fastapi import APIRouter, Depends
from src.tailors.dependencies import get_current_tailor
from src.auth.dependencies import get_current_user
from src.products.schemas import ProductUpload, ProductUpdate, ProductListItem, ProductItem, ProductTailorItem, CreateCustomCode
from src.auth.schemas import BaseResponse
from src.reviews.schemas import ReviewItem
from src.products.CRUD import get_product_by_ids, _create_product, get_product_by_id, _update_product, _delete_product, _create_custom_code
from dependencies import get_db
from typing import List
from fastapi.responses import JSONResponse
from responses import delete_success_response, create_success_response, update_success_response


router = APIRouter(
    prefix="/products",
    tags=["product"],
)


@router.post('', response_model=BaseResponse)
def create_product(req_body: ProductUpload,
                   tailor=Depends(get_current_tailor),
                   db=Depends(get_db)):
    new_product = _create_product(req_body, tailor.id, db)
    return create_success_response("Product", data={'id': new_product.id})


@router.get('', response_model=List[ProductListItem])
def get_products(current_user=Depends(get_current_user),
                 db=Depends(get_db)):
    products = get_product_by_ids(db)
    return products


@router.get('/{product_id}', response_model=ProductItem)
def get_product(product_id: str,
                current_user=Depends(get_current_user),
                db=Depends(get_db)):
    products = get_product_by_id(product_id, db)
    print(products.tailor)
    return products


@router.put('/{product_id}', response_model=BaseResponse)
def update_product(product_id: str,
                   req_body: ProductUpdate,
                   tailor=Depends(get_current_tailor),
                   db=Depends(get_db)):
    product = _update_product(product_id, req_body, db)
    return update_success_response('Product')


@router.delete('/{product_id}', response_model=BaseResponse)
def delete_product(product_id: str,
                   tailor=Depends(get_current_tailor),
                   db=Depends(get_db)):
    product = _delete_product(product_id, tailor, db)
    return delete_success_response('Product')

@router.get('/{product_id}/tailor', response_model=ProductTailorItem)
def get_product_tailor_info(product_id: str,
                            current_user=Depends(get_current_user),
                            db=Depends(get_db)):
    product = get_product_by_id(product_id, db)
    return product.tailor


@router.get('/{product_id}/reviews', response_model=List[ReviewItem])
def get_product_reviews(product_id: str,
                        current_user=Depends(get_current_user),
                        db=Depends(get_db)):
    product = get_product_by_id(product_id, db)
    return product.reviews


@router.post('/{product_id}/customization-code', response_model=None)
def create_custom_code(product_id: str,
                       req_body: CreateCustomCode,
                       tailor=Depends(get_current_tailor),
                       db=Depends(get_db)):
    code = _create_custom_code(product_id, tailor.id, req_body, db)
    return {"message": "success", "code": code}
