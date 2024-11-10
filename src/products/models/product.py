from sqlalchemy import Boolean, Column, String, Enum, ForeignKey, Float, Table, Integer
from sqlalchemy_json import NestedMutableJson
from sqlalchemy.orm import relationship
from models import BaseModel, Base
from models import ProductType
from src.storage.aws_s3_storage import s3_client

    
product_category = Table('product_category', Base.metadata,
    Column('product_id', String(60), ForeignKey('products.id')),
    Column('category_id', String(60), ForeignKey('categories.id'))
)


class Product(BaseModel):
    __tablename__ = "products"
    
    tailor_id = Column(String(60), ForeignKey('tailors.id'), nullable=False)
    name = Column(String(128), nullable=False)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=False)
    is_published = Column(Boolean, default=False)
    images = Column(NestedMutableJson, nullable=False)
    description = Column(String(400), nullable=False)
    duration = Column(Integer, nullable=False)
    type = Column(Enum(ProductType), nullable=True, default=ProductType.cloth)

    meta_data = Column(NestedMutableJson, nullable=True)
    image_cover_index = Column(Integer, default=0)

    tailor = relationship("Tailor", back_populates="products")
    reviews = relationship('Review', secondary='orders', viewonly=True, back_populates='product')
    orders = relationship("Order", back_populates="product")
    carts = relationship("CartItem", back_populates="product")
    categories = relationship("Category", secondary=product_category, viewonly=True, back_populates="products")

    @property
    def image(self) -> dict:
        cover_image = self.images[self.image_cover_index]
        print("oleg",cover_image)
        return s3_client.generate_presigned_url('get_object',
                                                cover_image['url'],
                                                width=cover_image['width'],
                                                height=cover_image['height'],
                                                aspect_ratio=cover_image['width']/cover_image['height'])


class Category(BaseModel):
    __tablename__ = 'categories'

    parent_id = Column(String(60), nullable=True)
    name = Column(String(60), nullable=False, unique=True)
    products = relationship('Product', secondary=product_category, back_populates='categories')
