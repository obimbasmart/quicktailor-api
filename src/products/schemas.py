from pydantic import BaseModel, UUID4, computed_field, Field, EmailStr
from typing import List, Optional, Dict
from datetime import datetime
from src.storage.aws_s3_storage import s3_client
from src.reviews.schemas import ReviewItem

class Category(BaseModel):
    id: UUID4
    name: str


class TailorListInfo(BaseModel):
    id: UUID4
    brand_name: str | None
    photo: str | None
    is_available: bool

    class Config:
        from_attributes = True

class TailorListItem(BaseModel):
    id: str = UUID4
    brand_name: str | None
    photo: str | None
    is_verified: bool
    is_available: bool
    categories: List[Category] = []


    @computed_field
    @property
    def no_products(self) -> int:
        return 0

    @computed_field
    @property
    def no_reviews(self) -> int:
        return 0

    @computed_field
    @property
    def avg_rating(self) -> float:
        return 0.0

    class Config:
        from_attributes = True


class ProductItem(BaseModel):
    id: UUID4
    name: str
    price: float
    description: str
    images: List[Dict] = Field(exclude=True)
    categories: List[Category]
    tailor: TailorListItem | None
    reviews: List[ReviewItem] = Field(max_length=2)

    @computed_field
    @property
    def p_images(self) -> List:
        return s3_client.generate_presigned_urls('get_object', self.images)
    


class ProductListItem(BaseModel):
    id: UUID4
    name: str
    price: float
    image: Dict
    images: List[Dict] = Field(exclude=True)
    image_cover_index: int = Field(exclude=True, default=0)
    tailor: TailorListInfo | None
    type: str


    @computed_field
    @property
    def average_rating(self) -> float:
        return 0.0
    
    

    class Config:
        from_attributes = True

class ProductUpload(BaseModel):
    name: str
    price: float
    description: str
    duration: int
    is_active: bool = Field(default=True)
    categories: List[str]
    images: List = Field(..., max_length=6, min_length=2)
    image_cover_index: int = Field(ge=0, le=6, default=0)

    class Config:
        extra = 'forbid'



class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    estimated_tc: Optional[int] = None
    is_active: Optional[bool] = None
    colors: Optional[List[str]] = None
    categories: Optional[List[str]] = None
    images: Optional[List[str]] = Field(default=None, max_length=4, min_length=2)
    image_cover_index: Optional[int] = Field(ge=0, le=4, default=0)

    class Config:
        extra = 'forbid'


class Location(BaseModel):
    state: str
    city: str
    address: str

class ProductTailorItem(TailorListInfo):
    first_name: str
    last_name: str
    is_verified: bool
    # tailor: object = Field(exclude=True)
    address: Location | None

    @computed_field
    @property
    def no_reviews(self) -> int:
        # return len(self.tailor.reviews)
        return 0
    
    @computed_field
    @property
    def avg_review(self) -> float:
        # return  self.tailor.reviews.rating .....
        return 0.0

class CreateCustomCode(BaseModel):
    deal: str
    unit: str
    value: float
    email: EmailStr = Field(alias="customer_email")
    limit: int = Field(default=1)
    start_date: datetime
    expires_in: datetime = Field(alias='end_date')
