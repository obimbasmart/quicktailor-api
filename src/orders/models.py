from sqlalchemy import (Column, String,  ForeignKey, Enum, JSON, Float)
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship
from models import BaseModel
from enum import Enum as PyEnum
from src.orders.constants import ORDER_STAGES
from sqlalchemy_json import NestedMutableJson
from src.payments.models import Payment


class OrderStatus(PyEnum):
    PENDING = "pending"
    IN_PROGRESS = "in progress"
    DELIVERED = "delivered"
    DECLINED = "declined"


class Order(BaseModel):
    __tablename__ = "orders"

    tailor_id = Column(String(60), ForeignKey('tailors.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    product_id = Column(String(60), ForeignKey('products.id'), nullable=False)
    payment_id = Column(String(60), ForeignKey('payments.id'), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    measurement = Column(NestedMutableJson, nullable=True, default={})
    stages = Column(NestedMutableJson, default=ORDER_STAGES)
    customization_id = Column(String(60), ForeignKey(
        'customizations.id'), nullable=True)
    amount_paid = Column(Float, nullable=False)

    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")
    tailor = relationship("Tailor", back_populates="orders")
    customization_code = relationship(
        "Customization", back_populates="orders")
    review = relationship("Review", back_populates="order")
