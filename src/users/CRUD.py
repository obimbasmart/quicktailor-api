from src.auth.schemas import UserRegIn
from .models import User
from sqlalchemy.orm import Session
from utils import generate_uuid

def create_user(user: UserRegIn, db: Session):
    new_user = User(**user.model_dump(exclude="password"))

    new_user.set_password(user.password)
    new_user.message_key = generate_uuid()

    # TODO: sychronize user to message service

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user():
    pass