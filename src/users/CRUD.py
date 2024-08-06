from src.auth.schemas import UserRegIn
from .models import User
from src.users.schemas import UpdateFields, MeasurementUpdate
from sqlalchemy.orm import Session
from utils import generate_uuid
from pydantic import UUID4
from src.users.constants import SUCCESSFUL_UPDATE


def create_user(user: UserRegIn, db: Session):
    new_user = User(**user.model_dump(exclude="password"))

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
    measurement_tmp =[] 
    updated_measurement = None
    if 'measurement_type' in update_fields:
        # Remove measurement_type from update_fields since it should not be part of the measurement object
        update_fields.pop("measurement_type")
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
        user.measurement = []
        for m in measurement_tmp:
            user.measurement.append(m)

    # Commit the changes to the database
    db.commit()
    db.refresh(user)
    return updated_measurement

