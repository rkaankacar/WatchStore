from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .watch import WatchSimpleResponse

# --- BRAND BASE ---
class BrandBase(BaseModel):
    name: str = Field(..., alias="BrandName")
    country: str = Field(..., alias="Country")
    description: str = Field(..., alias="Description")

class BrandCreate(BrandBase):
    pass

class BrandUpdate(BrandBase):
    name: Optional[str] = Field(None, alias="BrandName")
    country: Optional[str] = Field(None, alias="Country")
    description: Optional[str] = Field(None, alias="Description")

class BrandSimpleResponse(BrandBase):
    id: int = Field(..., alias="BrandID")
    created_at: datetime = Field(..., alias="CreatedAt")
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class BrandResponse(BrandSimpleResponse):
    watches: List["WatchSimpleResponse"] = []
