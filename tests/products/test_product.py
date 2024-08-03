from main import client
from src.auth.schemas import BaseResponse
from src.products.schemas import ProductListItem, ProductTailorItem, ProductItem
from fastapi import status


def test_create_product_success(access_token_tailor, product_data):
    res = client.post('/products', json=product_data.model_dump(),
                      headers=access_token_tailor['header'])

    assert res.status_code == 201
    BaseResponse.model_validate(res.json())


def test_create_product_failure_unauthorized(product_data):
    res = client.post('/products', json=product_data.model_dump())
    assert res.status_code == 401
    assert res.json()['detail']


def test_create_product_failure_access_denied(access_token_user, product_data):
    res = client.post('/products', json=product_data.model_dump(),
                      headers=access_token_user['header'])
    assert res.status_code == 403
    assert res.json()['detail']


def test_get_products(access_token_user, access_token_tailor):
    user_res = client.get('/products', headers=access_token_user['header'])
    tailor_res = client.get('/products', headers=access_token_user['header'])

    assert user_res.status_code == status.HTTP_200_OK == tailor_res.status_code
    assert isinstance(user_res.json(), list)
    [ProductListItem.model_validate(Item) for Item in user_res.json()]


def test_get_product(access_token_user, db_product_id):
    res = client.get(f'/products/{db_product_id}',
                     headers=access_token_user['header'])
    assert res.status_code == status.HTTP_200_OK
    ProductItem.model_validate(res.json())


def test_get_product_tailor_info(access_token_user, db_product_id):
    res = client.get(f'/products/{db_product_id}/tailor',
                     headers=access_token_user['header'])
    assert res.status_code == status.HTTP_200_OK
    ProductTailorItem.model_validate(res.json())


def test_delete_product_success(access_token_tailor, db_product_id):
    res = client.delete(
        f'/products/{db_product_id}', headers=access_token_tailor['header'])
    assert res.status_code == status.HTTP_200_OK
    BaseResponse.model_validate(res.json())


def test_delete_product_unauthorized(access_token_user, db_product_id):
    res = client.delete(
        f'/products/{db_product_id}', headers=access_token_user['header'])
    assert res.status_code == status.HTTP_403_FORBIDDEN
    assert res.json()['detail']


def test_delete_product_access_denied(access_token_tailor_02, db_product_id):
    res = client.delete(
        f'/products/{db_product_id}', headers=access_token_tailor_02['header'])
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
    assert res.json()['detail']