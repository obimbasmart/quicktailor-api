from src.auth.schemas import UserRegIn
from src.users.schemas import UpdateFields, MeasurementUpdate, AddFavorite
from sqlalchemy.orm import Session
from utils import generate_uuid
from pydantic import UUID4
from src.users.constants import SUCCESSFUL_UPDATE
from src.orders.schemas import OrderItem
from src.orders.models import Order

def create_new_order(user_id: str, tailor_id: str, order_data: OrderItem, db: Session):
    
    data = {k:v  for k, v in order_data if v != None}
    new_order = Order(**data, user_id = user_id, tailor_id = tailor_id)

    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order
