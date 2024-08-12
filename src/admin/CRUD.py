from typing import List
from sqlalchemy.orm import Session
from src.products.models.product import Fabric
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from src.tailors.models import Tailor
from src.users.models import User
from src.auth.schemas import AdminRegIn
from src.admin.models import Admin
from src.admin.schemas import AdminTailorUpdate
from src.admin.utils import TailorState
from config import get_settings
from utils import generate_uuid

settings = get_settings()



def _create_admin(req_body: AdminRegIn, db: Session):
    if req_body.sso != settings.ADMIN_SSO:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='The provided SSO code is not valid!')
    
    admin = Admin(**req_body.model_dump(exclude=['password_2', 'password']))
    admin.set_password(req_body.password)
    admin.message_key = generate_uuid()

    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

    
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


def _update_tailor(tailor_id, action: TailorState, db):
    tailor = _get_tailor(tailor_id, db)

    if not tailor:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Tailor not found')

    state_updates = {
        TailorState.VERIFY: {'nin_is_verified': True},
        TailorState.SUSPEND: {'is_suspended': True},
    }


    [
        setattr(tailor, key, value)
        for key, value in state_updates.get(action).items()
    ]

    tailor.check_and_activate(db)

    db.commit()
    db.refresh(tailor)
    return tailor