from main import client
from src.users.schemas import (UserInfo, SuccessMsg, FemaleMeasurementInfo,
        MaleMeasurementInfo, FavoriteResponse)
from uuid import uuid4
import pytest
from pydantic import ValidationError
from utils import generate_uuid
import json  

def test_get_user_favorites_success(access_token_user, reset_db):

    get_response = client.get("/users/favorites/{}".format(access_token_user['id']), headers=access_token_user['header'])

    assert get_response.status_code == 200, "Expected 200, got {}".format(get_response.status_code)
    FavoriteResponse.model_validate(get_response.json())

def test_get_user_favorites_unauthorized(access_token_user, access_token_user_02, reset_db):

    get_response = client.get("/users/favorites/{}".format(access_token_user['id']), headers=access_token_user_02['header'])
    assert get_response.status_code == 401, "Expected 401, got {}".format(get_response.status_code)

def test_add_tailor_favorites(access_token_user, access_token_tailor,  favorite_update_fields, reset_db):
    tailor_id = access_token_tailor['id']
    update_data = favorite_update_fields(tailor_id).model_dump()
    response = client.put(
        "/users/favorites/{}".format(access_token_user['id']),
        json=update_data,
        headers=access_token_user['header']
    )
    assert response.status_code == 200, "Expected 200, got {}".format(response.status_code)
    SuccessMsg.model_validate(response.json())

def test_add_product_favorites(access_token_user, access_token_tailor, product_01,  favorite_update_fields, reset_db):
    
    product_id = product_01(access_token_tailor)
    update_data = favorite_update_fields(None,product_id).model_dump()
    response = client.put(
        "/users/favorites/{}".format(access_token_user['id']),
        json=update_data,
        headers=access_token_user['header']
    )
    assert response.status_code == 200, "Expected 200, got {}".format(response.status_code)
    SuccessMsg.model_validate(response.json())

def test_wrong_id_add_favorites(access_token_user, access_token_tailor, product_01,  favorite_update_fields, reset_db):

    product_id = product_01(access_token_tailor)
    tailor_id = access_token_tailor['id']
    product_data = favorite_update_fields(None,access_token_user['id']).model_dump()
    tailor_data = favorite_update_fields(product_id,None).model_dump()

    response_tailor = client.put(
        "/users/favorites/{}".format(access_token_user['id']),
        json=tailor_data,
        headers=access_token_user['header']
    )
    response_product = client.put(
        "/users/favorites/{}".format(access_token_user['id']),
        json=product_data,
        headers=access_token_user['header']
    )

    assert response_tailor.status_code == 404, "Expected 404, got {}".format(response_tailor.status_code)
    assert response_product.status_code == 404, "Expected 404, got {}".format(response_product.status_code)


def test_add_favorites_unauthorized(access_token_user, access_token_user_02,  access_token_tailor, product_01,  favorite_update_fields, reset_db):

    product_id = product_01(access_token_tailor)
    tailor_id = access_token_tailor['id']
    send_data = favorite_update_fields(tailor_id,product_id).model_dump()

    response_data= client.put(
        "/users/favorites/{}".format(access_token_user['id']),
        json=send_data,
        headers=access_token_user_02['header']
    )

    assert response_data.status_code == 401, "Expected 401, got {}".format(response_data.status_code)
