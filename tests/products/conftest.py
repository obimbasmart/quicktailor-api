from src.products.schemas import ProductUpload, CreateCustomCode
import pytest
from main import client

product_info = ProductUpload(name='test_product', price=43000.0, description="lorem ipsum delarmo",
                             estimated_tc=2, fabrics=["ankara"], categories=["senator"], colors=["red", "blue"],
                             images=["img-0", 'img-1'], is_active=True)


@pytest.fixture
def product_data():
    return product_info


@pytest.fixture
def db_product_id(access_token_tailor, product_data) -> str:
    res = client.post('/products', json=product_data.model_dump(),
                      headers=access_token_tailor['header'])
    assert res.status_code == 201
    return res.json()['id']
