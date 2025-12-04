from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.session import Base


class Watches_Images(Base):
    __tablename__ = "Watches_Images"
    
    ImageID = Column(Integer, primary_key=True, index=True)
    ImageUrl = Column(String, nullable=False)
    CreatedAt = Column(DateTime, nullable=False)
    
    # --- Foreign Key ---
    WatchID = Column(Integer, ForeignKey("Watches.WatchID"), nullable=False)
    
    # --- İLİŞKİ (Watches_Images Tarafı) ---
    # Bir resmin bir SAATİ olur (tekil)
    watch = relationship("Watches", back_populates="images")  