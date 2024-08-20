from sqlalchemy.orm import Session
from fastapi import Depends, Body, HTTPException, Header, status
from msg.dependencies import get_db
from msg.models import User
import os


def verify_by_id(user_id: str, db: Session):
    user = db.query(User).filter(user_id == User.user_id).one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


def get_user_by_id(user_id: str, db: Session):
    user = db.query(User).filter(user_id == User.user_id).one_or_none()

    return user


def verify_secret_key(x_secret_key: str = Header(...)):

    SECRET_KEY = os.getenv("SECRET_KEY")

    if x_secret_key != SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid secret key"
        )
