from sqlalchemy import Column, String,  Enum, Float, DateTime, BigInteger
from models import BaseModel
from enum import Enum as PyEnum
from sqlalchemy_json import NestedMutableJson


class PaymentStatus(PyEnum):
    failed = 'failed'
    success = 'success'
    ABANDONED = 'abandoned'
    ONGOING = 'ongoing'
    PENDING = 4
    REVERSED = 5
    QUEUED = 6


class Channel(PyEnum):
    bank_acount = "bank_account"
    transfer = "transfer"
    ussd = "ussd"
    card = "card"


class Currency(PyEnum):
    NGN = 'NGN'
    USD = 'USD'


class Payment(BaseModel):
    __tablename__ = "payments"

    transaction_id = Column(BigInteger, nullable=False)
    reference = Column(String(120), nullable=False)
    amount = Column(Float, nullable=False)
    paid_at = Column(DateTime)
    status = Column(Enum(PaymentStatus), nullable=False)
    channel = Column(Enum(Channel), nullable=False)
    currency = Column(Enum(Currency), nullable=False)
    customer_email = Column(String(128), nullable=False)
    customer_firstname = Column(String(128), nullable=True)
    customer_lastname = Column(String(128), nullable=True)
    meta_data = Column(NestedMutableJson, default={})
