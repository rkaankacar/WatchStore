import sys
import os

# Python'un proje kök dizinini görmesi için yol ayarı
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- IMPORTLAR ---
from backend.core.config import settings
from backend.core.errors import register_exception_handlers
from backend.database.session import async_engine
from backend.database.session import Base  # Tablo oluşturmak için gerekli
from backend.models import * # Modelleri yükle ki tablolar oluşabilsin

# --- ROUTER IMPORTLARI ---
# Login router'ını ekledik
from backend.routers import auth 
# Endpointleri doğru klasörden çağırıyoruz
from backend.api.v1 import brands, cart, orders, reviews, watches, users, favorites

def create_application() -> FastAPI:
    """
    FastAPI uygulamasını başlatan ve tüm bileşenleri (Router, DB, Middleware)
    birleştiren ana fabrika fonksiyonu.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="Saat Satış E-Ticaret API (Asenkron Mimari)",
        version=settings.VERSION,
        docs_url="/docs",
        redoc_url=None, 
    )

    # 1. CORS AYARLARI
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], 
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 2. HATA YÖNETİMİ
    register_exception_handlers(app)

    # 3. DATABASE EVENTLERİ (Başlarken)
    @app.on_event("startup")
    async def startup_event():
        print(f"🚀 {settings.PROJECT_NAME} Başlatılıyor...")
        
        # --- TABLOLARI OTOMATİK OLUŞTUR ---
        # Veritabanında tablolar yoksa oluşturur. Varsa dokunmaz.
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Veritabanı tabloları kontrol edildi/oluşturuldu.")

    @app.on_event("shutdown")
    async def shutdown_event():
        print("🛑 Uygulama Kapanıyor: Veritabanı bağlantıları temizleniyor...")
        await async_engine.dispose()

    # 4. ROUTERLARI DAHİL ETME
    
    # Login / Auth (Prefix yok, direkt /login)
    app.include_router(auth.router, tags=["Authentication"])
    
    # API V1 Endpointleri
    app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
    app.include_router(brands.router, prefix="/api/v1/brands", tags=["Brands"])
    app.include_router(watches.router, prefix="/api/v1/watches", tags=["Watches"])
    app.include_router(cart.router, prefix="/api/v1/cart", tags=["Cart"])
    app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["Reviews"])
    app.include_router(orders.router, prefix="/api/v1/orders", tags=["Orders"])
    app.include_router(favorites.router, prefix="/api/v1/favorites", tags=["Favorites"])
    
    return app

# Uygulamayı ayağa kaldır
app = create_application()




# uvicorn backend.main:app --reload