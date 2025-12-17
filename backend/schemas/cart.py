from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from .watch import WatchSimpleResponse

# --- CART (SEPET) ---
class CartBase(BaseModel):
    quantity: int = Field(..., alias="Quantity", gt=0)

class CartCreate(CartBase):
    watch_id: int = Field(..., alias="WatchID")

class CartUpdate(BaseModel):
    quantity: int = Field(..., alias="Quantity", gt=0)

class CartResponse(CartBase):
    id: int = Field(..., alias="CartID")
    user_id: int = Field(..., alias="UserID")
    watch_id: int = Field(..., alias="WatchID")

    watch: Optional[WatchSimpleResponse] = None
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
