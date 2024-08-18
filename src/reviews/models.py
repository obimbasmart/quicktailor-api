from sqlalchemy import Column, String, Integer, ForeignKey, Text, Enum
from models import BaseModel
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum


class Rating(PyEnum):
    POOR = 1
    FAIR = 2
    GOOD = 3
    VERY_GOOD = 4
    EXCELLENT = 5


class Review(BaseModel):
    __tablename__ = "reviews"
    order_id = Column(String(60), ForeignKey('orders.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'),  nullable=False)
    tailor_id = Column(String(60), ForeignKey('tailors.id'),  nullable=False)
    text = Column(Text, nullable=False)
    seller_communication_level = Column(Enum(Rating), nullable=True)
    product_quality = Column(Enum(Rating), nullable=True)
    product_as_described = Column(Enum(Rating), nullable=True)
    recommend_to_friend = Column(Enum(Rating), nullable=True)

    user = relationship('User', back_populates="reviews")
    order = relationship('Order', back_populates="review")
