import os
import pytest
from database import Base, engine
from src.products.schemas import ProductUpload
from src.auth.schemas import TailorRegIn, UserRegIn, AdminRegIn
from main import client
from config import get_settings

settings = get_settings()
SSO = settings.ADMIN_SSO

_tailor_email_01 = 'tailor_01@gmail.com'
_tailor_email_02 = 'tailor_02@gmail.com'

_user_email_01 = 'tester@gmail.com'
_user_email_02 = 'tester02@gmail.com'

_admin_email_01 = 'admin@gmail.com'
_admin_email_02 = 'admin02@gmail.com'

_user_data_register = {
    "username": "tester",
    "phone": "09023473648",
    "password": "Test@user1",
    "password_2": "Test@user1"
}


_tailor_data_register = {
    "first_name": "tailorf",
    "last_name": "tailorl",
    "phone": "09384726482",
    "password": "Tailor@gmail1",
    "password_2": "Tailor@gmail1"
}

_admin_data_register = {
    'username': 'adminer',
    'phone': '09038394837',
    'password': 'Admin@gmail1',
    'password_2': 'Admin@gmail1'
}

_login_data_u = {"email": _user_email_01, "password": _user_data_register.get('password')}
_login_data_t = {"email": _tailor_email_01, "password": _tailor_data_register.get('password')}
_login_data_a = {"email": _admin_email_01, "password": _admin_data_register.get('password')}


tailor_reg_obj = TailorRegIn(**_tailor_data_register, email=_tailor_email_01)
tailor_reg_obj_02 = TailorRegIn(**_tailor_data_register, email=_tailor_email_02)

user_reg_obj = UserRegIn(**_user_data_register, email=_user_email_01)
user_reg_obj_02 = UserRegIn(**_user_data_register, email=_user_email_02)

admin_reg_obj = AdminRegIn(**_admin_data_register, email=_admin_email_01, sso=SSO)
admin_reg_obj_fake_sso = AdminRegIn(**_admin_data_register, email=_admin_email_02, sso='not correct')
