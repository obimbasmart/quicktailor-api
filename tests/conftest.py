import os
import pytest
from database import Base, engine
from main import client
from typing import Dict
from tests import data as test_data
from fastapi import HTTPException



def pytest_configure(config):
    env = os.getenv('ENVIRONMENT', 'production')
    if env.lower() != 'testing':
        pytest.exit("Tests can only be run in the testing environment. "
                    "Please set ENVIRONMENT=testing before running tests.")


@pytest.fixture
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def create_new_user(user_details, user_type: str = 'user') -> Dict:
    res_r = client.post(f'/auth/register/{user_type}',
                        json=user_details.model_dump())
    
    if res_r.status_code != 201:
        raise HTTPException(res_r.status_code,
                            'User can\'t be created')
    res_l = client.post(
        "/auth/login", json=user_details.model_dump(include=["email", "password"]))
    return \
        {
            'id': res_l.json()['data']['id'],
            'header': {"Authorization": f'Bearer {res_l.json()["access_token"]}'}
        }


@pytest.fixture
def access_token_tailor(reset_db):
    return create_new_user(test_data.tailor_reg_obj, user_type='tailor')


@pytest.fixture
def access_token_tailor_02():
    return create_new_user(test_data.tailor_reg_obj_02, user_type='tailor')


@pytest.fixture
def access_token_user(reset_db) -> str:
    return create_new_user(test_data.user_reg_obj)


@pytest.fixture
def access_token_user_02(reset_db) -> str:
    return create_new_user(test_data.user_reg_obj_02)


@pytest.fixture
def access_token_admin(reset_db) -> str:
    return create_new_user(test_data.admin_reg_obj, 'admin')

@pytest.fixture
def access_token_fake_admin(reset_db) -> str:
    return create_new_user(test_data.admin_reg_obj_fake_sso, 'admin')
