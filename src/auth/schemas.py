from pydantic import BaseModel, EmailStr, Field
from typing import Dict, Any
from uuid import UUID


class BaseUser(BaseModel):
  email: EmailStr
  phone: str = Field(max_length=11)
  password: str = Field(..., pattarn=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
  password_2: str

class UserRegIn(BaseUser):
  username: str = Field(..., pattern=r'^[A-Za-z][A-Za-z0-9_]{3,20}$')

class TailorRegIn(BaseUser):
  first_name: str = Field(..., pattern=r'^[A-Za-z][A-Za-z0-9_]{4,20}$')
  last_name: str = Field(..., pattern=r'^[A-Za-z][A-Za-z0-9_]{4,20}$')


class Login(BaseModel):
  email: EmailStr
  password: str

class LoginResponse(BaseModel):
  access_token: str
  data: Dict[str, UUID]
  
class BaseResponse(BaseModel):
  message: str
