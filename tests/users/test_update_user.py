from main import client
from src.users.schemas import UserInfo, SuccessMsg
from uuid import uuid4
import pytest
from pydantic import ValidationError
from utils import generate_uuid


def test_update_user_success(access_token_user, info_update_fields, reset_db):

    update_response = client.put(
        "/users/{}".format(access_token_user['id']), json=info_update_fields.model_dump(), headers=access_token_user['header'])
    assert update_response.status_code == 200, "Expected 200, got {}".format(
        update_response.status_code)
    SuccessMsg.model_validate(update_response.json())

    update_response = client.put(
        "/users/{}".format(access_token_user['id']), json=info_update_fields.model_dump(), headers=access_token_user['header'])


def test_invalid_fields(access_token_user, failure_data, reset_db):

    update_response = client.put(
        "/users/{}".format(access_token_user['id']), json=failure_data, headers=access_token_user['header'])
    assert update_response.status_code == 422, "Expected 422, got {}".format(
        update_response.status_code)
    assert update_response.json()['errors']


def test_unauthorized_update(access_token_user, access_token_user_02, info_update_fields, reset_db):

    other_user_id = access_token_user_02['id']

    update_response = client.put("/users/{}".format(other_user_id),
                                 json=info_update_fields.model_dump(), headers=access_token_user['header'])
    assert update_response.status_code == 401, "Expected 401, got {}".format(
        update_response.status_code)
    assert update_response.json()['detail']


def test_already_used_email(access_token_user, access_token_user_02, info_update_fields_02, reset_db):

    other_user_id = access_token_user_02['id']

    update_response = client.put("/users/{}".format(other_user_id),
                                 json=info_update_fields_02.model_dump(), headers=access_token_user_02['header'])
    print("This is the status code for succesful update", update_response.json())
    assert update_response.status_code == 422, "Expected 422, got {}".format(
        update_response.status_code)
    assert update_response.json()['detail']
