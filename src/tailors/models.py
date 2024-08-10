from sqlalchemy import Boolean, Column, String, DATETIME, TEXT
from sqlalchemy_json import NestedMutableJson
from models import BaseUser
from sqlalchemy.orm import relationship

class Tailor(BaseUser):
    __tablename__ = "tailors"
    
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    DOB = Column(DATETIME, nullable=True)
    brand_name = Column(String(60), nullable=True)
    about = Column(String(400), nullable=True)
    nin = Column(String(11), nullable=True, unique=True)
    cac_number = Column(String(20), nullable=True)
    bank_details = Column(NestedMutableJson, nullable=True)
    photo = Column(TEXT, nullable=True)
    nin_photo = Column(TEXT, nullable=True)
    is_available = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    is_suspended = Column(Boolean, default=False)
    nin_is_verified = Column(Boolean, default=False)
    last_active = Column(DATETIME, nullable=True)
    language = Column(NestedMutableJson, nullable=True)

    products = relationship('Product', back_populates="tailor")
    orders = relationship("Order", back_populates="tailor")
