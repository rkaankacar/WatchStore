from typing import List, Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api import deps
from backend.crud.crud_favorite import favorites as favorites_crud # CRUD nesnesini doğru import ettik
from backend.schemas import FavoriteCreate, FavoriteResponse
from backend.models import Users

router = APIRouter()

# 1. FAVORİLERİMİ LİSTELE (Zaten temizdi)
@router.get("/", response_model=List[FavoriteResponse])
async def read_favorites(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: Users = Depends(deps.get_current_user)
) -> Any:
    """
    Giriş yapmış kullanıcının favori listesini CRUD üzerinden getirir.
    """
    favorites_list = await favorites_crud.get_multi_by_user(
        db, user_id=current_user.UserID, skip=skip, limit=limit
    )
    return favorites_list

# 2. FAVORİYE EKLE (Temizlendi: Varlık kontrolü ve oluşturma mantığı kaldırıldı)
@router.post("/", response_model=FavoriteResponse, status_code=status.HTTP_201_CREATED)
async def add_to_favorites(
    *,
    fav_in: FavoriteCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: Users = Depends(deps.get_current_user)
) -> Any:
    """
    Bir saati favorilere ekler. Zaten ekliyse var olanı döner (CRUD'da yönetilir).
    """
    # Tüm varlık kontrolü, çakışma kontrolü ve oluşturma mantığı CRUD'a devredildi.
    new_fav = await favorites_crud.create_or_get_existing(
        db, 
        obj_in=fav_in, 
        user_id=current_user.UserID
    )
    return new_fav

# 3. FAVORİDEN ÇIKAR (Temizlendi: Varlık kontrolü, sahiplik kontrolü ve hata fırlatma kaldırıldı)
@router.delete("/{favorite_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_favorite(
    favorite_id: int,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: Users = Depends(deps.get_current_user)
) -> None:
    """
    Favori ID'sine göre silme işlemi yapar. Varlık ve sahiplik kontrolü CRUD'a taşındı.
    """
    # Tüm güvenlik kontrolü ve silme işlemi CRUD'a devredildi.
    await favorites_crud.remove_by_id_with_ownership_check(
        db, 
        favorite_id=favorite_id, 
        current_user=current_user
    )
    return None