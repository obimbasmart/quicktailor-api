from fastapi import Depends, HTTPException, status
from src.auth.dependencies import get_current_user
from src.tailors.models import Tailor
from src.users.models import User
from src.auth.schemas import AdminRegIn
from dependencies import get_db
from sqlalchemy.orm import Session
from src.admin.models import Admin


def get_current_admin(current_user = Depends(get_current_user)):
    if not isinstance(current_user, Admin):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return current_user

def get_current_admin_or_tailor(current_user = Depends(get_current_user)):
    if isinstance(current_user, User):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return current_user

def get_admin_by_email(req_body: AdminRegIn, db: Session = Depends(get_db)) -> Admin:
    admin = db.query(Admin).filter(req_body.email==Admin.email).one_or_none()
    return admin