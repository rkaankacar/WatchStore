import sys
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.sql import text # <-- Düzgün SQL çalıştırmak için kritik
from dotenv import load_dotenv
load_dotenv()  # .env dosyasını oku

# Python'un proje kök dizinini görmesi için yol ayarı (Zaten doğru)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# --- KRİTİK İMPORTLAR ---
from backend.core.config import settings
from backend.core.errors import register_exception_handlers
from backend.database.session import async_engine, Base
# Tüm modellerin içe aktarılması, Base.metadata'nın görmesi için şart
from backend.models.watches import watches
from backend.models.favorites import favorites
from backend.models.cart import cart
from backend.models.reviews import reviews
from backend.models.ordersdetails import ordersdetails
from backend.models.watches_images import watches_images
from backend.models.brands import brands
from backend.models.orders import orders
from backend.models.users import users
from backend.models.returns import returns

# --- ROUTER IMPORTLARI ---
from backend.routers import auth, utils
from backend.api.v1 import brands, cart, orders, reviews, watches, users, favorites, create_payment, returns

# --- 1. Uygulama Yaratma Fabrika Fonksiyonu ---
def create_application() -> FastAPI:
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="Saat Satış E-Ticaret API (Asenkron Mimari)",
        version=settings.VERSION,
        docs_url="/docs",
        redoc_url=None, 
    )
    
    origins =[
        "http://localhost:5173"
    ]
    
    # CORS AYARLARI
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins, 
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # DÜZELTME: STATIC DOSYA AYARLARI
    BASE_PATH = Path(__file__).resolve().parent
    static_path = BASE_PATH / "static"

    if not static_path.exists():
        static_path.mkdir(parents=True, exist_ok=True)
        print(f"⚠️ Static klasörü bulunamadı, otomatik oluşturuldu: {static_path}")

    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
    
    # HATA YÖNETİMİ
    register_exception_handlers(app)

    # 4. ROUTERLARI DAHİL ETME
    app.include_router(auth.router, tags=["Authentication"])
    app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
    app.include_router(brands.router, prefix="/api/v1/brands", tags=["Brands"])
    app.include_router(watches.router, prefix="/api/v1/watches", tags=["Watches"])
    app.include_router(cart.router, prefix="/api/v1/cart", tags=["Cart"])
    app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["Reviews"])
    app.include_router(orders.router, prefix="/api/v1/orders", tags=["Orders"])
    app.include_router(favorites.router, prefix="/api/v1/favorites", tags=["Favorites"])
    app.include_router(utils.router, prefix="/api/v1", tags=["Utils"])
    app.include_router(create_payment.router, prefix="/api/v1/payment", tags=["Payment"])
    app.include_router(returns.router, prefix="/api/v1/returns", tags=["returns"])
    #
    return app





# Uygulamayı ayağa kaldır
app = create_application()

# --- 2. DATABASE EVENTLERİ (Uygulama dışındaki event handler'lar) ---

# Tabloları oluşturma ve şema ayarları
@app.on_event("startup")
async def startup_event():
    print(f"🚀 {settings.PROJECT_NAME} Başlatılıyor...")
    
    async with async_engine.begin() as conn:
        
        # 1. Adım: Şema Oluşturma
        if settings.SCHEMA_NAME:
            await conn.execute(
                # CREATE SCHEMA komutu
                text(f"CREATE SCHEMA IF NOT EXISTS {settings.SCHEMA_NAME}")
            )
            # Bağlantıyı doğru şemaya ayarlama
            await conn.execute(
                text(f"SET search_path TO {settings.SCHEMA_NAME}")
            )

        # 2. Adım: Tabloları Oluşturma
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Veritabanı tabloları kontrol edildi/oluşturuldu.")

# Uygulama kapanırken bağlantıları temizleme
@app.on_event("shutdown")
async def shutdown_event():
    print("🛑 Uygulama Kapanıyor: Veritabanı bağlantıları temizleniyor...")
    await async_engine.dispose()
    
    
    # uvicorn backend.main:app --reload
    # celery -A backend.worker.celery_app worker -l INFO -P solo