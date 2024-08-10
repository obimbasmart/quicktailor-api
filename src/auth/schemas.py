from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator, ValidationInfo, model_validator
from typing import Dict, Any
from uuid import UUID


class BaseUser(BaseModel):
    model_config = ConfigDict(regex_engine='python-re')

    email: EmailStr
    phone: str = Field(max_length=11)
    password: str = Field(
        ..., pattern=r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')
    password_2: str

    @model_validator(mode='after')
    def check_passwords_match(self):
        if self.password != self.password_2:
            raise ValueError('passwords do not match')
        return self


class UserRegIn(BaseUser):
    username: str = Field(..., pattern=r'^[A-Za-z][A-Za-z0-9_]{4,20}$')
    # class Config:
    #   extra = 'forbid'


class TailorRegIn(BaseUser):
    first_name: str = Field(..., pattern=r'^[A-Za-z][A-Za-z0-9_]{3,20}$')
    last_name: str = Field(..., pattern=r'^[A-Za-z][A-Za-z0-9_]{3,20}$')

    class Config:
        extra = 'forbid'


class AdminRegIn(BaseUser):
    sso: str

class Login(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    data: Dict[str, UUID]


class BaseResponse(BaseModel):
    message: str
