import pytest
from database import Base, engine
from src.products.schemas import ProductUpload
from src.auth.schemas import TailorRegIn, UserRegIn
from main import client

tailor_email_01 = 'tailor_01@gmail.com'
tailor_email_02 = 'tailor_02@gmail.com'

tailor_info = {
    'first_name': "tailof",
    "last_name": "tailorl",
    'phone': "09023456778",
    'password': "Tailor@pwd1",
    'password_2': "Tailor@pwd1"
}

tailor_reg_info = TailorRegIn(**tailor_info, email=tailor_email_01)
tailor_reg_info_02 = TailorRegIn(**tailor_info, email=tailor_email_02)

user_reg_info = UserRegIn(username='test', email='test_user@gmail.com', phone='09034568373',
                          password='test@pwd1', password_2='test@pwd1')


@pytest.fixture
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def create_new_user(user_info: TailorRegIn | UserRegIn, user_type: str = 'user') -> dict:
    res_r = client.post(f'/auth/register/{user_type}',
                        json=user_info.model_dump())
    assert res_r.status_code == 201
    res_l = client.post(
        "/auth/login", json=user_info.model_dump(include=["email", "password"]))
    return {"Authorization": f'Bearer {res_l.json()["access_token"]}'}


@pytest.fixture
def access_token_tailor_header(reset_db):
    return create_new_user(tailor_reg_info, user_type='tailor')


@pytest.fixture
def access_token_tailor_header_02():
    return create_new_user(tailor_reg_info_02, user_type='tailor')


@pytest.fixture
def access_token_user_header(reset_db) -> str:
    return create_new_user(user_reg_info)
