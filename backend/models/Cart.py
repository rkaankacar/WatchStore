from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from backend.database.session import Base




class cart(Base):
    __tablename__ = "cart"
    
    
    CartID = Column(Integer, primary_key=True, index=True)
    Quantity = Column(Integer, nullable=False)
    
    # --- Foreign Keys ---
    UserID = Column(Integer, ForeignKey("users.UserID"), nullable=False)
    WatchID = Column(Integer, ForeignKey("watches.WatchID",ondelete="CASCADE"), nullable=False)
    
    # --- İLİŞKİLER (Cart Tarafı) ---
    # Bu sepet öğesi bir KULLANICIYA aittir (tekil)
    user = relationship("users", back_populates="cart_items")
    
    # Bu sepet öğesi bir SAATE aittir (tekil)
    watch = relationship("watches", back_populates="cart_items")