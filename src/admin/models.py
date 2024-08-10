from sqlalchemy import Boolean, Column, String, JSON
from sqlalchemy_json import NestedMutableJson
from models import BaseUser
from sqlalchemy.ext.mutable import MutableList

class Admin(BaseUser):
    __tablename__ = "admins"
    is_super_admin = Column(Boolean, default=False)