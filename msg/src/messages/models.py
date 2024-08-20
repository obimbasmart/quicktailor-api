from sqlalchemy import (String, Column, func,  Boolean, Text, Enum,
                        JSON, ForeignKey, case)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from enum import Enum as _Enum
from msg.models import BaseModel, User
from sqlalchemy.ext.mutable import MutableDict, MutableList


class Message(BaseModel):

    __tablename__ = 'messages'

    from_user_id: Mapped[str] = mapped_column(
        String(60), ForeignKey('users.user_id'), nullable=False)
    from_user_key: Mapped[str] = mapped_column(String(60), nullable=False)
    to_user_id: Mapped[str] = mapped_column(
        String(60), ForeignKey('users.user_id'), nullable=False)
    product: Mapped[dict] = mapped_column(
        MutableDict.as_mutable(JSON), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    media_name: Mapped[str] = mapped_column(String(240), nullable=True)
    is_viewed: Mapped[bool] = mapped_column(Boolean, default=False)

    from_user = relationship('User', foreign_keys=[
                             from_user_id], back_populates='sent_messages')
    to_user = relationship('User', foreign_keys=[
                           to_user_id], back_populates='received_messages')

    @classmethod
    def get_last_messages(cls, user_id, db):
        user1_case = case(
            (cls.from_user_id < cls.to_user_id, cls.from_user_id),
            else_=cls.to_user_id
        ).label("user1")

        user2_case = case(
            (cls.from_user_id < cls.to_user_id, cls.to_user_id),
            else_=cls.from_user_id
        ).label("user2")

        subquery = (
            db.query(
                func.max(cls.created_at).label("max_created_at"),
                user1_case,
                user2_case
            )
            .filter((cls.from_user_id == user_id) | (cls.to_user_id == user_id))
            .group_by(user1_case, user2_case)
            .subquery()
        )

        query = (
            db.query(cls)
            .join(
                subquery,
                (cls.created_at == subquery.c.max_created_at) &
                ((cls.from_user_id == subquery.c.user1) & (cls.to_user_id == subquery.c.user2) |
                 (cls.from_user_id == subquery.c.user2) & (cls.to_user_id == subquery.c.user1))
            )
            .order_by(cls.created_at.desc())
        )

        return query.all()
