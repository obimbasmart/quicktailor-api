from pydantic import BaseModel, UUID4

class Category(BaseModel):
    id: UUID4
    name: str