
from src.auth.schemas import TailorRegIn
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
