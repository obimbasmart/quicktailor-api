from database import SessionLocal
from sqlalchemy.orm import Session
from src.users.models import User
from src.tailors.models import Tailor

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _utils_get_by_email(email: str, db: Session):
    user = db.query(User).filter(email==User.email).one_or_none()
    if not user:
        return db.query(Tailor).filter(email==Tailor.email).one_or_none()
    return user
