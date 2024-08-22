from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from src.users.models import User
from src.tailors.models import Tailor
from src.auth.schemas import UserRegIn, BaseResponse, TailorRegIn, Login, LoginResponse, AdminRegIn
from src.auth.dependencies import get_db
from src.tailors.CRUD import create_tailor
from src.users.CRUD import create_user
from src.auth.utils import create_access_token
from src.auth.config import settings as auth_settings
from src.auth.dependencies import get_by_email
from src.admin.CRUD import _create_admin
from src.messages.dependencies import send_user_data_to_message_system, get_user_msg_data
from exceptions import already_exists_exception
from responses import create_success_response


router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={404: {"message": "Not found", "status": "Error"}},
)


@router.post("/register/user", response_model=BaseResponse)
def register_user(req_body: UserRegIn,
                  background_task: BackgroundTasks,
                  user: User = Depends(get_by_email),
                  db=Depends(get_db)):
    if user:
        raise already_exists_exception('User')

    user = create_user(req_body, db)
    user_data = get_user_msg_data(user)
    background_task.add_task(send_user_data_to_message_system, user_data)

    return create_success_response('User')


@router.post("/register/tailor", response_model=BaseResponse)
def register_tailor(req_body: TailorRegIn,
                    background_task: BackgroundTasks,
                    tailor: Tailor = Depends(get_by_email),
                    db=Depends(get_db)):
    if tailor:
        raise already_exists_exception('User')

    tailor = create_tailor(req_body, db)
    tailor_data = get_user_msg_data(tailor)
    background_task.add_task(send_user_data_to_message_system, tailor_data)

    return create_success_response('Tailor')


@router.post("/register/admin", response_model=BaseResponse)
def register_admi(req_body: AdminRegIn,
                  background_task: BackgroundTasks,
                  admin=Depends(get_by_email),
                  db=Depends(get_db)):
    if admin:
        raise already_exists_exception('User')


    admin = _create_admin(req_body, db)
    admin_data = get_user_msg_data(admin)
    background_task.add_task(send_user_data_to_message_system, admin_data)
    return create_success_response('Admin')

@router.post("/login", response_model=LoginResponse)
def login(req_body: Login, user=Depends(get_by_email)):
    if not user or not user.check_password(req_body.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    access_token = create_access_token(
        {"email": user.email}, auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {"access_token": access_token, "data": {"id": user.id}}
