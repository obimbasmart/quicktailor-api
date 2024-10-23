from src.auth.schemas import UserRegIn
from .models import User
from src.users.schemas import UpdateUserFields, MeasurementUpdate, AddFavorite, PasswordReset
from sqlalchemy.orm import Session
from utils import generate_uuid
from pydantic import UUID4
from src.tailors.dependencies import get_tailor_by_id
from src.products.CRUD import get_product_by_id

from src.users.constants import SUCCESSFUL_UPDATE
from fastapi import HTTPException
from exceptions import not_found_exception, unauthorized_access_exception
from services.otp import otp_service


def create_user(user: UserRegIn, db: Session):
    if not otp_service.verify_otp(user.email, user.otp):
        raise unauthorized_access_exception("Invalid OTP")

    new_user = User(**user.model_dump(exclude=["password", 'password_2']))

    new_user.set_password(user.password)
    new_user.message_key = generate_uuid()
    new_user.username = "User-" + new_user.id[-4:]

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_users(db: Session, filters: dict = None):
    return db.query(User).all()


def _update_user(current_user: User,  req_body: UpdateUserFields, db: Session):

    update_data = req_body.model_dump(exclude_unset=True)

    [
        setattr(current_user, key, value)
        for key, value in update_data.items()
    ]

    db.commit()
    db.refresh(current_user)
    return current_user


def _update_user_password(user: User, req_body: PasswordReset, db: Session):
    user.set_password(req_body.password)
    db.commit()
    db.refresh(user)
    return user


def update_measurements(user: User,
                        update_data: UpdateUserFields,
                        db: Session):

    update_data = update_data.model_dump(exclude_unset=True)
    user.measurements.update(update_data)

    db.commit()
    db.refresh(user)
    return user


def add_to_favorites(user: User, req_body: AddFavorite, db: Session):

    update_data = req_body.model_dump(exclude_defaults=True)

    if update_data.get('tailor_id'):
        tailor = get_tailor_by_id(update_data.get('tailor_id'), db)
        user.favorites['tailors'] = toggle_item_in_list(tailor.id, user.favorites['tailors'])
    
    if update_data.get('product_id'):
        product = get_product_by_id(update_data.get('product_id'), db)
        user.favorites['products'] = toggle_item_in_list(product.id, user.favorites['products'])

    db.commit()
    db.refresh(user)
    return True


def toggle_item_in_list(item: str, items: list):
    items.remove(item) \
        if item in items \
            else items.append(item)
    return items