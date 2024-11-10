from pydantic import BaseModel, UUID4, computed_field, EmailStr, Field
from typing import List, Union
from src.products.schemas import Category
from typing import Optional, Dict
from datetime import date
from models import Gender
from datetime import datetime
from src.storage.aws_s3_storage import s3_client

class Location(BaseModel):
    state: str
    city: str
    address: str

class BankDetails(BaseModel):
    bank_name: str
    account_number: str
    account_name: Optional[str] = None

class TailorListItem(BaseModel):
    id: str = UUID4
    brand_name: str | None
    photo: str | None
    is_verified: bool
    is_available: bool
    categories: List[Category] = []
    type: str


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

class TailorItem(TailorListItem):
    # first_name: str
    # last_name: str
    email: EmailStr
    is_enabled: bool
    # phone: str
    about: str | None
    address: Location | None
    type: str

    @computed_field
    @property
    def no_completed_jobs(self) -> int:
        return 0
    
class TailorProductListItem(BaseModel):
    id: UUID4
    name: str
    price: float
    image_cover_index: int = Field(exclude=True, default=0)
    image: Dict
    created_at: datetime

class TailorProductItem(BaseModel):
    id: UUID4
    name: str
    price: float
    description: str
    images: List = Field(exclude=True, default=[])
    created_at: datetime
    is_active: bool
    is_published: bool
    categories: List

    @computed_field
    @property
    def p_images(self) -> List:
        return s3_client.generate_presigned_urls('get_object', self.images)
    


class UpdateTailor(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    brand_name: Optional[str] = None
    photo: Optional[str] = None
    about: Optional[str] = None
    location: Optional[Location] = None
    bank_details: Optional[BankDetails] = None
    push_notification: Optional[bool] = None
    email_notification: Optional[bool] = None
    location_access: Optional[bool] = None
    type: Optional[str] = None

    class Config:
        extra = 'forbid'

class UpdateTailorType(BaseModel):
    type: str = Union['TAILOR', 'SHOEMAKER']
    class Config:
        extra = 'forbid'

class VerificationInfo(BaseModel):
    first_name: str
    last_name: str
    DOB: date
    gender: Gender
    vNIN: str