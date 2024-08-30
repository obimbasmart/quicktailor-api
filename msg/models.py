from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, relationship, mapped_column
import uuid
from datetime import datetime, timezone
from enum import Enum as _Enum
from msg.database import Base


class UserType(_Enum):
    USER = "user"
    ADMIN = "admin"
    TAILOR = "tailor"


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


class User(BaseModel):

    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(String(60), nullable=False)
    user_type: Mapped[UserType] = mapped_column(Enum(UserType), nullable=False)
    message_key: Mapped[str] = mapped_column(String(60), nullable=False)

    sent_messages = relationship(
        'Message', foreign_keys='Message.from_user_id', back_populates='from_user')
    received_messages = relationship(
        'Message', foreign_keys='Message.to_user_id', back_populates='to_user')
