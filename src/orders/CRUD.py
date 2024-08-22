from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.orders.models import Order, OrderStatus
from src.orders.constants import OrderStageStatus
from src.carts.models import CartItem
from typing import List
from src.products.models.customization import Customization
from sqlalchemy import func
from exceptions import not_found_exception


def create_orders(cart: List[str], payment_id: str, db: Session):

    carts = get_cart_items_by_id(cart, db)

    orders = [
        create_single_order(item, payment_id, db)
        for item in carts
    ]

    db.add_all(orders)
    db.commit()
    return orders


def create_single_order(cart_item: CartItem, payment_id, db: Session) -> Order:
    new_order = Order(
        tailor_id=cart_item.product.tailor.id,
        payment_id=payment_id,
        user_id=cart_item.user_id,
        product_id=cart_item.product_id,
        measurement=cart_item.measurements,
        customization_id=cart_item.customization_id,
    )

    new_order.amount_paid = get_actual_money_paid(customization_id=cart_item.customization_id,
                                                  product_price_tag=cart_item.product.price,
                                                  db=db)
    return new_order


def update_order_stage_status(order_id: str, current_user_id: str,  stage_name: str, new_status: str, db: Session):

    if new_status.upper() in OrderStageStatus.__members__:
        _new_status = OrderStageStatus[new_status.upper()]
    else:
        raise HTTPException(
            status_code=404, detail=f"Key: '{new_status}'  not found")

    order = db.query(Order).filter(Order.id == order_id).one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    stages = Order.deserialize_stages(order.stages)
    if stage_name not in stages:
        raise HTTPException(
            status_code=404,  detail="Stage '{stage_name}' not found in order")

    stage_order = list(stages.keys())
    # Check if the current stage is the last stage (stage 6)
    is_last_stage = (stage_name == stage_order[-1])
    # Permission check based on stage and user
    if is_last_stage:
        if current_user_id != order.user_id:
            raise HTTPException(status_code=401,  detail="Unauthorized access")
    else:
        if current_user_id != order.tailor_id:
            raise HTTPException(status_code=401,  detail="Unauthorized access")

    current_stage_index = stage_order.index(stage_name)
    if current_stage_index > 0:
        for previous_stage in stage_order[:current_stage_index]:
            if stages[previous_stage]['status'] != OrderStageStatus.COMPLETED:
                raise HTTPException(
                    status_code=401,  detail="Unauthorized access")

    stages[stage_name]['status'] = _new_status
    order.stages = Order.serialize_stages(stages)

    db.commit()
    db.refresh(order)

    return order


def update_order_status(order_id: str,  new_status: str, db: Session):
    if new_status.upper() in OrderStatus.__members__:
        _new_status = OrderStatus[new_status.upper()]
    else:
        raise HTTPException(
            status_code=404, detail=f"Key: '{new_status}'  not found")

    order = db.query(Order).filter(Order.id == order_id).one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = _new_status

    db.commit()
    db.refresh(order)

    return order


def get_cart_items_by_id(cart: List[str], session: Session):
    cart_items = session.query(CartItem).filter(CartItem.id.in_(cart)).all()

    if len(cart) != len(cart_items):
        raise not_found_exception('One or more cart items')
    return cart_items


def get_cart_items_by_reference(reference: str, db: Session):
    cart_identifiers = reference.split('-')
    cart_items = db.query(CartItem).filter(
        func.right(CartItem.id, 6).in_(cart_identifiers)
    ).all()

    if len(cart_items) != len(cart_identifiers):
        raise not_found_exception('One or more cart items')
    return cart_items


def get_actual_money_paid(customization_id: str,
                          product_price_tag: str,
                          db: Session) -> float:
    code = db.query(Customization).filter(
        Customization.id == customization_id).one_or_none()

    if not code:
        return product_price_tag

    deal_operations = {
        "INCREAMENT": lambda price, value: price + value,
        "DISCOUNT": lambda price, value: price - value,
    }

    unit_calculations = {
        "NAIRA": lambda price, value: value,
        "PERCENT": lambda price, value: (value / 100) * price,
    }

    adjustment_value = unit_calculations[code.unit](
        product_price_tag, code.value)
    actual_price = deal_operations[code.deal](
        product_price_tag, adjustment_value)

    return actual_price
