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

