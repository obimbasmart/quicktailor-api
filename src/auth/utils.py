from datetime import datetime, timedelta, timezone
from .config import settings
import jwt
from src.users.models import User
from src.tailors.models import Tailor
from src.admin.models import Admin
from fastapi import Depends
from dependencies import get_db

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_by_email(email: str, db=None):
    user = db.query(User).filter(email==User.email).one_or_none()
    if not user:
        user = db.query(Tailor).filter(email==Tailor.email).one_or_none()

    if not user:
        user = db.query(Admin).filter(email==Admin.email).one_or_none()
    return user