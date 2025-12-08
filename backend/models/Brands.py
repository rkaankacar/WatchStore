from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database.session import Base


class brands(Base): #markalar
    __tablename__ = "brands"

    
    BrandID = Column(Integer, primary_key=True, index=True)
    BrandName = Column(String, unique=True, index=True, nullable=False)
    Country = Column(String, nullable=False)
    Description = Column(String, nullable=False)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # --- İLİŞKİ (Brands Tarafı) ---
    # Bir markanın birden fazla SAATİ olur (çoğul)
    watches = relationship("watches", back_populates="brand")
    