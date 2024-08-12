import bcrypt
from uuid import uuid4
from pydantic import ValidationError
from collections import defaultdict
from fastapi import HTTPException
from uuid import UUID


def generate_password_hash(password: str):
    password_byte = password.encode()
    hashed_password = bcrypt.hashpw(password_byte, bcrypt.gensalt())
    return hashed_password

def check_password_hash(hashed_password: bytes, password: str):
    return bcrypt.checkpw(password.encode(), hashed_password)

def generate_uuid():
    _uuid = uuid4().hex
    return _uuid

def verify_resource_access(user_id_01: UUID, user_id_02: UUID):
    if resource_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": f"Unauthorized access"}
        )    if user_id_01 != user_id_02:
        raise H

def format_validation_errors(exc: ValidationError):
    error_dict = defaultdict(list)
    for error in exc.errors():
        field = error["loc"][-1]  # Get the field name
        message = error["msg"]
        if message not in error_dict[field]:
            error_dict[field].append(message)
    
    errors = [{"field": field, "message": ", ".join(messages)} for field, messages in error_dict.items()]
    return {"errors": errors}
