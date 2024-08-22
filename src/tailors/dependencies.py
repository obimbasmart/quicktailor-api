from sqlalchemy.orm import Session
from fastapi import Depends, Body, HTTPException
from dependencies import get_db
from src.tailors.models import Tailor
from src.auth.schemas import TailorRegIn
from src.auth.dependencies import get_current_user
from exceptions import not_found_exception, access_denied_exception


def get_tailor_by_id(tailor_id: str, db: Session = Depends(get_db)) -> Tailor:
    tailor = db.query(Tailor).filter(tailor_id==Tailor.id).one_or_none()
    if not tailor:
        raise not_found_exception('Tailor')
    return tailor


def get_tailor_by_email(req_body : TailorRegIn = Body(...), db: Session = Depends(get_db)) -> Tailor:
    tailor = db.query(Tailor).filter(req_body.email==Tailor.email).one_or_none()
    return tailor

def get_current_tailor(current_user = Depends(get_current_user)):
    if not isinstance(current_user, Tailor):
        raise access_denied_exception()
    return current_user