from main import client
from fastapi import status
from fastapi import HTTPException
import pytest


def test_admin_register_wrong_sso(access_token_fake_admin):
    assert access_token_fake_admin.status_code == status.HTTP_400_BAD_REQUEST

def test_get_tailors_success(access_token_admin):
    res = client.get('/admin/tailors', headers=access_token_admin.get('header'))
    assert res.status_code == status.HTTP_200_OK

def test_verify_tailor(access_token_admin, access_token_tailor):

    res = client.get(f'/admin/tailors/{access_token_tailor.get("id")}',
                     headers=access_token_admin.get('header'))
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get('nin_is_verified') == False

    res = client.patch(f'/admin/tailors/{access_token_tailor.get("id")}/verify',
                     headers=access_token_admin.get('header'))
    assert res.status_code == status.HTTP_200_OK

    res = client.get(f'/admin/tailors/{access_token_tailor.get("id")}',
                     headers=access_token_admin.get('header'))
    assert res.json()['nin_is_verified'] == True

def test_suspend_tailor(access_token_admin, access_token_tailor):

    res = client.get(f'/admin/tailors/{access_token_tailor.get("id")}',
                     headers=access_token_admin.get('header'))
    assert res.status_code == status.HTTP_200_OK
    assert res.json().get('is_suspended') == False

    res = client.patch(f'/admin/tailors/{access_token_tailor.get("id")}/suspend',
                     headers=access_token_admin.get('header'))
    assert res.status_code == status.HTTP_200_OK

    res = client.get(f'/admin/tailors/{access_token_tailor.get("id")}',
                     headers=access_token_admin.get('header'))
    assert res.json()['is_suspended'] == True

