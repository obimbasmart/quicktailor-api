from src.auth.schemas import UserRegIn, Login
import pytest


_user_id = {"id": "506a89b7-03d8-4ae7-8487-3c70e5ffb656"}


_user_data_register = {
                        "email" : "test@gmail.com", "username" : "test",
                        "phone" : "09023473648", "password": "test_pwd",
                        "password_2" : "test_pwd"
                      }

_login_data = {"email" : "test@gmail.com", "password": "test_pwd"}

@pytest.fixture
def user_id():
    return _user_id


@pytest.fixture
def user_data_register():
    return UserRegIn(**_user_data_register)


@pytest.fixture
def login_data():
    return _login_data
