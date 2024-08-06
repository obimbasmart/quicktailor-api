from pydantic import BaseModel, UUID4, Field, computed_field, EmailStr, root_validator, validator
from typing import Union, List, Optional
import re
from .constants import VALID_MEASUREMENT_NAMES

class Location(BaseModel):
    state: str
    city: str
    address: str

class SuccessMsg(BaseModel):
    message: str

class BaseOptional(BaseModel):
    @root_validator(pre=True)
    def check_fields(cls, values):
        valid_fields = set(cls.__fields__.keys())
        provided_fields = set(values.keys())
        if not provided_fields.issubset(valid_fields):
            invalid_fields = provided_fields - valid_fields
            raise ValueError(f"Invalid fields provided: {', '.join(invalid_fields)}")
        if not any(values.values()):
            raise ValueError("At least one field must be provided for update")
        return values


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
class KidMeasurementInfo(BaseModel):
    waist: float
    neck: float

class MeasurementUpdate(BaseOptional):
    measurement_type: str = "male"
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


class UpdateFields(BaseOptional):
    username: Optional[str] = Field(None, pattern=r'^[A-Za-z][A-Za-z0-9_]{3,20}$')
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=11)
    gender: Optional[str] = None
    address: Optional[Location] = None
    password: Optional[str] = None

    @validator('gender')
    def validate_gender(cls, v):
        if v and v not in ['male', 'female', 'other']:
            raise ValueError("Gender must be 'male', 'female', or 'other'")
        return v

    @validator('password')
    def validate_password(cls, v):
        if v:
            if len(v) < 8:
                raise ValueError("Password must be at least 8 characters long")
            if not any(c.islower() for c in v):
                raise ValueError("Password must contain at least one lowercase letter")
            if not any(c.isupper() for c in v):
                raise ValueError("Password must contain at least one uppercase letter")
            if not any(c.isdigit() for c in v):
                raise ValueError("Password must contain at least one digit")
            if not any(c in "@$#!%*?&" for c in v):
                raise ValueError("Password must contain at least one special character (@$!%*?&)")
        return v


    @validator('phone')
    def phone_valid(cls, v):
        if v and not v.isdigit():
            raise ValueError('Phone number must contain only digits')
        return v
