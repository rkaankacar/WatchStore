from sqlalchemy import Column, Integer, String, DateTime,func
from sqlalchemy.orm import relationship
from database.session import Base


class Users(Base):
    
    __tablename__ = "Users"
     
    UserID = Column(Integer, primary_key=True, index=True)
    FullName = Column(String, nullable=False)
    Email = Column(String, unique=True, index=True, nullable=False)
    Password = Column(String, nullable=False)
    Phone = Column(String, unique=True, index=True, nullable=True)
    Address = Column(String, nullable=True)
    City = Column(String, nullable=True)
    Country = Column(String, nullable=True)
    Role = Column(String, nullable=False)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now(),nullable=False)
    
    # --- İLİŞKİLER (Users Tarafı) ---
    # Bir kullanıcının birden fazla SİPARİŞİ olur (çoğul)
    orders = relationship("Orders", back_populates="user")
    
    # Bir kullanıcının birden fazla YORUMU olur (çoğul)
    reviews = relationship("Reviews", back_populates="user")
    
    # Bir kullanıcının sepetinde birden fazla ÖĞE olur (çoğul)
    cart_items = relationship("Cart", back_populates="user")
