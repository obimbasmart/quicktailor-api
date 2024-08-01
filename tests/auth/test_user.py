from main import client
from src.auth.schemas import BaseResponse, LoginResponse
from tests.schemas import ErrorResponse, MissingFieldResponse

import pytest
from pydantic import ValidationError


def test_user_register_success(user_data_register, reset_db):
    response = client.post("/auth/register/user",
                           json=user_data_register.model_dump())
    assert response.status_code == 201
    register_response_json = response.json()
    BaseResponse.model_validate(register_response_json)
    assert register_response_json["message"]


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
    response = client.post("/auth/login", json={"email" : "test@gmail.com", "password" : "fake_pwd"})
    assert response.status_code == 401
    ErrorResponse.model_validate(response.json())
