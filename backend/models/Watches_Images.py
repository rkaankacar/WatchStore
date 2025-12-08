from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database.session import Base
from sqlalchemy.sql import func

class watches_images(Base):
    __tablename__ = "watches_images"
    
    
    ImageID = Column(Integer, primary_key=True, index=True)
    ImageUrl = Column(String, nullable=False)
    CreatedAt =Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # --- Foreign Key ---
    WatchID = Column(Integer, ForeignKey("watches.WatchID",ondelete="CASCADE"), nullable=False)
    
    # --- İLİŞKİ (Watches_Images Tarafı) ---
    # Bir resmin bir SAATİ olur (tekil)
    watch = relationship("watches", back_populates="images")  