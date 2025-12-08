from sqlalchemy import Column, Integer, String, DateTime, DECIMAL,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database.session import Base

class watches(Base): #saatler
    
    __tablename__ = "watches"
    
    
    WatchID = Column(Integer, primary_key=True, index=True)
    ModelName = Column(String, nullable=False)
    Gender = Column(String, nullable=False)
    CaseMaterial = Column(String, nullable=False)
    StrapMaterial = Column(String, nullable=False)
    MovementType = Column(String, nullable=False)
    WaterResistance = Column(String, nullable=False)
    Description = Column(String, nullable=True)
    Price = Column(DECIMAL, nullable=False)
    Stock = Column(Integer, nullable=False)
    ImageUrl = Column(String, nullable=False) # Bu ana resim sanırım
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # --- Foreign Keys ---
    BrandID = Column(Integer, ForeignKey("brands.BrandID"), nullable=False)
    
    # --- İLİŞKİLER (Watches Tarafı) ---
    # Bir saatin bir MARKASI olur (tekil)
    brand = relationship("brands", back_populates="watches")
    
    # Bir saatin birden fazla RESMİ olur (çoğul)
    images = relationship("watches_images", back_populates="watch")
    
    # Bir saatin birden fazla YORUMU olur (çoğul)
    reviews = relationship("reviews", back_populates="watch")
    
    # Bir saat, birden fazla SEPET ÖĞESİNDE bulunabilir (çoğul)
    cart_items = relationship("cart", back_populates="watch")
    
    # Bir saat, birden fazla SİPARİŞ DETAYINDA bulunabilir (çoğul)
    order_details = relationship("ordersdetails", back_populates="watch")
    
    favorite_items = relationship("favorites", back_populates="watch")