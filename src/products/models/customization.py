from sqlalchemy import Boolean, Column, String, Enum, Float, ForeignKey, DateTime
from sqlalchemy_json import NestedMutableJson
from models import BaseModel
from datetime import datetime, timezone
from enum import Enum as _Enum

class UNIT(_Enum):
    NAIRA = 0
    PERCENT = 1

class DEAL(_Enum):
    INCREAMENT = 0
    DISCOUNT = 1

class CustomizationCode(BaseModel):
    __tablename__ = "customization_codes"

    deal = Column(Enum(DEAL), default=UNIT.NAIRA)
    unit = Column(Enum(UNIT), default=DEAL.DISCOUNT)
    value = Column(Float, nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'))
    tailor_id = Column(String(60), ForeignKey('tailors.id'))
    product_id = Column(String(60), ForeignKey('products.id'))
    expires_in = Column(DateTime, nullable=False)
    start_date = Column(DateTime, default= lambda: datetime.now(tz=timezone.utc))
    is_active = Column(Boolean, default=True)
