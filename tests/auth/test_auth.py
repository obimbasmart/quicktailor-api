from main import client
from src.auth.schemas import BaseResponse, LoginResponse
from tests.schemas import ErrorResponse, MissingFieldResponse
from fastapi import status

import pytest
from pydantic import ValidationError


def test_user_register_success(user_data_register,
                               tailor_data_register,
                               admin_data_register,
                               reset_db):

    res_u = client.post("/auth/register/user",
                        json=user_data_register.model_dump())

    res_t = client.post("/auth/register/tailor",
                        json=tailor_data_register.model_dump())

    res_a = client.post("/auth/register/admin",
                        json=admin_data_register.model_dump())

    assert res_u.status_code == res_t.status_code == res_a.status_code == status.HTTP_201_CREATED

    BaseResponse.model_validate(res_u.json())
    BaseResponse.model_validate(res_t.json())
    BaseResponse.model_validate(res_a.json())


def test_user_register_existing_email(user_data_register,
                                      tailor_data_register,
                                      admin_data_register):
    res_u = client.post("/auth/register/user",
                        json=user_data_register.model_dump())

    res_t = client.post("/auth/register/tailor",
                        json=tailor_data_register.model_dump())

    res_a = client.post("/auth/register/admin",
                        json=admin_data_register.model_dump())

    assert res_u.status_code == res_t.status_code == res_a.status_code == status.HTTP_409_CONFLICT
    ErrorResponse.model_validate(res_u.json())
    ErrorResponse.model_validate(res_t.json())
    ErrorResponse.model_validate(res_a.json())


def test_user_register_missing_fields():
    res_u = client.post("/auth/register/user")
    res_t = client.post("/auth/register/tailor")
    res_a = client.post("/auth/register/admin")
    assert res_u.status_code == res_a.status_code == res_t.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    MissingFieldResponse.model_validate(res_u.json())
    MissingFieldResponse.model_validate(res_t.json())
    MissingFieldResponse.model_validate(res_a.json())


def test_user_login_success(login_data, login_data_t, login_data_a):
    res_u = client.post("/auth/login", json=login_data)
    res_t = client.post("/auth/login", json=login_data_t)
    res_a = client.post("/auth/login", json=login_data_a)

    assert res_u.status_code == res_t.status_code == res_a.status_code == status.HTTP_200_OK
    LoginResponse.model_validate(res_u.json())
    LoginResponse.model_validate(res_t.json())
    LoginResponse.model_validate(res_a.json())


def test_user_login_failure(login_data, login_data_t, login_data_a):
    fake_pwd = 'fake1234'
    res_u = client.post("/auth/login", json={"email": login_data.get('email'), "password": fake_pwd})
    res_t = client.post("/auth/login", json={"email": login_data_t.get('email'), "password": fake_pwd})
    res_a = client.post("/auth/login", json={"email": login_data_a.get('email'), "password": fake_pwd})

    assert res_u.status_code == res_t.status_code == res_a.status_code == status.HTTP_401_UNAUTHORIZED
    ErrorResponse.model_validate(res_u.json())
    ErrorResponse.model_validate(res_t.json())
    ErrorResponse.model_validate(res_a.json())
