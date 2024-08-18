
from src.auth.schemas import TailorRegIn
from src.tailors.schemas import UpdateTailor
from .models import Tailor
from sqlalchemy.orm import Session
from utils import generate_uuid


def create_tailor(tailor: TailorRegIn, db: Session):
    new_tailor = Tailor(**tailor.model_dump(exclude="password"))

    new_tailor.set_password(tailor.password)
    new_tailor.message_key = generate_uuid()

    # TODO: sychronize tailor to message service

    db.add(new_tailor)
    db.commit()
    db.refresh(new_tailor)
    return new_tailor


def get_tailors(db: Session, filters: dict = None):
    return db.query(Tailor).all()


def _update_tailor(tailor: Tailor, req_body: UpdateTailor, db: Session):
    update_data = req_body.model_dump(exclude_unset=True)

    [
        setattr(tailor, attr, value)
        for attr, value in update_data.items()
        if attr not in ['first_name', 'last_name']
    ]

    if not tailor.nin_is_verified:
        [
            setattr(tailor, attr, value)
            for attr, value in update_data.items()
            if attr in ['first_name', 'last_name']
        ]

    tailor.check_and_activate(db)

    db.commit()
    db.refresh(tailor)
    return tailor
