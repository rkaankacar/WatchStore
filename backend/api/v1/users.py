from typing import List, Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api import deps
from backend.crud.crud_user import user as user_crud
from backend.schemas import UserChangePassword, UserCreate, UserUpdate, UserResponse, UserSimpleResponse

router = APIRouter()

# 1. KULLANICI OLUŞTURMA (Temizlendi: Email kontrolü ve 400 hatası kaldırıldı)
@router.post("/", response_model=UserSimpleResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    user_in: UserCreate
) -> Any:
    """
    Yeni kullanıcı oluşturur. Email kontrolü ve şifre hashleme CRUD'a taşındı.
    """
    # Tüm iş mantığı (email kontrolü, 400 hatası) CRUD'a devredildi.
    new_user = await user_crud.create_user_with_check(db, obj_in=user_in)
    return new_user

# 2. KULLANICILARI LİSTELEME (Zaten temizdi)
@router.get("/", response_model=List[UserSimpleResponse])
async def read_users(
    db: AsyncSession = Depends(deps.get_async_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Tüm kullanıcıları listeler.
    """
    users = await user_crud.get_multi(db, skip=skip, limit=limit)
    return users

# 3. TEK KULLANICI DETAYI (Temizlendi: 404 kontrolü kaldırıldı)
@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(deps.get_async_db)
) -> Any:
    """
    ID'si verilen kullanıcının detaylarını getirir. Bulunamazsa 404 CRUD'dan gelir.
    """
    # Yeni CRUD metodunu kullanıyoruz. Bulunamazsa 404'ü CRUD fırlatır.
    user = await user_crud.get_or_404(db, id=user_id)
    return user

# 4. KULLANICI GÜNCELLEME (Temizlendi: 404 kontrolü kaldırıldı)
@router.put("/update/{user_id}", response_model=UserSimpleResponse)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(deps.get_async_db)
) -> Any:
    """
    Kullanıcı bilgilerini günceller. Varlık kontrolü CRUD'a taşındı.
    """
    # Yeni CRUD metodunu kullanıyoruz. Bulunamazsa 404'ü CRUD fırlatır.
    updated_user = await user_crud.update_or_404(db, id=user_id, obj_in=user_in)
    return updated_user

# 5. KULLANICI SİLME (Temizlendi: 404 kontrolü kaldırıldı)
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(deps.get_async_db)
) -> None:
    """
    Kullanıcıyı siler. Varlık kontrolü CRUD'a taşındı.
    """
    # Yeni CRUD metodunu kullanıyoruz. Bulunamazsa 404'ü CRUD fırlatır.
    await user_crud.remove_or_404(db, id=user_id)
    return None

@router.put("/change-password")
async def change_password(
    body: UserChangePassword,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user=Depends(deps.get_current_user)
):
    return await user_crud.change_password_with_confirm(
       db,
       user_id=current_user.UserID,
       current_password=body.current_password,
       new_password=body.new_password,
       new_password_again=body.new_password_again
    )
    
@router.get("/users/{user_id}", response_model=UserSimpleResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(deps.get_async_db)):
    return await user_crud.get_or_profile(db, id=user_id)


