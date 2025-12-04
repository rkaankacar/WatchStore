from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from database.session import Base




class Cart(Base):
    __tablename__ = "Cart"
    
    CartID = Column(Integer, primary_key=True, index=True)
    Quantity = Column(Integer, nullable=False)
    
    # --- Foreign Keys ---
    UserID = Column(Integer, ForeignKey("Users.UserID"), nullable=False)
    WatchID = Column(Integer, ForeignKey("Watches.WatchID"), nullable=False)
    
    # --- İLİŞKİLER (Cart Tarafı) ---
    # Bu sepet öğesi bir KULLANICIYA aittir (tekil)
    user = relationship("Users", back_populates="cart_items")
    
    # Bu sepet öğesi bir SAATE aittir (tekil)
    watch = relationship("Watches", back_populates="cart_items")