from pydantic import BaseModel

class ErrorResponse(BaseModel):
  detail: str

class MissingFieldResponse(BaseModel):
  errors: list