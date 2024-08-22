from src.auth.schemas import UserRegIn, Login
from src.users.schemas import UpdateFields, MeasurementUpdate, AddFavorite
import pytest
from src.carts.schemas import AddToCart, RemoveCart


_info_update_fields = {"username": "arekak", "email": "ammalino@gmail.com",
                       "password": "Imaewwr22@", "phone": "08123456799"}
_info_update_fields_02 = {"username": "arek", "email": "tester02@gmail.com",
                          "password": "Imaewwr22@", "phone": "08123456789"}
_measurement_update_fields = {
    "measurement_type": "MALE", "neck": 3.4, "waist": 1.5, "chest_burst": 3.9}

_failure_data = {"name": "my_name", "is_online": True}


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


@pytest.fixture
def favorite_update_fields():
    def _favorite_update_fields(tailor_id: str = None, product_id: str = None):
        return AddFavorite(tailor_id=tailor_id, product_id=product_id)
    return _favorite_update_fields


@pytest.fixture
def create_new_cart():
    def create_cart(product_id: str, measurements: dict = _measurement_update_fields):
        return AddToCart(product_id=product_id, measurements=measurements)
    return create_cart


@pytest.fixture
def remove_cart_field():
    def remove_field(cart_id: str):
        return RemoveCart(cart_id=cart_id)
    return remove_field
