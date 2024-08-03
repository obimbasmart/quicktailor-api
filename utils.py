import bcrypt
from uuid import uuid4
from pydantic import ValidationError
from fastapi import Depends
from dependencies import get_db


def generate_password_hash(password: str):
    password_byte = password.encode()
    hashed_password = bcrypt.hashpw(password_byte, bcrypt.gensalt())
    return hashed_password

def check_password_hash(hashed_password: bytes, password: str):
    return bcrypt.checkpw(password.encode(), hashed_password)

def generate_uuid():
    _uuid = uuid4().hex
    return _uuid

from collections import defaultdict

def format_validation_errors(exc: ValidationError):
    error_dict = defaultdict(list)
    for error in exc.errors():
        field = error["loc"][-1]  # Get the field name
        message = error["msg"]
        if message not in error_dict[field]:
            error_dict[field].append(message)
    
    errors = [{"field": field, "message": ", ".join(messages)} for field, messages in error_dict.items()]
    return {"errors": errors}
