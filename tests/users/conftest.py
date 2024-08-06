from src.auth.schemas import UserRegIn, Login
from src.users.schemas import UpdateFields, MeasurementUpdate
import pytest


_info_update_fields = {"email": "memmalino@gmail.com", "password": "Imaewwr22@", "phone": "08123456789"}
_info_update_fields_02 = {"email": "test_user_02@gmail.com", "password": "Imaewwr22@", "phone": "08123456789"}
_measurement_update_fields = {"measurement_type": "male", "neck":3.4, "waist": 1.5, "chest_burst": 3.9}


_failure_data = {"name": "my_name", "is_online":True}


@pytest.fixture
def failure_data():
    return _failure_data

@pytest.fixture
def info_update_fields():
    return UpdateFields(**_info_update_fields)

@pytest.fixture
def measurement_update_fields():
    return MeasurementUpdate(**_measurement_update_fields)

@pytest.fixture
def info_update_fields_02():
    return UpdateFields(**_info_update_fields_02)
