from fastapi import Depends, HTTPException, status
from src.auth.dependencies import get_current_user
from src.tailors.models import Tailor
from src.users.models import User


def get_current_admin(current_user = Depends(get_current_user)):
    if isinstance(current_user, Tailor) or not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return current_user

def get_current_admin_or_tailor(current_user = Depends(get_current_user)):
    if isinstance(current_user, User) and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return current_user