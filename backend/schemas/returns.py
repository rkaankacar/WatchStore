from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from .order import OrderResponse

class ReturnBase(BaseModel):
    order_id: int = Field(..., alias="OrderID")
    order_detail_id: Optional[int] = Field(None, alias="OrderDetailID")
    request_type: str = Field(..., alias="RequestType") 
    reason: str = Field(..., alias="Reason") 
    description: Optional[str] = Field(None, alias="Description")

class ReturnCreate(ReturnBase):
    pass 

class ReturnUpdate(BaseModel):
    status: Optional[str] = Field(None, alias="Status")

class ReturnResponse(ReturnBase):
    id: int = Field(..., alias="ReturnID")
    user_id: int = Field(..., alias="UserID")
    user_name: Optional[str] = Field(None, alias="UserName")
    status: str = Field(..., alias="Status")
    created_at: datetime = Field(..., alias="CreatedAt")
    description: Optional[str] = Field(None, alias="Description")

    order: Optional[OrderResponse] = None 

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
