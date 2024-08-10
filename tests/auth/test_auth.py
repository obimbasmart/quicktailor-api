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


def test_user_register_existing_email(user_data_register):
    response = client.post("/auth/register/user",
                           json=user_data_register.model_dump())
    assert response.status_code == 409
    register_response_json = response.json()
    ErrorResponse.model_validate(register_response_json)


def test_user_register_missing_fields():
    response = client.post("/auth/register/user")
    assert response.status_code == 422
    MissingFieldResponse.model_validate(response.json())


def test_user_login_success(login_data):
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    LoginResponse.model_validate(response.json())


def test_user_login_failure():
    response = client.post(
        "/auth/login", json={"email": "test@gmail.com", "password": "fake_pwd"})
    assert response.status_code == 401
    ErrorResponse.model_validate(response.json())
