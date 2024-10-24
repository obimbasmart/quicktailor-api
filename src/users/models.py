from sqlalchemy import Column, String
from sqlalchemy_json import NestedMutableJson
from src.users.constants import MEASUREMENTS, FAVORITES
from models import BaseUser
from src.carts.models import CartItem
from sqlalchemy.orm import relationship


class User(BaseUser):
    __tablename__ = "users"
    username = Column(String(60), nullable=True)
    measurements = Column(NestedMutableJson, default=MEASUREMENTS)
    favorites = Column(NestedMutableJson, default=FAVORITES)
    carts = relationship('CartItem', back_populates='user')
    orders = relationship('Order', back_populates='user')
    reviews = relationship('Review', back_populates='user')