from main import client
from src.auth.schemas import BaseResponse
from src.products.schemas import ProductListItem, ProductTailorItem, ProductItem
from fastapi import status


def test_create_product_success(access_token_tailor, product_data):
    res = client.post('/products', json=product_data.model_dump(),
                      headers=access_token_tailor['header'])

    assert res.status_code == status.HTTP_201_CREATED
    BaseResponse.model_validate(res.json())


def test_create_product_failure_unauthorized(product_data):
    res = client.post('/products', json=product_data.model_dump())
    assert res.status_code == 401
    assert res.json()['detail']


def test_create_product_failure_access_denied(access_token_user, product_data):
    res = client.post('/products', json=product_data.model_dump(),
                      headers=access_token_user['header'])
    assert res.status_code == status.HTTP_403_FORBIDDEN
    assert res.json()['detail']


def testget_product_by_ids(access_token_user,
                           access_token_tailor,
                           access_token_admin):
    res_u = client.get('/products', headers=access_token_user['header'])
    res_t = client.get('/products', headers=access_token_tailor['header'])
    res_a = client.get('/products', headers=access_token_admin['header'])

    assert res_u.status_code == status.HTTP_200_OK == res_t.status_code == res_a.status_code
    assert isinstance(res_u.json(), list)
    [ProductListItem.model_validate(Item) for Item in res_u.json()]
    [ProductListItem.model_validate(Item) for Item in res_t.json()]
    [ProductListItem.model_validate(Item) for Item in res_a.json()]


def testget_product_by_id(access_token_user, db_product_id):
    res = client.get(f'/products/{db_product_id}',
                     headers=access_token_user['header'])
    assert res.status_code == status.HTTP_200_OK
    ProductItem.model_validate(res.json())


def testget_product_by_id_tailor_info(access_token_user, db_product_id):
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


def test_update_product(access_token_tailor, db_product_id):
    res = client.put(f'/products/{db_product_id}',
                     headers=access_token_tailor['header'],
                     json={'name': 'Red Asoebi'})

    assert res.status_code == status.HTTP_200_OK

    res = client.get(f'/products/{db_product_id}',
                     headers=access_token_tailor['header'])
    assert res.status_code == status.HTTP_200_OK
    assert res.json()['name'] == 'Red Asoebi'
