from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from backend.database.session import Base



class orders(Base):
    __tablename__="orders"

    
    OrderID = Column(Integer, primary_key=True, index=True)
    OrderDate = Column(DateTime, nullable=False)
    TotalAmount = Column(DECIMAL, nullable=False)
    Status = Column(String, nullable=False)
    ShippingAddress = Column(String, nullable=False)
   # PaymentID = Column(String(100), index=True, nullable=True)
   # ConversationID = Column(String(100), index=True, nullable=True)
    # --- Foreign Key ---
    UserID = Column(Integer, ForeignKey("users.UserID"), nullable=False)
    
    # --- İLİŞKİLER (Orders Tarafı) ---
    # Bir siparişin bir KULLANICISI olur (tekil)
    user = relationship("users", back_populates="orders")
    
    # Bir siparişin birden fazla SİPARİŞ DETAYI olur (çoğul)
    order_details = relationship("ordersdetails", back_populates="order")
    
    payments = relationship("payments", back_populates="order")