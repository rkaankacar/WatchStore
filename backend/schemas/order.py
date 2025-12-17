from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, TYPE_CHECKING
from decimal import Decimal
from datetime import datetime
from .user import UserSimpleResponse
from .watch import WatchSimpleResponse

# --- ORDER DETAILS ---
class OrderDetailBase(BaseModel):
    quantity: int = Field(..., alias="Quantity", gt=0)
    unit_price: Decimal = Field(..., alias="UnitPrice", ge=0)

class OrderDetailCreate(OrderDetailBase):
    watch_id: int = Field(..., alias="WatchID")

class OrderDetailUpdate(BaseModel):
    quantity: Optional[int] = Field(None, alias="Quantity")

class OrderDetailResponse(OrderDetailBase):
    id: int = Field(..., alias="OrderDetailID")
    order_id: int = Field(..., alias="OrderID")
    watch_id: int = Field(..., alias="WatchID")

    watch: Optional[WatchSimpleResponse] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

# --- ORDER (SİPARİŞ) ---
class OrderBase(BaseModel):
    total_amount: Decimal = Field(..., alias="TotalAmount") 
    status: str = Field(..., alias="Status")
    shipping_address: str = Field(..., alias="ShippingAddress")

class OrderCreate(OrderBase):
    user_id: int = Field(..., alias="UserID")

class OrderUpdate(BaseModel):
    Status: Optional[str]

class OrderResponse(OrderBase):
    id: int = Field(..., alias="OrderID")
    user_id: int = Field(..., alias="UserID")
    order_date: datetime = Field(..., alias="OrderDate")
    
    user: Optional[UserSimpleResponse] = None
    order_details: List[OrderDetailResponse] = []
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
