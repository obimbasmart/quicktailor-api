import pytest

_update_data_t = {
    "brand_name": "Yomi casual",
    "about": """
                    I am a good tailor, and I hope to pass the unittest,
                    make una help me. I can sew Senator and Nigerian attires.
             """,
    "photo": "http://www.my-photo.com",
}


@pytest.fixture
def update_data_t():
    return _update_data_t
