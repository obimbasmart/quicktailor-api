from fastapi import APIRouter, Depends, status, HTTPException
from src.users.dependencies import get_current_user
from src.carts.schemas import CartItems, AddCart, TailorInfo, RemoveCart, ProductInfo
from src.auth.schemas import BaseResponse
from src.products.CRUD import _get_product
from dependencies import get_db
from src.carts.CRUD import add_cart, remove_cart, get_cart
from src.tailors.dependencies import get_tailor_by_id
from typing import List


router = APIRouter(
    prefix="/carts",
    tags=["carts"],
)


@router.get('/{user_id}', response_model=List[CartItems])
async def get_user_carts(user_id: str,
                         current_user=Depends(get_current_user),
                         db=Depends(get_db)):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=401, detail="Unauthorized arekar request")
    response = []
    if current_user.carts:
        response = ([CartItems(id=cart.id, tailor=TailorInfo(**cart.product.tailor.__dict__),
                               product=ProductInfo(**cart.product.__dict__)) for cart in current_user.carts])
    return response


@router.post('/{user_id}', response_model=BaseResponse)
async def add_new_cart(req_body: AddCart, user_id: str,
                       current_user=Depends(get_current_user),
                       db=Depends(get_db)):
    if user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorized request")

    # used to verify product_id before proceeding
    _get_product(req_body.product_id, db)

    if add_cart(user_id, req_body, db):
        return {"message": "Cart Added successfully"}

    raise HTTPException(status_code=501, detail="An unexepcted Error Occurred")


@router.delete('/{cart_id}', response_model=BaseResponse)
async def delete_cart(cart_id: str,
                      current_user=Depends(get_current_user),
                      db=Depends(get_db)):

    # used to verify product_id before proceeding
    cart = get_cart(cart_id, db)
    if cart.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorized request")

    if remove_cart(cart_id, db):
        return {"message": "Cart removed successfully"}

    raise HTTPException(status_code=501, detail="An unexepcted Error Occurred")
