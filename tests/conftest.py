import pytest
from database import Base, engine



@pytest.fixture
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
