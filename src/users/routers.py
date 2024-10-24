from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import UUID4
from dependencies import get_db
from src.auth.schemas import BaseResponse
from src.users.CRUD import _update_user, update_measurements, add_to_favorites, _update_user_password
from src.users.dependencies import get_user_by_id, get_current_user
from src.users.schemas import (UserInfo, AddFavorite,
                               UpdateUserFields, Favorites,
                               PasswordReset, SuccessMsg, MeasurementItem, MeasurementUpdate)
from src.reviews.schemas import UploadReview
from src.reviews.CRUD import create_new_review
from src.carts.CRUD import add_to_cart, delete_cart_item
from src.carts.schemas import CartItem, AddToCart
from src.orders.schemas import UserOrderItem, OrderListItem
from src.orders.dependencies import get_order_by_id
from utils import verify_resource_access
from responses import update_success_response, create_success_response
from exceptions import unauthorized_access_exception

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get('/{user_id}', response_model=UserInfo)
async def get_single_user(user_id: UUID4,
                          current_user=Depends(get_current_user),
                          db=Depends(get_db),
                          user=Depends(get_user_by_id)):

    verify_resource_access(user.id, current_user.id)
    return user


@router.put('/{user_id}', response_model=SuccessMsg)
async def update_user(req_body: UpdateUserFields,
                      user_id: UUID4,
                      current_user=Depends(get_current_user),
                      user=Depends(get_user_by_id),
                      db=Depends(get_db)):
    print(req_body)
    verify_resource_access(user.id, current_user.id)
    update = _update_user(current_user, req_body, db)
    return update_success_response('User')


@router.patch('/{user_id}/password')
def update_user_password(req_body: PasswordReset,
                         user_id: str,
                         db=Depends(get_db),
                         current_user=Depends(get_current_user),
                         user=Depends(get_user_by_id)):

    verify_resource_access(user.id, current_user.id)
    user = _update_user_password(user, req_body, db)
    return update_success_response('Password')


@router.get('/{user_id}/measurements', response_model=MeasurementItem)
async def get_user_measurements(user_id: UUID4,
                                current_user=Depends(get_current_user),
                                db=Depends(get_db),
                                user=Depends(get_user_by_id)):

    return user.measurements


@router.put('/{user_id}/measurements', response_model=None)
async def update_user_measurement(user_id: str,
                                  req_body: MeasurementUpdate,
                                  db=Depends(get_db),
                                  user=Depends(get_user_by_id),
                                  current_user=Depends(get_current_user)):

    verify_resource_access(user.id, current_user.id)
    user = update_measurements(user, req_body, db)
    return update_success_response('Measurements')


@router.get('/{user_id}/favorites', response_model=Favorites)
async def get_user_favorites(user_id: str,
                             current_user=Depends(get_current_user),
                             db=Depends(get_db),
                             user=Depends(get_user_by_id)):
    print(user.favorites)
    verify_resource_access(user.id, current_user.id)
    return user.favorites


@router.put('/{user_id}/favorites', response_model=SuccessMsg)
def update_user_favorite(req_body: AddFavorite,
                         user_id: str,
                         current_user=Depends(get_current_user),
                         db=Depends(get_db),
                         user=Depends(get_user_by_id)):

    verify_resource_access(user.id, current_user.id)
    favorite = add_to_favorites(user, req_body, db)
    return update_success_response('Favorites')


@router.get('/{user_id}/cart', response_model=List[CartItem])
async def get_user_cart(user_id: str,
                        db=Depends(get_db),
                        user=Depends(get_user_by_id),
                        current_user=Depends(get_current_user)):

    verify_resource_access(user.id, current_user.id)
    return current_user.cart


@router.post('/{user_id}/cart', response_model=BaseResponse)
async def add_new_cart(req_body: AddToCart,
                       user_id: str,
                       db=Depends(get_db),
                       current_user=Depends(get_current_user),
                       user=Depends(get_user_by_id)):

    verify_resource_access(user.id, current_user.id)
    cart_item = add_to_cart(user, req_body, db)
    return update_success_response("Cart")


@router.delete('/{user_id}/carts/{cart_id}', response_model=BaseResponse)
async def delete_cart(cart_id: str,
                      user_id: str,
                      user=Depends(get_user_by_id),
                      current_user=Depends(get_current_user),
                      db=Depends(get_db)):

    verify_resource_access(user.id, current_user.id)
    cart_item = delete_cart_item(cart_id, user, db)
    return update_success_response('Cart')


@router.get('/{user_id}/orders/{order_id}', response_model=UserOrderItem)
def get_current_user_order(user_id: str,
                           order_id: str,
                           current_user=Depends(get_current_user),
                           user=Depends(get_user_by_id),
                           order=Depends(get_order_by_id)):

    verify_resource_access(user.id, current_user.id)
    return order


@router.get('/{user_id}/orders', response_model=List[OrderListItem])
async def get_user_orders(user_id: str,
                          current_user=Depends(get_current_user),
                          user=Depends(get_user_by_id)):
    verify_resource_access(user.id, current_user.id)
    return current_user.orders


@router.post('/{user_id}/orders/{order_id}/reviews', response_model=BaseResponse)
def create_review(user_id: str,
                  order_id: str,
                  req_body: UploadReview,
                  user=Depends(get_user_by_id),
                  order=Depends(get_order_by_id),
                  current_user=Depends(get_current_user),
                  db=Depends(get_db)):

    verify_resource_access(user.id, current_user.id)

    if order.user_id != current_user.id:
        raise unauthorized_access_exception()

    review = create_new_review(user, order, req_body, db)
    return create_success_response('Review')
