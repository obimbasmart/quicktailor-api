from sqlalchemy import (Boolean, Column, String, DATETIME, 
        ForeignKey, Float, Table, Integer,JSON)
from sqlalchemy_json import NestedMutableJson
from sqlalchemy.orm import relationship
from models import BaseModel, Base
from sqlalchemy.ext.mutable import MutableList


class CartItem(BaseModel):
    __tablename__ = "carts"

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    product_id = Column(String(60), ForeignKey('products.id'), nullable=False)
    measurements = Column(NestedMutableJson, nullable=False)
    customization_id = Column(String(60), ForeignKey('customizations.id'), nullable=True)


    user = relationship("User", back_populates="carts")
    product = relationship("Product", back_populates="carts")
    customization_code = relationship("Customization", back_populates="carts")
