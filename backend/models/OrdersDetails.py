from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from database.session import Base



class OrdersDetails(Base):
    __tablename__ = "OrderDetails"
    
    OrderDetailID = Column(Integer, primary_key=True, index=True)
    Quantity = Column(Integer, nullable=False)
    UnitPrice = Column(DECIMAL, nullable=False) # O anki birim fiyatı
    
    # --- Foreign Keys ---
    OrderID = Column(Integer, ForeignKey("Orders.OrderID"), nullable=False)
    WatchID = Column(Integer, ForeignKey("Watches.WatchID"), nullable=False)
    
    # --- İLİŞKİLER (OrdersDetails Tarafı) ---
    # Bu detay, bir SİPARİŞE aittir (tekil)
    order = relationship("Orders", back_populates="order_details")
    
    # Bu detay, bir SAATE aittir (tekil)
    watch = relationship("Watches", back_populates="order_details")