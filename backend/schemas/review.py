from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, TYPE_CHECKING
from decimal import Decimal
from datetime import datetime
from .user import UserSimpleResponse
from .watch import WatchSimpleResponse

# --- REVIEW (YORUMLAR) ---
class ReviewBase(BaseModel):
    rating: Decimal = Field(..., alias="Rating", ge=1, le=5)
    comment: Optional[str] = Field(None, alias="Comment")

class ReviewCreate(ReviewBase):
    watch_id: int = Field(..., alias="WatchID")

class ReviewUpdate(BaseModel):
    rating: Optional[Decimal] = Field(None, alias="Rating")
    comment: Optional[str] = Field(None, alias="Comment")

class ReviewResponse(ReviewBase):
    id: int = Field(..., alias="ReviewID")
    user_id: int = Field(..., alias="UserID")
    watch_id: int = Field(..., alias="WatchID")
    created_at: datetime = Field(..., alias="CreatedAt")
    
    user: Optional[UserSimpleResponse] = None 
    watch: Optional[WatchSimpleResponse] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
