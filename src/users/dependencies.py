from sqlalchemy.orm import Session
from fastapi import Depends, Body, HTTPException
from dependencies import get_db
from src.users.models import User
from src.auth.schemas import UserRegIn
from src.auth.dependencies import get_current_user
def get_user_by_email(req_body : UserRegIn = Body(...), db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(req_body.email==User.email).one_or_none()
    print(req_body)
    return user

def get_user_by_id(user_id: str, db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(user_id==User.id).one_or_none()
    return user

def get_current_user(current_user = Depends(get_current_user)):
    if not isinstance(current_user, User):
        raise HTTPException(status_code=403, detail="Access denied")
    return current_user

