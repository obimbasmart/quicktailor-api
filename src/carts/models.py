from sqlalchemy import (Boolean, Column, String, DATETIME, 
        ForeignKey, Float, Table, Integer,JSON)
from sqlalchemy_json import NestedMutableJson
from sqlalchemy.orm import relationship
from models import BaseModel, Base
from sqlalchemy.ext.mutable import MutableList


class Cart(BaseModel):
    __tablename__ = "carts"

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    product_id = Column(String(60), ForeignKey('products.id'), nullable=False)
    measurement = Column(MutableList.as_mutable(JSON), nullable=True, default=[])
    customization_id = Column(String(60), ForeignKey('customizations.id'), nullable=True)


    user = relationship("User", back_populates="carts")
    product = relationship("Product", back_populates="carts")

