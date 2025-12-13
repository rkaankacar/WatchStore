import asyncio
from sqlalchemy.sql import text

# Gerekli importlar (Kendi dosya yollarınla eşleşmeli)
from backend.core.config import settings
from backend.database.session import async_engine, Base

# Tüm model sınıflarını içe aktarın ki Base.metadata onları görsün
from backend.models.watches import watches
from backend.models.favorites import favorites
from backend.models.cart import cart
from backend.models.reviews import reviews
from backend.models.ordersdetails import ordersdetails
from backend.models.watches_images import watches_images
from backend.models.brands import brands
from backend.models.orders import orders
from backend.models.users import users
from backend.models.payments import payments
from backend.models.returns import returns

async def create_schema_and_tables():
    print("--- SCHEMA VE TABLO OLUŞTURMA BAŞLADI ---")
    
    try:
        async with async_engine.begin() as conn:
            
            # 1. Şema Oluşturma Kontrolü
            if settings.SCHEMA_NAME:
                print(f"1. Şema ({settings.SCHEMA_NAME}) kontrol ediliyor/oluşturuluyor...")
                await conn.execute(
                    text(f"CREATE SCHEMA IF NOT EXISTS {settings.SCHEMA_NAME}")
                )
                print(f"2. Bağlantı şemaya ayarlanıyor: {settings.SCHEMA_NAME}")
                await conn.execute(
                    text(f"SET search_path TO {settings.SCHEMA_NAME}")
                )

            # 2. Tabloları Oluşturma
            print("3. Tablolar Base.metadata üzerinden oluşturuluyor...")
            await conn.run_sync(Base.metadata.create_all)
        
        print("--- BAŞARILI: Tablolar oluşturulmuş olmalı. PostgreSQL'ü kontrol edin. ---")

    except Exception as e:
        print(f"!!! HATA: Tablo oluşturulurken kritik bir hata oluştu: {e}")
        # Hata detaylarını görmek için exception'ı tekrar fırlatabiliriz
        # raise

if __name__ == "__main__":
    # Asenkron fonksiyonu çalıştır
    asyncio.run(create_schema_and_tables())