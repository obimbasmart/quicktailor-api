from sqlalchemy import Boolean, Column, String, Enum, Float, ForeignKey, DateTime
from sqlalchemy_json import NestedMutableJson
from models import BaseModel
from datetime import datetime, timezone
from enum import Enum as _Enum
from sqlalchemy.orm import relationship

class UNIT(_Enum):
    NAIRA = 0
    PERCENT = 1


class DEAL(_Enum):
    INCREAMENT = 0
    DISCOUNT = 1


class Customization(BaseModel):
    __tablename__ = "customizations"

    deal = Column(Enum(DEAL), default=DEAL.DISCOUNT)
    unit = Column(Enum(UNIT), default=UNIT.NAIRA)
    value = Column(Float, nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'))
    tailor_id = Column(String(60), ForeignKey('tailors.id'))
    product_id = Column(String(60), ForeignKey('products.id'))
    expires_in = Column(DateTime, nullable=False)
    start_date = Column(
        DateTime, default=lambda: datetime.now(tz=timezone.utc))
    is_active = Column(Boolean, default=True)

    orders = relationship('Order', back_populates='customization_code')
    carts = relationship('CartItem', back_populates='customization_code')
