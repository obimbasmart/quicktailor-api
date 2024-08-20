from sqlalchemy.orm import Session
from fastapi import Depends, Body, HTTPException, status
from dependencies import get_db
from src.users.models import User
from src.auth.schemas import UserRegIn
from src.auth.dependencies import get_current_user
from exceptions import not_found_exception, unauthorized_access_exception


def get_user_by_email(req_body: UserRegIn = Body(...), db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(req_body.email == User.email).one_or_none()
    return user


def get_user_by_id(user_id: str, db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(user_id == User.id).one_or_none()

    if not user:
        raise not_found_exception('User')
    return user


def get_current_user(current_user=Depends(get_current_user)):
    if not isinstance(current_user, User):
        raise unauthorized_access_exception()
    return current_user
