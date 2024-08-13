from fastapi import  HTTPException
from sqlalchemy.orm import Session
from src.orders.models import Order, OrderStatus
from datetime import datetime
from src.orders.constants import OrderStageStatus
from src.orders.schemas import OrderItem

def create_new_order(user_id: str, tailor_id: str, order_data: OrderItem, db: Session):

    data = {k: v for k, v in order_data if v is not None}

    new_order = Order(**data, user_id=user_id, tailor_id=tailor_id)

    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


def update_order_stage_status(order_id: str, current_user_id: str,  stage_name: str, new_status:str, db: Session):

    if new_status.upper() in OrderStageStatus.__members__:
        _new_status = OrderStageStatus[new_status.upper()]
    else:
        raise HTTPException(status_code=404, detail=f"Key: '{new_status}'  not found")
    
    order = db.query(Order).filter(Order.id == order_id).one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    stages = Order.deserialize_stages(order.stages)
    if stage_name not in stages:
        raise HTTPException(status_code=404,  detail= "Stage '{stage_name}' not found in order")

    stage_order = list(stages.keys())
    # Check if the current stage is the last stage (stage 6)
    is_last_stage = (stage_name == stage_order[-1])
    # Permission check based on stage and user
    if is_last_stage:
        if current_user_id != order.user_id:
            raise HTTPException(status_code=401,  detail= "Unauthorized access")
    else:
        if current_user_id != order.tailor_id:
            raise HTTPException(status_code=401,  detail= "Unauthorized access")

    current_stage_index = stage_order.index(stage_name)
    if current_stage_index > 0:
        for previous_stage in stage_order[:current_stage_index]:
            if stages[previous_stage]['status'] != OrderStageStatus.COMPLETED:
                raise HTTPException(status_code=401,  detail= "Unauthorized access")

    stages[stage_name]['status'] = _new_status
    order.stages = Order.serialize_stages(stages)

    db.commit()
    db.refresh(order)

    return order

def update_order_status(order_id:str,  new_status: str, db: Session):
    if new_status.upper() in OrderStatus.__members__:
        _new_status = OrderStatus[new_status.upper()]
    else:
        raise HTTPException(status_code=404, detail=f"Key: '{new_status}'  not found")

    order = db.query(Order).filter(Order.id == order_id).one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = _new_status

    db.commit()
    db.refresh(order)

    return order
