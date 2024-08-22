from sqlalchemy import Boolean, Column, String, DATETIME, ForeignKey, Float, Table, Integer
from sqlalchemy_json import NestedMutableJson
from sqlalchemy.orm import relationship
from models import BaseModel, Base

product_category = Table('product_category', Base.metadata,
    Column('product_id', String(60), ForeignKey('products.id')),
    Column('category_id', String(60), ForeignKey('categories.id'))
)

product_fabric = Table('product_fabric', Base.metadata,
    Column('product_id', String(60), ForeignKey('products.id')),
    Column('fabric_id', String(60), ForeignKey('fabrics.id'))
)

class Product(BaseModel):
    __tablename__ = "products"
    
    tailor_id = Column(String(60), ForeignKey('tailors.id'), nullable=False)
    name = Column(String(128), nullable=False)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=False)
    images = Column(NestedMutableJson, nullable=False)
    description = Column(String(400), nullable=False)
    estimated_tc = Column(Integer, nullable=False)
    colors = Column(NestedMutableJson, nullable=False)
    meta_data = Column(NestedMutableJson, nullable=True)
    image_cover_index = Column(Integer, default=0)

    tailor = relationship("Tailor", back_populates="products")
    reviews = relationship('Review', secondary='orders', viewonly=True, back_populates='product')
    orders = relationship("Order", back_populates="product")
    carts = relationship("CartItem", back_populates="product")

    fabrics = relationship("Fabric", secondary=product_fabric, back_populates="products")
    categories = relationship("Category", secondary=product_category, viewonly=True, back_populates="products")


class Category(BaseModel):
    __tablename__ = 'categories'

    parent_id = Column(String(60), nullable=True)
    name = Column(String(60), nullable=False, unique=True)
    products = relationship('Product', secondary=product_category, back_populates='categories')

class Fabric(BaseModel):
    __tablename__ = 'fabrics'
    name = Column(String(60), nullable=False, unique=True)

    products = relationship('Product', secondary=product_fabric, back_populates='fabrics')
