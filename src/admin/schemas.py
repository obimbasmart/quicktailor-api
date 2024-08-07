from pydantic import BaseModel, EmailStr, computed_field
from uuid import UUID
from datetime import datetime
from src.users.schemas import Location

class AdminTailorListItem(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    brand_name: str | None
    email: EmailStr
    photo: str | None
    is_verified: bool

class AdminUserListItem(BaseModel):
    id: UUID
    username: str
    email: EmailStr

class AdminTailorItem(AdminTailorListItem):
    phone: str
    address: Location | None
    created_at: datetime
    is_suspended: bool

    @computed_field
    @property
    def no_completed_orders(self) -> int:
        return 0
    
    @computed_field
    @property
    def no_rejected_orders(self) -> int:
        return 0
    
    @computed_field
    @property
    def no_pending_orders(self) -> float:
        return 0.0
