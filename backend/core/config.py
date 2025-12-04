# backend/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Saat Satış API"
    VERSION: str = "1.0.0"

    # PostgreSQL bağlantısı
    ASYNC_DATABASE_URL: str = "postgresql+asyncpg://postgres:2004@localhost:5432/clockdatabase"

    # Şema ismi
    SCHEMA_NAME: str = "saat_satis"
    
    # --- EKLENEN KISIM (AUTH İÇİN ŞART) ---
    SECRET_KEY: str = "x9Kz2mP5qL8r" # JWT imzalama anahtarı
    ALGORITHM: str = "HS256" # Şifreleme algoritması
    # --------------------------------------

    class Config:
        env_file = ".env"  # Ortam değişkenleri buradan okunur (opsiyonel)
        env_file_encoding = "utf-8"

# Tüm projede kullanılacak tekil settings nesnesi
settings = Settings()