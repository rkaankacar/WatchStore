from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from backend.database.session import Base  # <--- Base'i import et

class favorites(Base):  # <--- (Base) EKLENDİ!
    __tablename__ = "favorites"
    
    
    FavoriteID = Column("favoriteid",Integer, primary_key=True, index=True)
    UserID = Column(Integer, ForeignKey("users.UserID"), nullable=False)
    WatchID = Column(Integer, ForeignKey("watches.WatchID",ondelete="CASCADE"), nullable=False)
    
    # --- İLİŞKİLER ---
    user = relationship("users", back_populates="favorite_items")
    watch = relationship("watches", back_populates="favorite_items")