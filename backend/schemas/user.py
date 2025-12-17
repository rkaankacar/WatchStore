from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .order import OrderResponse
    from .review import ReviewResponse
    from .cart import CartResponse

# --- USER BASE & SIMPLE ---
class UserBase(BaseModel):
    full_name: str = Field(..., alias="FullName")
    email: EmailStr = Field(..., alias="Email")
    phone: Optional[str] = Field(None, alias="Phone")
    address: Optional[str] = Field(None, alias="Address")
    city: Optional[str] = Field(None, alias="City")
    country: Optional[str] = Field(None, alias="Country")
    role: str = Field(default="user", alias="Role")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, alias="Password")

class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, alias="FullName")
    email: Optional[EmailStr] = Field(None, alias="Email")
    phone: Optional[str] = Field(None, alias="Phone")
    address: Optional[str] = Field(None, alias="Address")
    city: Optional[str] = Field(None, alias="City")
    country: Optional[str] = Field(None, alias="Country")

class UserChangePassword(BaseModel):
    current_password: str 
    new_password: str 
    new_password_again: str 

class UserSimpleResponse(BaseModel):
    id: int = Field(..., alias="UserID")
    full_name: str = Field(..., alias="FullName")
    email: EmailStr = Field(..., alias="Email")
    phone: Optional[str] = Field(None, alias="Phone")
    address: Optional[str] = Field(None, alias="Address")
    city: Optional[str] = Field(None, alias="City")
    country: Optional[str] = Field(None, alias="Country")
    role: str = Field(..., alias="Role")
    created_at: datetime = Field(..., alias="CreatedAt")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        extra="ignore",
        ignored_types=(list, dict)
    )

class UserResponse(UserSimpleResponse):
    orders: List["OrderResponse"] = []
    reviews: List["ReviewResponse"] = []
    cart_items: List["CartResponse"] = []
