from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL, JSON
from sqlalchemy.orm import relationship
from backend.database.session import Base
from datetime import datetime

class payments(Base):
    __tablename__ = "payments"
    
    PaymentID = Column(Integer, primary_key=True, index=True)
    
    # --- İŞLEM DETAYLARI ---
    Amount = Column(DECIMAL(10, 2), nullable=False) # Tahsil edilen miktar
    PaymentDate = Column(DateTime, nullable=False, default=datetime.utcnow)
    Status = Column(String(50), nullable=False) # Successful, Failed, Refunded vb.
    
    # --- IYZICO ALANLARI (Doğrudan Iyzico'dan gelir) ---
    IyzicoRefId = Column(String(100), index=True, nullable=True) # Iyzico'dan dönen ödeme ID'si
    ConversationID = Column(String(100), index=True, nullable=False) # Backend'in ürettiği takip ID'si
    AuthCode = Column(String(50), nullable=True) # Yetkilendirme kodu
    RawResponse = Column(JSON, nullable=True) # Iyzico'dan dönen JSON cevabının tamamı
    
    # --- İLİŞKİLER ---
    # Her ödeme bir SİPARİŞİ fonlar (Foreign Key)
    OrderID = Column(Integer, ForeignKey("orders.OrderID"), nullable=False)
    order = relationship("orders", back_populates="payments")
    
    # Her ödemeyi bir KULLANICI dener (Foreign Key)
    UserID = Column(Integer, ForeignKey("users.UserID"), nullable=False) 
    # (Opsiyonel olarak users ilişkisi eklenebilir)