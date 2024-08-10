from sqlalchemy.orm import Session
from fastapi import Depends, Body
from dependencies import get_db
from src.users.models import User
from src.auth.schemas import UserRegIn

def get_user_by_email(req_body : UserRegIn = Body(...), db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(req_body.email==User.email).one_or_none()
    return user

def get_user_by_id(user_id: str, db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(user_id==User.id).one_or_none()
    return user

