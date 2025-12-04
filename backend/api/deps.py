from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

# --- IMPORTLAR ---
from backend.database.session import AsyncSessionLocal
from backend.core.config import settings
from backend.crud.crud_user import user as user_crud
from backend.models import Users

# 1. Token Nereden Gelecek?
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/login" 
)

# 2. Veritabanı Bağlantısı
async def get_async_db() -> AsyncGenerator[AsyncSession, None]: 
    """
    FastAPI için asenkron veritabanı oturumu sağlayan jeneratör.
    """
    async with AsyncSessionLocal() as session: 
        try:
            yield session
        except Exception:
            await session.rollback() 
            raise

# 3. KİMLİK DOĞRULAMA (Standart Kullanıcı Bekçisi)
async def get_current_user(
    db: AsyncSession = Depends(get_async_db),
    token: str = Depends(reusable_oauth2)
) -> Users:
    """
    Token'ı doğrular ve kullanıcıyı veritabanından getirir.
    """
    try:
        # Token'ı gizli anahtarla çöz
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        # Token içindeki ID'yi al
        token_data = payload.get("sub")
        
        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token geçersiz: ID bulunamadı."
            )
            
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Oturum süresi dolmuş veya token geçersiz."
        )

    # Veritabanından kullanıcıyı bul
    user = await user_crud.get(db, id=int(token_data))
    
    if not user:
        raise HTTPException(
            status_code=404, 
            detail="Kullanıcı bulunamadı."
        )
    
    return user

# 4. YETKİ KONTROLÜ (Admin Bekçisi) - YENİ EKLENDİ
async def get_current_admin_user(
    current_user: Users = Depends(get_current_user),
) -> Users:
    """
    Sadece 'admin' rolüne sahip kullanıcıların geçmesine izin verir.
    """
    if current_user.Role != "admin":
        raise HTTPException(
            status_code=403, 
            detail="Bu işlem için Admin yetkisi gerekiyor!"
        )
    return current_user