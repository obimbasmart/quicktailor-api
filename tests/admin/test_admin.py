from main import client
from fastapi import status
from fastapi import HTTPException
import pytest


def test_admin_register_wrong_sso(access_token_fake_admin):
    assert access_token_fake_admin.status_code == status.HTTP_400_BAD_REQUEST

def test_get_tailors_success(access_token_admin):
    res = client.get('/admin/tailors', headers=access_token_admin.get('header'))
    assert res.status_code == status.HTTP_200_OK
