from typing import List
from sqlalchemy.orm import Session
from src.products.models.product import Fabric
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from src.tailors.models import Tailor
from src.users.models import User


def _create_fabrics(fabrics: List[str], db: Session):
    fabric_obj = [Fabric(name=name) for name in fabrics]
    db.add_all(fabric_obj)

    try:
        db.commit()
    except IntegrityError as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"One or more fabrics already exist with the given names")
    return [fabric.name for fabric in fabric_obj]


def _delete_fabric(fabric: str, db: Session):
    fabric_obj = db.query(Fabric).filter(Fabric.name==fabric).one_or_none()
    if not fabric_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No fabric found with given name")
    
    db.delete(fabric_obj)
    db.commit()
    return True

def _update_fabric(name: str, new_name: str, db: Session):
    fabric_obj = db.query(Fabric).filter(Fabric.name==name).one_or_none()
    if not fabric_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No fabric found with given name")
    
    fabric_obj.name = new_name
    db.add(fabric_obj)
    db.commit()
    return True

def _get_tailors(db: Session):
    return db.query(Tailor).all()

def _get_tailor(id: str, db: Session):
    return db.query(Tailor).filter(Tailor.id == id).one_or_none()

def _get_user(id: str, db: Session):
    return db.query(User).filter(User.id == id).one_or_none()

def _get_users(db: Session):
    return db.query(User).all()