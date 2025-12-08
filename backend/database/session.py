# project_name/database/session.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import MetaData
from backend.core.config import settings  # config dosyasından import

# --- SQLAlchemy Temelleri ---

# 1. Base Sınıfı Tanımı
class Base(DeclarativeBase):
    """Veritabanı Modelleri için ana sınıf."""
    metadata = MetaData(schema=settings.SCHEMA_NAME) 

# 2. Asenkron Motor (Engine)
async_engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=True, 
)

# 3. Asenkron Oturum Fabrikası (Session Maker)
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession, 
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

# ⚠️ ÖNEMLİ NOT:
# Tüm ORM modelleriniz (örneğin models/user.py) artık
# from database.session import Base
# şeklinde bu dosyadan Base sınıfını import etmelidir.