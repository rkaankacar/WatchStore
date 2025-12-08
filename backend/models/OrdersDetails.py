from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from backend.database.session import Base



class ordersdetails(Base):
    __tablename__ = "orderdetails"
    
    
    OrderDetailID = Column(Integer, primary_key=True, index=True)
    Quantity = Column(Integer, nullable=False)
    UnitPrice = Column(DECIMAL, nullable=False) # O anki birim fiyatı
    
    # --- Foreign Keys ---
    OrderID = Column(Integer, ForeignKey("orders.OrderID"), nullable=False)
    WatchID = Column(Integer, ForeignKey("watches.WatchID",ondelete="CASCADE"), nullable=False)
    
    # --- İLİŞKİLER (OrdersDetails Tarafı) ---
    # Bu detay, bir SİPARİŞE aittir (tekil)
    order = relationship("orders", back_populates="order_details")
    
    # Bu detay, bir SAATE aittir (tekil)
    watch = relationship("watches", back_populates="order_details")