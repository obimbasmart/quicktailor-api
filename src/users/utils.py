from sqlalchemy.orm import Session
from fastapi import Depends, Body
from src.users.models import User


def get_user_via_email(email: str, db: Session ) -> User:
    user = db.query(User).filter(email==User.email).one_or_none()
    return user



