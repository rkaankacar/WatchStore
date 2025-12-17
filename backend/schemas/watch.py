from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from decimal import Decimal
from .brand import BrandSimpleResponse

if TYPE_CHECKING:
    from .review import ReviewResponse

# --- WATCH IMAGE BASE ---
class WatchImageBase(BaseModel):
    image_url: str = Field(..., alias="ImageUrl")

class WatchImageCreate(WatchImageBase):
    watch_id: int = Field(..., alias="WatchID")

class WatchImageUpdate(BaseModel):
    image_url: Optional[str] = Field(None, alias="ImageUrl")

class WatchImageSimpleResponse(WatchImageBase):
    id: int = Field(..., alias="ImageID")
    watch_id: int = Field(..., alias="WatchID")
    created_at: datetime = Field(..., alias="CreatedAt")
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

# --- WATCH BASE & SIMPLE ---
class WatchBase(BaseModel):
    model_name: str = Field(..., alias="ModelName")
    gender: str = Field(..., alias="Gender")
    case_material: str = Field(..., alias="CaseMaterial")
    strap_material: str = Field(..., alias="StrapMaterial")
    movement_type: str = Field(..., alias="MovementType")
    water_resistance: str = Field(..., alias="WaterResistance")
    description: Optional[str] = Field(None, alias="Description")
    price: Decimal = Field(..., alias="Price", gt=0)
    stock: int = Field(..., alias="Stock", ge=0)
    image_url: str = Field(..., alias="ImageUrl")

class WatchCreate(WatchBase):
    brand_id: int = Field(..., alias="BrandID")

class WatchUpdate(BaseModel):
    model_name: Optional[str] = Field(None, alias="ModelName")
    price: Optional[Decimal] = Field(None, alias="Price", gt=0)
    stock: Optional[int] = Field(None, alias="Stock", ge=0)
    brand_id: Optional[int] = Field(None, alias="BrandID")
    image_url: Optional[str] = Field(None, alias="ImageUrl")

class WatchSimpleResponse(WatchBase):
    id: int = Field(..., alias="WatchID")
    brand_id: int = Field(..., alias="BrandID")
    created_at: datetime = Field(..., alias="CreatedAt")
    
    brand: Optional[BrandSimpleResponse] = None
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class WatchResponse(WatchSimpleResponse):
    images: List[WatchImageSimpleResponse] = []
    reviews: List["ReviewResponse"] = []
