from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.session import Base


class Favorites:
    __tablename__ = "favorites"
    
    favoriteID = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, ForeignKey("Users.UserID"), nullable=False)
    WatchID = Column(Integer, ForeignKey("Watches.WatchID"), nullable=False)
    
    # --- İLİŞKİLER (Favorites Tarafı) ---
    user = relationship("Users", back_populates="favorite_items")
    watch = relationship("Watches", back_populates="favorite_items")