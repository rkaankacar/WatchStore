from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from backend.database.session import Base
from sqlalchemy.sql import func


class reviews(Base):
    __tablename__ = "reviews"
    
    
    ReviewID = Column(Integer, primary_key=True, index=True)
    Rating = Column(DECIMAL, nullable=False)
    Comment = Column(String, nullable=True)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # --- Foreign Keys ---
    UserID = Column(Integer, ForeignKey("users.UserID"), nullable=False)
    WatchID = Column(Integer, ForeignKey("watches.WatchID",ondelete="CASCADE"), nullable=False)
    
    # --- İLİŞKİLER (Reviews Tarafı) ---
    # Bir yorumun bir KULLANICISI olur (tekil)
    user = relationship("users", back_populates="reviews")
    
    # Bir yorumun bir SAATİ olur (tekil)
    watch = relationship("watches", back_populates="reviews")