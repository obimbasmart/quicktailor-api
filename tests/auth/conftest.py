from src.auth.schemas import UserRegIn, Login, TailorRegIn, AdminRegIn
import pytest
import tests.data as test_data


@pytest.fixture
def user_data_register():
    return test_data.user_reg_obj


@pytest.fixture
def tailor_data_register():
    return test_data.tailor_reg_obj


@pytest.fixture
def admin_data_register():
    return test_data.admin_reg_obj


@pytest.fixture
def login_data_t():
    return test_data._login_data_t


@pytest.fixture
def login_data():
    return test_data._login_data_u

@pytest.fixture
def login_data_a():
    return test_data._login_data_a
