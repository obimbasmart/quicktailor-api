from main import client
from src.users.schemas import UserInfo
from uuid import uuid4
import pytest
from pydantic import ValidationError


def test_get_single_user_success(access_token_user, reset_db):

    get_response = client.get("/users/{}".format(access_token_user['id']), headers=access_token_user['header'])

    assert get_response.status_code == 200, "Expected 200, got {}".format(get_response.status_code)
    UserInfo.model_validate(get_response.json())


def test_get_single_user_not_found(access_token_user, reset_db):

    invalid_user_id = str(uuid4())

    # Get user
    response = client.get("/users/{}".format(invalid_user_id), headers=access_token_user['header'])
    print(response.json())
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found with the id"}
