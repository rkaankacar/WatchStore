from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from database.session import Base



class Orders(Base):
    __tablename__="Orders"
    
    OrderID = Column(Integer, primary_key=True, index=True)
    OrderDate = Column(DateTime, nullable=False)
    TotalAmount = Column(DECIMAL, nullable=False)
    Status = Column(String, nullable=False)
    ShippingAddress = Column(String, nullable=False)
    
    # --- Foreign Key ---
    UserID = Column(Integer, ForeignKey("Users.UserID"), nullable=False)
    
    # --- İLİŞKİLER (Orders Tarafı) ---
    # Bir siparişin bir KULLANICISI olur (tekil)
    user = relationship("Users", back_populates="orders")
    
    # Bir siparişin birden fazla SİPARİŞ DETAYI olur (çoğul)
    order_details = relationship("OrdersDetails", back_populates="order")