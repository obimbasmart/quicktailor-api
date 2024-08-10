from sqlalchemy import Boolean, Column, String, JSON
from sqlalchemy_json import NestedMutableJson
from models import BaseUser
from .constants import MALE_MEASUREMENTS, FAVORITES, FEMALE_MEASUREMENTS
from sqlalchemy.ext.mutable import MutableList

class User(BaseUser):
    __tablename__ = "users"
    username = Column(String(60), nullable=False)
    measurement = Column(MutableList.as_mutable(JSON), nullable=True, default=[MALE_MEASUREMENTS, FEMALE_MEASUREMENTS])
    favorites = Column(NestedMutableJson, default=FAVORITES)
