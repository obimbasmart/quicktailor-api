from src.auth.schemas import UserRegIn
from .models import User
from src.users.schemas import UpdateFields, MeasurementUpdate, AddFavorite
from sqlalchemy.orm import Session
from utils_ import generate_uuid
from pydantic import UUID4
from src.users.constants import SUCCESSFUL_UPDATE


def create_user(user: UserRegIn, db: Session):
    new_user = User(**user.model_dump(exclude=["password", 'password_2']))

    new_user.set_password(user.password)
    new_user.message_key = generate_uuid()

    # TODO: sychronize user to message service

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_users(db: Session, filters: dict = None):
    return db.query(User).all()

def update_user(user_id: str,  update_data:UpdateFields, db: Session):

    user = db.query(User).filter(user_id==User.id).one_or_none()

    # Update the user fields if they are provided in update_data
    update_fields = update_data.dict(exclude_unset=True)
    for key, value in update_fields.items():
        if value is not None:
            if key == "password":
                # Hash the password and store it in password_hash attribute
                user.set_password(value)
            else:
                setattr(user, key, value)
    # Commit the changes to the database
    db.commit()
    db.refresh(user)
    return  SUCCESSFUL_UPDATE

def update_measurement(user_id: str, update_data: UpdateFields, db: Session):
    user = db.query(User).filter(User.id == user_id).one_or_none()

    # Update the user fields if they are provided in update_data
    update_fields = update_data.dict(exclude_unset=True)
    measurement_type = update_fields.get("measurement_type")
    measurement_tmp = []
    updated_measurement = None

    if 'measurement_type' in update_fields:
        # Convert the Enum to its string value
        measurement_type = measurement_type.value
        update_fields['measurement_type'] = measurement_type

    updated = False

    # Check and update the measurements
    for measurement in user.measurement:
        if measurement.get("measurement_type") == measurement_type:
            for k, v in update_fields.items():
                if v is not None:
                    measurement[k] = v
            updated = True
            updated_measurement = measurement
        measurement_tmp.append(measurement)

    if not updated:
        new_measurement = {"measurement_type": measurement_type, **update_fields}
        updated_measurement = new_measurement
        user.measurement.append(new_measurement)
    else:
        user.measurement = [m for m in measurement_tmp]

    # Commit the changes to the database
    db.commit()
    db.refresh(user)
    return updated_measurement

def add_favorite(user_id: str, update_data: AddFavorite, db: Session):
    user = db.query(User).filter(User.id == user_id).one_or_none()

    update_fields = update_data.dict(exclude_unset=True)
    tmp_favorites = user.favorites.copy()
    for k, v in tmp_favorites.items():
        for key, value in update_fields.items():
            if value != None:
                if key[:5] in k:
                    if value not in v:
                        user.favorites[k].append(value)
                    else:
                        user.favorites[k].remove(value)

                        print("Thise" in "Thiser")
    print(user.favorites, " here are we all time here again ago")
   
   # Commit the changes to the database
    db.commit()
    db.refresh(user)
    return SUCCESSFUL_UPDATE
