from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from .user import UserSimpleResponse
from .watch import WatchSimpleResponse

class FavoriteCreate(BaseModel):
    watch_id: int

class FavoriteResponse(BaseModel):
    FavoriteID: int = Field(..., alias="FavoriteID") 
    
    UserID: int
    WatchID: int
    
    user: Optional[UserSimpleResponse] = None 
    watch: Optional[WatchSimpleResponse] = None 
    
    model_config = ConfigDict(
        from_attributes=True, 
        populate_by_name=True
    )
