from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database.session import Base


class Brands(Base): #markalar
    __tablename__ = "Brands"
    
    BrandID = Column(Integer, primary_key=True, index=True)
    BrandName = Column(String, unique=True, index=True, nullable=False)
    Country = Column(String, nullable=False)
    Description = Column(String, nullable=False)
    CreatedAt = Column(DateTime, nullable=False)
    
    # --- İLİŞKİ (Brands Tarafı) ---
    # Bir markanın birden fazla SAATİ olur (çoğul)
    watches = relationship("Watches", back_populates="brand")
    