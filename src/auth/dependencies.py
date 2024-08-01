from typing import Annotated
from src.auth.config import settings as auth_settings
import jwt
from fastapi import Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from dependencies import get_db
from fastapi import Depends
from src.auth.utils import get_by_email as utils_get_by_email
from src.users.models import User
from src.tailors.models import Tailor
from src.auth.schemas import Login
from sqlalchemy.orm import Session



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth_settings.SECRET_KEY, algorithms=[auth_settings.ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = utils_get_by_email(email, db)
    if user is None:
        raise credentials_exception
    return user

def get_by_email(req_body: Login = Body(...),  db = Depends(get_db)):
    return utils_get_by_email(req_body.email, db)