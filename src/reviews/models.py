from sqlalchemy import Column, String,Integer, ForeignKey, Text
from models import BaseModel
from sqlalchemy.orm import relationship


class Review(BaseModel):
    __tablename__ = "reviews"
    order_id = Column(String(60), ForeignKey('orders.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'),  nullable=False)
    text = Column(Text, nullable=False)
    seller_communication_level = Column(Integer, nullable=True)
    product_quality = Column(Integer, nullable=True)
    product_as_described = Column(Integer, nullable=True)
    recommend_to_friend = Column(Integer, nullable=True)

    user  = relationship('User', back_populates="reviews")
    order = relationship('Order', back_populates="review")

