from pydantic import BaseModel, UUID4, Field, computed_field, EmailStr
from typing import Union, List
from src.products.schemas import Category
from typing import Optional

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
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    about: str | None
    address: Location | None

    @computed_field
    @property
    def no_completed_jobs(self) -> int:
        return 0


class UpdateTailor(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    brand_name: Optional[str] = None
    location: Optional[Location] = None
    bank_details: Optional[BankDetails] = None
    push_notification: Optional[bool] = None
    email_notification: Optional[bool] = None
    location_access: Optional[bool] = None

    class Config:
        extra = 'forbid'