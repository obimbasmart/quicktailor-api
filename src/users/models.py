from sqlalchemy import Boolean, Column, String
from sqlalchemy_json import NestedMutableJson
from models import BaseUser
from .constants import MALE_MEASUREMENTS, FAVORITES


class User(BaseUser):
    __tablename__ = "users"

    username = Column(String(60), nullable=False)
    measurement = Column(NestedMutableJson, nullable=True, default=MALE_MEASUREMENTS)
    is_admin = Column(Boolean, default=False)
    favorites = Column(NestedMutableJson, default=FAVORITES)
