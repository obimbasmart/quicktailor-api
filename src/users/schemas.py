from pydantic import BaseModel, UUID4, Field, computed_field, EmailStr, ConfigDict, field_validator
from src.auth.schemas import BaseUser
from typing import Union, List, Optional
import re
from .constants import VALID_MEASUREMENT_NAMES
from models import Gender
from src.tailors.schemas import  TailorListItem
from src.products.schemas import ProductItem

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

class FemaleMeasurementInfo(BaseModel):
    burst: float
    waist: float
    hips: float
    full_length: float
    shoulder: float
    half_length: float
    round_sleeve: float
    neck: float

class MaleMeasurementInfo(BaseModel):
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

class MeasurementUpdate(BaseModel):
    measurement_type: Gender = "MALE"
    shoulder: Optional[float] = None
    waist: Optional[float] = None
    neck: Optional[float] = None
    chest_burst: Optional[float] = None
    stomach: Optional[float] = None
    top_length: Optional[float] = None
    sleeve_length: Optional[float] = None
    muscle: Optional[float] = None
    laps: Optional[float] = None
    hips: Optional[float] = None
    knee: Optional[float] = None
    burst: Optional[float] = None
    full_length: Optional[float] = None
    half_length: Optional[float] = None
    round_sleeve: Optional[float] = None
   
    class Config:
        json_encoders = {
        Gender: lambda v: v.value
        }
        extra='forbid'


class UpdateFields(BaseModel):
    password: str = Field(None, pattern=r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')
    username: str = Field(None, pattern=r'^[A-Za-z][A-Za-z0-9_]{3,20}$')
    email: str = None
    phone: str = Field(None, max_length=11)
    gender: Gender | None = None
    address: Optional[Location] = None

    class Config:
        extra='forbid'
        regex_engine='python-re'


class FavoriteResponse(BaseModel):
    tailors: list[TailorListItem]
    products: list[ProductItem]

class AddFavorite(BaseModel):
    tailor_id: Optional[str] = None
    product_id: Optional[str] =  None

