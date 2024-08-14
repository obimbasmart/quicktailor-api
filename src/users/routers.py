from fastapi import APIRouter, Depends, HTTPException
from typing import List, Union
from pydantic import UUID4
from dependencies import get_db
from src.auth.schemas import BaseResponse
from src.users.CRUD import update_user, update_measurement, add_favorite
from src.users.dependencies import get_user_by_id, get_current_user
from src.users.utils import get_user_via_email, get_products, get_tailors
from src.users.schemas import (UserInfo, AddFavorite,  UpdateFields, FavoriteResponse,
                               SuccessMsg, FemaleMeasurementInfo,  MaleMeasurementInfo, MeasurementUpdate)
from src.tailors.dependencies import get_tailor_by_id
from src.products.schemas import ProductItem, TailorListInfo
from src.products.CRUD import _get_product
from src.reviews.schemas import UploadReview
from src.reviews.CRUD import create_new_review
from src.carts.CRUD import add_cart, remove_cart, get_cart
from src.carts.schemas import CartItems, AddCart, TailorInfo, ProductInfo
from src.orders.schemas import ProductItem, UserItem, UserOrderItem
from src.orders.dependencies import get_user_order
from src.orders.models import OrderStatus

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get('/{user_id}', response_model=UserInfo)
async def get_single_user(user_id: UUID4, current_user=Depends(get_current_user),
                          db=Depends(get_db), user=Depends(get_user_by_id)):
    if not user:
        raise HTTPException(
            status_code=404, detail="User not found with the id")
    return user


@router.put('/{user_id}', response_model=SuccessMsg)
async def update_user_route(req_body: UpdateFields,  user_id: str, current_user=Depends(get_current_user),
                            db=Depends(get_db)):
    verify_email = get_user_via_email(req_body.email, db)
    if current_user.email == req_body.email:
        raise HTTPException(
            status_code=422, detail="This is your present Email")
    if verify_email:
        raise HTTPException(status_code=422, detail="Email is Already in use")
    if current_user.id != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized request")

    update = update_user(user_id, req_body, db)
    return update


@router.get('/measurement/{user_id}', response_model=List[Union[MaleMeasurementInfo, FemaleMeasurementInfo]])
async def get_user_measurement(user_id: UUID4, current_user=Depends(get_current_user),
                               db=Depends(get_db), user=Depends(get_user_by_id)):
    if not user:
        raise HTTPException(
            status_code=404, detail="User not found with the id")
    formatted_measurements = []
    for measurement in user.measurement:
        if "measurement_type" in measurement and measurement['measurement_type'] == "MALE":
            formatted_measurements.append(MaleMeasurementInfo(**measurement))
        else:
            formatted_measurements.append(FemaleMeasurementInfo(**measurement))

    return formatted_measurements


@router.put('/measurement/{user_id}', response_model=Union[MaleMeasurementInfo, FemaleMeasurementInfo])
async def update_user_measurement(req_body: MeasurementUpdate,
                                  user_id: str,
                                  current_user=Depends(get_current_user),
                                  db=Depends(get_db), user=Depends(get_user_by_id)):
    if user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorized request")
    if not user:
        raise HTTPException(
            status_code=404, detail="User not found with the id")
    update = update_measurement(user_id, req_body, db)
    update = update_measurement(user_id, req_body, db)
    if update:
        if update['measurement_type'] == "MALE":
            return MaleMeasurementInfo(**update)
        else:
            return FemaleMeasurementInfo(**update)


@router.get('/favorites/{user_id}', response_model=FavoriteResponse)
async def get_user_favorite(
    user_id: str,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
    user=Depends(get_user_by_id)
):
    if user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorized request")
    if not user:
        raise HTTPException(
            status_code=404, detail="User not found with the id")

    tailors = []
    products = []
    if user.favorites.get('tailors'):
        tailors = get_tailors(user.favorites['tailors'], db)
    if user.favorites.get('products'):
        products = get_products(user.favorites['products'], db)

    return FavoriteResponse(
        tailors=tailors,
        products=products
    )


@router.put('/favorites/{user_id}', response_model=SuccessMsg)
def update_user_favorite(req_body: AddFavorite, user_id: str, current_user=Depends(get_current_user),
                         db=Depends(get_db), user=Depends(get_user_by_id)):
    if user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorized request")

    if req_body.tailor_id:
        if not get_tailor_by_id(req_body.tailor_id, db):
            raise HTTPException(status_code=404, detail="tailor_id not valid")
    if req_body.product_id:
        if not _get_product(req_body.product_id, db):
            raise HTTPException(status_code=404, detail="product_id not valid")
    if not user:
        raise HTTPException(
            status_code=404, detail="User not found with the id")
    update = add_favorite(user_id, req_body, db)
    if not update:
        raise HTTPException(status_code=500, detail="An Error has occured")

    return update


@router.get('/{user_id}/carts', response_model=List[CartItems])
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


@router.post('/{user_id}/carts', response_model=BaseResponse)
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


@router.delete('/{user_id}/carts/{cart_id}', response_model=BaseResponse)
async def delete_cart(cart_id: str, user_id: str,
                      current_user=Depends(get_current_user),
                      db=Depends(get_db)):

    # used to verify product_id before proceeding
    cart = get_cart(cart_id, db)
    if cart.user_id != current_user.id or user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorized request")

    if remove_cart(cart_id, db):
        return {"message": "Cart removed successfully"}

    raise HTTPException(status_code=501, detail="An unexepcted Error Occurred")




@router.get('/{user_id}/orders/{order_id}', response_model=UserOrderItem)
def get_current_user_order(user_id: str, order_id: str, current_user=Depends(get_current_user),
                           db=Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized request")
    order = get_user_order(order_id, user_id,  db)
    tailor = TailorListInfo(**order.tailor.__dict__)
    user = UserItem(**order.user.__dict__)
    product = ProductItem(
        **{**order.product.__dict__, "image": order.product.images[0]})
    user_order = UserOrderItem(
        **{**order.__dict__,
           "completion_date": order.created_at if order.status == OrderStatus.DELIVERED else None,
           "tailor": tailor,
           "product": product,
           "user": user})
    return user_order


@router.get('/{user_id}/orders', response_model=None)
def get_current_tailor_order(user_id: str, current_user=Depends(get_current_user),
                             db=Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized request")
    orders = [UserOrderItem(
        **{**order.__dict__,
           "completion_date": order.created_at if order.status == OrderStatus.DELIVERED else None,
           "tailor": TailorListInfo(**order.tailor.__dict__),
           "product": ProductItem(**{**order.product.__dict__, "image": order.product.images[0]}),
           "user": UserItem(**order.user.__dict__)
           }) for order in current_user.orders]

    return orders


@router.post('/{user_id}/orders/{order_id}/reviews', response_model=BaseResponse)
def create_review(req_body: UploadReview, user_id: str, order_id: str, current_user=Depends(get_current_user),
                  db=Depends(get_db),):
    order = get_user_order(order_id, user_id, db)
    if order.user_id != current_user.id or user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorized request")
    new_review = create_new_review(req_body, user_id, order_id, db)
    if not new_review:
        raise HTTPException(
            status_code=422, detail="you already submitted a review")
    return {"message": "Review submitted successfully"}
