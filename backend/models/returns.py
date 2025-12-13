from sqlalchemy import Column, Integer, String, DateTime,ForeignKey, Text
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database.session import Base



class returns(Base):
    __tablename__ = "returns"

    ReturnID = Column(Integer, primary_key=True, index=True)
    OrderID = Column(Integer, ForeignKey("orders.OrderID"))
    UserID = Column(Integer, ForeignKey("users.UserID"))
    
    # Talep Tipi: "İade" veya "Değişim"
    RequestType = Column(String(20), nullable=False) 
    
    # Neden: "Kusurlu Ürün", "Beden Uymadı", "Vazgeçtim" vb.
    Reason = Column(String(255), nullable=False)
    Description = Column(Text, nullable=True) # Müşterinin detaylı notu
    
    # Durum: "Beklemede", "Onaylandı", "Reddedildi", "Tamamlandı"
    Status = Column(String(50), default="Beklemede")
    
    CreatedAt = Column(DateTime, default=datetime.now)
    
    # İlişkiler
    order = relationship("orders", back_populates="returns")
    user = relationship("users")