from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from src.users.models import User
from src.tailors.models import Tailor
from .schemas import UserRegIn, BaseResponse, TailorRegIn, Login, LoginResponse, AdminRegIn
from src.users.dependencies import get_user_by_email
from src.tailors.dependencies import get_tailor_by_email
from src.auth.dependencies import get_db
from src.tailors.CRUD import create_tailor
from src.users.CRUD import create_user
from .utils import create_access_token
from .config import settings as auth_settings
from src.auth.dependencies import get_by_email
from src.admin.dependencies import get_admin_by_email
from src.admin.CRUD import _create_admin
from src.messages.dependencies import send_user_info
from src.messages.schemas import UserInfo
router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={404: {"message": "Not found", "status": "Error"}},
)


@router.post("/register/user", response_model=BaseResponse)
def register_user(req_body: UserRegIn,
                  user: User = Depends(get_user_by_email),
                  db=Depends(get_db)):
    if user:
        raise HTTPException(status_code=409, detail="User already exist")

    # TODO: sync user to message app service - Background task

    user = create_user(req_body, db)
    user_info = UserInfo(message_key=user.message_key, user_id = user.id, user_type = 'user')
    message_user_info = send_user_info(user_info)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={"message": "Registeration successfull!"})

@router.post("/register/tailor", response_model=BaseResponse)
def register_tailor(req_body: TailorRegIn,
                    tailor: Tailor = Depends(get_tailor_by_email),
                    db=Depends(get_db)):
    if tailor:
        raise HTTPException(status_code=409, detail="Tailor already exist")

    # TODO: sync tailor to message app service - Background task

    tailor = create_tailor(req_body, db)
    tailor_info = UserInfo(message_key=tailor.message_key, user_id = tailor.id, user_type = 'tailor')
    message_user_info = send_user_info(user_info)

    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={"message": "Registeration successfull!"})


@router.post("/register/admin", response_model=BaseResponse)
def register_admi(req_body: AdminRegIn,
                  admin=Depends(get_admin_by_email),
                  db=Depends(get_db)):
    if admin:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Admin with email already exist")

    # TODO: sync tailor to message app service - Background task

    admin = _create_admin(req_body, db)
    admin_info = UserInfo(message_key=admin.message_key, user_id = admin.id, user_type = 'admin')
    message_user_info = send_user_info(user_info)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Registeration successfull!"})


@router.post("/login", response_model=LoginResponse)
def login(req_body: Login, user=Depends(get_by_email)):
    if not user or not user.check_password(req_body.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    access_token = create_access_token(
        {"email": user.email}, auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {"access_token": access_token, "data": {"id": user.id}}
