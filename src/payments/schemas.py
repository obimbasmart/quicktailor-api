from pydantic import BaseModel, EmailStr
from typing import List, Dict

class PaystackWebhookPayload(BaseModel):
    event: str
    data: dict

class CheckOut(BaseModel):
    cart: List[str]

    class Config:
        extra = 'forbid'

class InitPayment(BaseModel):
    amount: float
    email: EmailStr
    reference: str
    metadata: Dict