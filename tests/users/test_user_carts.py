from main import client
from src.auth.schemas import BaseResponse
from src.products.schemas import ProductListItem, ProductTailorItem, ProductItem
from fastapi import status
from src.users.schemas import (UserInfo, SuccessMsg, FemaleMeasurementInfo,
                               MaleMeasurementInfo, FavoriteResponse)
from uuid import uuid4
from src.carts.schemas import CartItems
import pytest
from pydantic import ValidationError
from utils import generate_uuid
import json
from typing import List


def test_create_cart_success(access_token_tailor, product_01, access_token_user, create_new_cart):

    product = product_01(access_token_tailor)
    send_data = create_new_cart(product).model_dump()
    res = client.post(f'/carts/{access_token_user["id"]}', json=send_data,
                      headers=access_token_user['header'])
    print("here is what I am testing", res.json())
    assert res.status_code == 200
    BaseResponse.model_validate(res.json())


def test_create_cart_failure_unauthorized(create_new_cart, access_token_user,  access_token_tailor, product_01):
    product = product_01(access_token_tailor)
    res = client.post(
        f'/carts/{access_token_user["id"]}', json=create_new_cart(product).model_dump())
    assert res.status_code == 401
    assert res.json()['detail']


def test_create_cart_failure_access_denied(access_token_tailor, product_01, access_token_user, create_new_cart):
    product = product_01(access_token_tailor)
    res = client.post(f'/carts/{access_token_user["id"]}', json=create_new_cart(product).model_dump(),
                      headers=access_token_tailor['header'])
    assert res.status_code == 403
    assert res.json()['detail']


def test_get_cart_successful(access_token_user, access_token_tailor, product_01, create_new_cart):
    product = product_01(access_token_tailor)
    cart_creation = res = client.post(f'/carts/{access_token_user["id"]}', json=create_new_cart(product).model_dump(),
                                      headers=access_token_user['header'])
    res = client.get('/carts/{}'.format(access_token_user['id']),
                     headers=access_token_user['header'])
    assert res.status_code == 200
    print("This is the cart response:  ", res.json()[0])
    CartItems.model_validate(res.json()[0])


def test_get_empty_cart(access_token_user):
    res = client.get(
        f'/carts/{access_token_user["id"]}', headers=access_token_user['header'])
    assert res.status_code == 200


def test_get_cart_failiure_access_denied(access_token_tailor):
    res = client.get(
        f'/carts/{access_token_tailor["id"]}', headers=access_token_tailor['header'])
    assert res.status_code == 403


def test_get_cart_failure_unauthorized(access_token_tailor, access_token_user):
    res = client.get(
        f'/carts/{access_token_tailor["id"]}', headers=access_token_user['header'])
    assert res.status_code == 401


def test_delete_cart_successful(access_token_user, access_token_tailor, remove_cart_field, product_01, create_new_cart):
    product = product_01(access_token_tailor)
    cart_creation = client.post(
        f'/carts/{access_token_user["id"]}',
        json=create_new_cart(product).model_dump(),
        headers=access_token_user['header']
    )

    res = client.get(
        f'/carts/{access_token_user["id"]}',
        headers=access_token_user['header']
    )
    cart_id = res.json()[0]['id']

    delete_response = client.delete(
        f'/carts/{cart_id}',
        headers=access_token_user['header']
    )

    print("This is the response for Deletion", delete_response.json())

    assert delete_response.status_code == 200, f"Expected 200, got {delete_response.status_code}"


"""
def test_delete_product_success(access_token_tailor, db_product_id):
    res = client.delete(
        f'/products/{db_product_id}', headers=access_token_tailor['header'])
    assert res.status_code == status.HTTP_200_OK
    BaseResponse.model_validate(res.json())


def test_delete_product_unauthorized(access_token_user, db_product_id):
    res = client.delete(
        f'/products/{db_product_id}', headers=access_token_user['header'])
    assert res.status_code == status.HTTP_403_FORBIDDEN
"""
