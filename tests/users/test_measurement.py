from main import client
from src.users.schemas import UserInfo, SuccessMsg, FemaleMeasurementInfo, MaleMeasurementInfo
from uuid import uuid4
import pytest
from pydantic import ValidationError
from utils import generate_uuid



def test_get_user_measurement(access_token_user, reset_db):

    get_response = client.get("/users/measurement/{}".format(access_token_user['id']), headers=access_token_user['header'])

    assert get_response.status_code == 200, "Expected 200, got {}".format(get_response.status_code)
    MaleMeasurementInfo.model_validate(get_response.json()[0])

def test_update_user_measurement_success(access_token_user, measurement_update_fields, reset_db):

    update_response = client.put("/users/measurement/{}".format(access_token_user['id']),json=measurement_update_fields.model_dump(), headers=access_token_user['header'])
    assert update_response.status_code == 200, "Expected 200, got {}".format(update_response.status_code)
    MaleMeasurementInfo.model_validate(update_response.json())


def test_invalid_fields(access_token_user, measurement_update_fields, failure_data, reset_db):
    
    update_response = client.put("/users/measurement/{}".format(access_token_user['id']),json=failure_data, headers=access_token_user['header'])
    assert update_response.status_code == 422, "Expected 200, got {}".format(update_response.status_code)
    assert update_response.json()['errors']


def test_unauthorized_update(access_token_user, access_token_user_02, measurement_update_fields, reset_db):
    
    other_user_id = access_token_user_02['id']

    update_response = client.put("/users/measurement/{}".format(other_user_id),json=measurement_update_fields.model_dump(), headers=access_token_user['header'])
    assert update_response.status_code == 401, "Expected 200, got {}".format(update_response.status_code)
    assert update_response.json()['detail']

