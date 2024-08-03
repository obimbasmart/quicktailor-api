from pydantic import BaseModel, UUID4, Field, computed_field, EmailStr, root_validator, validator
from typing import Union, List, Optional
import re


class Location(BaseModel):
    state: str
    city: str
    address: str

class UserInfo(BaseModel):
    id: str = UUID4
    username: str 
    email: EmailStr
    phone: str
    gender: str | None
    address: Location | None
    is_online: bool
    email_is_verified: bool

class SuccessMsg(BaseModel):
    message: str
from pydantic import BaseModel, EmailStr, Field, root_validator, validator
from typing import Optional

class Location(BaseModel):
    # Define your Location model here
    pass

class UpdateFields(BaseModel):
    username: Optional[str] = Field(None, pattern=r'^[A-Za-z][A-Za-z0-9_]{3,20}$')
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=11)
    gender: Optional[str] = None
    address: Optional[Location] = None
    password: Optional[str] = None

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
