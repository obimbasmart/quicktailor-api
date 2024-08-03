from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from src.auth.dependencies import get_current_user
from src.users.CRUD import get_users, update_user
from src.users.dependencies import get_user_by_id
from src.users.schemas import UserInfo, UpdateFields, SuccessMsg
from dependencies import get_db
from typing import List
from pydantic import UUID4

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get('', response_model=List[UserInfo])
def get_all_users(current_user=Depends(get_current_user),
                    db=Depends(get_db)):
    users = get_users(db)
    return users

@router.get('/{user_id}', response_model=UserInfo)
def get_single_user(user_id: UUID4, current_user=Depends(get_current_user),
                      db=Depends(get_db), user=Depends(get_user_by_id)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found with the id")

    return user
@router.put('/{user_id}', response_model=SuccessMsg)
def update_user_route(req_body: UpdateFields,  user_id: str, current_user=Depends(get_current_user),
                      db=Depends(get_db), user = Depends(get_user_by_id)):
    if not user:
       raise HTTPException(status_code=404, detail="User not found with the id")

    update = update_user(user_id, req_body, db)
    return update
