#!/usr/bin/env python3

"""BaseModel
"""

from sqlalchemy import String, Column, Boolean, TEXT, Enum
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from datetime import datetime, timezone
from sqlalchemy_json import NestedMutableJson
from enum import Enum as _Enum

from database import Base
from utils import generate_password_hash, check_password_hash


class BaseModel(Base):
    __abstract__ = True
    id: Mapped[str] = mapped_column(String(60), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc),
                                                 onupdate=lambda: datetime.now(timezone.utc))

    def __init__(self, *args, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now(timezone.utc)

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)


class UserType(_Enum):
    Tailor = 'Tailor'
    User = 'User'
    Admin = 'Admin'


class Gender(_Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'


class BaseUser(BaseModel):
    __abstract__ = True

    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(TEXT, nullable=False)
    phone = Column(String(60), nullable=True)
    email_notification = Column(Boolean, default=True)
    push_notification = Column(Boolean, default=True)
    is_online = Column(Boolean, default=False)
    email_is_verified = Column(Boolean, default=False)
    gender = Column(Enum(Gender), nullable=True)
    address = Column(NestedMutableJson, nullable=True)
    message_key = Column(String(60), nullable=False, unique=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
