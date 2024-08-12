from fastapi import APIRouter, Depends, HTTPException
from src.tailors.dependencies import get_current_tailor
from src.users.dependencies import get_current_user as current_user
from src.products.schemas import TailorListInfo
from src.auth.schemas import BaseResponse
from src.products.CRUD import  _get_product
from dependencies import get_db
from typing import List
from fastapi.responses import JSONResponse
from src.orders.schemas import (OrderItem, ProductItem,
        UserItem, UserOrderItem)
from src.orders.CRUD import create_new_order
from src.orders.dependencies import get_tailor_order, get_user_order
from src.orders.models import OrderStatus
router = APIRouter(
    prefix="/orders",
    tags=["order"],
)


@router.post('', response_model=BaseResponse)
def create_order(req_body: OrderItem,
                   user=Depends(current_user),
                   db=Depends(get_db)):
    product = _get_product(req_body.product_id, db)
    new_order = create_new_order(user.id, product.tailor_id, req_body, db)
    return JSONResponse(status_code=201, content={'message': 'success', "id": new_order.id})



@router.get('/{order_id}/users/{user_id}', response_model=UserOrderItem)
def get_current_user_order(user_id: str, order_id: str, user=Depends(current_user),
                   db=Depends(get_db)):
    print("do user heerer let's see debug", user)
    if user.id !=  user_id:
        raise HTTPException(status_code=401, detail="Unauthorized request")
    order = get_user_order(order_id, user_id,  db)
    tailor = TailorListInfo(**order.tailor.__dict__)
    user = UserItem(**order.user.__dict__)
    product = ProductItem(**{**order.product.__dict__, "image":order.product.images[0]})
    user_order = UserOrderItem(
        **{**order.__dict__,
        "completion_date": order.created_at if order.status == OrderStatus.DELIVERED  else None,
        "tailor": tailor,
        "product": product,
        "user":user})
    return user_order

@router.get('/{order_id}/tailors/{tailor_id}', response_model=UserOrderItem)
def get_current_tailor_order(tailor_id: str, order_id: str, tailor=Depends(get_current_tailor),
                   db=Depends(get_db)):
    if tailor.id != tailor_id:
        raise HTTPException(status_code=401, detail="Unauthorized request")
    order = get_tailor_order(order_id, tailor_id,  db)
    tailor = TailorListInfo(**order.tailor.__dict__)
    user = UserItem(**order.user.__dict__)
    product = ProductItem(**{**order.product.__dict__, "image":order.product.images[0]})
    tailor_order = UserOrderItem(
        **{**order.__dict__,
        "completion_date": order.created_at if order.status == OrderStatus.DELIVERED  else None,
        "tailor": tailor,
        "product": product,
        "user":user})
    return tailor_order

@router.get('/tailors/{tailor_id}', response_model=List[UserOrderItem])
def get_current_tailor_order(tailor_id: str, tailor=Depends(get_current_tailor),
                   db=Depends(get_db)):
    if tailor.id != tailor_id:
        raise HTTPException(status_code=401, detail="Unauthorized request")
    orders = [UserOrderItem(
        **{**order.__dict__,
        "completion_date": order.created_at if order.status == OrderStatus.DELIVERED  else None,
        "tailor": TailorListInfo(**order.tailor.__dict__),
        "product": ProductItem(**{**order.product.__dict__, "image":order.product.images[0]}),
        "user": UserItem(**order.user.__dict__)
    }) for order in tailor.orders]

    return orders

@router.get('/users/{user_id}', response_model=List[UserOrderItem])
def get_current_tailor_order(user_id: str, user=Depends(current_user),
                   db=Depends(get_db)):
    if user.id != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized request")
    orders = [UserOrderItem(
        **{**order.__dict__,
        "completion_date": order.created_at if order.status == OrderStatus.DELIVERED  else None,
        "tailor": TailorListInfo(**order.tailor.__dict__),
        "product": ProductItem(**{**order.product.__dict__, "image":order.product.images[0]}),
        "user": UserItem(**order.user.__dict__)
    }) for order in user.orders]

    return orders


"""
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

"""
