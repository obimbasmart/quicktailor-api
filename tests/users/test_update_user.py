from main import client
from src.users.schemas import UserInfo
from uuid import uuid4
import pytest
from pydantic import ValidationError


def test_get_single_user_success(user_data_register, login_data, reset_db):
    # Register user
    register_response = client.post("/auth/register/user",
                                    json=user_data_register.model_dump())

    # Login
    login_response = client.post("/auth/login", json=login_data)
    login_data = login_response.json()

    access_token = login_data.get('access_token')
    user_id = login_data.get('data', {}).get('id')

    if not access_token or not user_id:
        assert False, "Login failed to provide necessary data"

    # Construct headers correctly
    headers = {"Authorization": "Bearer {}".format(access_token)}

    # Get user
    get_response = client.get("/users/{}".format(user_id), headers=headers)

    assert get_response.status_code == 200, "Expected 200, got {}".format(get_response.status_code)
    UserInfo.model_validate(get_response.json())


def test_get_single_user_not_found(user_data_register, login_data, reset_db):

    invalid_user_id = str(uuid4())

    # Register user
    register_response = client.post("/auth/register/user",
                                    json=user_data_register.model_dump())

    # Login
    login_response = client.post("/auth/login", json=login_data)
    login_data = login_response.json()

    access_token = login_data.get('access_token')


    # Construct headers correctly
    headers = {"Authorization": "Bearer {}".format(access_token)}

    # Get user
    response = client.get("/users/{}".format(invalid_user_id), headers=headers)
    print(response.json())
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found with the id"}
