from sqlalchemy import (Column, String,  ForeignKey, Enum, JSON)
from sqlalchemy.ext.mutable import MutableDict, MutableList
from sqlalchemy.orm import relationship
from models import BaseModel
from enum import Enum as PyEnum
from src.orders.constants import ORDER_STAGES

class OrderStatus(PyEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DELIVERED = "delivered"
    DECLINED = "declined"

class Order(BaseModel):
    __tablename__ = "orders"

    tailor_id = Column(String(60), ForeignKey('tailors.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    product_id = Column(String(60), ForeignKey('products.id'), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    measurement = Column(MutableDict.as_mutable(JSON), nullable=True, default={})
    stages = Column(MutableDict.as_mutable(JSON), default=ORDER_STAGES)
    customization_code_id = Column(String(60), ForeignKey('customization_codes.id'), nullable=True)
 
    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")
    tailor = relationship("Tailor", back_populates="orders")
    customization_code = relationship("CustomizationCode", back_populates="orders")


