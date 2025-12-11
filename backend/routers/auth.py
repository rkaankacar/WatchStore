from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api import deps
from backend.crud.crud_user import user as user_crud
from backend.core import security
from backend.schemas import Token # <--- Şemayı import etmeyi unutma!

router = APIRouter()

# 1. DEĞİŞİKLİK: response_model=Token ekledik ki Swagger dokümanı doğru görünsün
@router.post("/login", response_model=Token)
async def login(
    db: AsyncSession = Depends(deps.get_async_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Kullanıcı girişi yapar.
    Dönüş: Token + Rol + UserID
    """
    # 1. Kullanıcıyı doğrula (Email ve Şifre kontrolü)
    user = await user_crud.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hatalı email veya şifre."
        )
    
    # 2. Token süresini belirle (30 dakika)
    access_token_expires = timedelta(minutes=30)
    
    # 3. DEĞİŞİKLİK: Token oluştur ve ŞEMAYA UYGUN (Rol ve ID ile) dön
    # Burası çok önemli, frontend "admin mi user mı" diye buraya bakacak.
    return {
        "access_token": security.create_access_token(
            subject=user.UserID, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
        "role": user.Role,      # <--- BU EKSİKTİ, EKLENDİ
        "user_id": user.UserID,  # <--- BU EKSİKTİ, EKLENDİ
        "name": user.FullName,
    
    }