from pydantic import BaseModel, UUID4, Field, EmailStr, computed_field
from typing import Optional, List
from models import Gender
from src.tailors.schemas import TailorListItem
from src.products.schemas import ProductItem
from datetime import datetime


class PasswordReset(BaseModel):
    password: str
    password_2: str

class Location(BaseModel):
    state: str
    city: str
    address: str


class SuccessMsg(BaseModel):
    message: str


class UserInfo(BaseModel):
    id: str = UUID4
    username: str
    email: EmailStr
    phone: str
    gender: str | None
    address: Location | None
    is_online: bool
    email_is_verified: bool



class FemaleMeasurement(BaseModel):
    burst: float
    waist: float
    hips: float
    full_length: float
    shoulder: float
    half_length: float
    round_sleeve: float
    neck: float


class MaleMeasurement(BaseModel):
    chest_burst: float
    stomach: float
    top_length: float
    sleeve_length: float
    shoulder: float
    muscle: float
    waist: float
    neck: float
    laps: float
    knee: float


class MeasurementItem(BaseModel):
    male: MaleMeasurement
    female: FemaleMeasurement


class MeasurementUpdate(MeasurementItem):
    male: Optional[MaleMeasurement] = None
    female: Optional[FemaleMeasurement] = None
    


class UpdateUserFields(BaseModel):
    username: str = Field(None, pattern=r'^[A-Za-z][A-Za-z0-9_]{3,20}$')
    phone: str = Field(None, max_length=11)
    gender: Gender | None = None
    address: Optional[Location] = None

    class Config:
        extra = 'forbid'
        regex_engine = 'python-re'


class Favorites(BaseModel):
    tailors: list[TailorListItem]
    products: list[ProductItem]


class AddFavorite(BaseModel):
    tailor_id: Optional[str] = None
    product_id: Optional[str] = None
