from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from database.session import Base



class Reviews(Base):
    __tablename__ = "Reviews"
    
    ReviewID = Column(Integer, primary_key=True, index=True)
    Rating = Column(DECIMAL, nullable=False)
    Comment = Column(String, nullable=True)
    CreatedAt = Column(DateTime, nullable=False)
    
    # --- Foreign Keys ---
    UserID = Column(Integer, ForeignKey("Users.UserID"), nullable=False)
    WatchID = Column(Integer, ForeignKey("Watches.WatchID"), nullable=False)
    
    # --- İLİŞKİLER (Reviews Tarafı) ---
    # Bir yorumun bir KULLANICISI olur (tekil)
    user = relationship("Users", back_populates="reviews")
    
    # Bir yorumun bir SAATİ olur (tekil)
    watch = relationship("Watches", back_populates="reviews")