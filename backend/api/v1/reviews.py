from typing import List, Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api import deps
from backend.crud.crud_review import review as review_crud # CRUD'u import et
from backend.schemas import ReviewCreate, ReviewUpdate, ReviewResponse
from backend.models import users, reviews # Artık sadece Users modeline ihtiyacımız var

router = APIRouter()

# 1. YORUMLARI LİSTELE (Bu kısım zaten temizdi)
@router.get("/", response_model=List[ReviewResponse])
async def read_reviews(
    watch_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(deps.get_async_db)
) -> Any:
    """
    Yorumları listeler. watch_id verilirse sadece o saate ait olanları getirir.
    """
    if watch_id:
        # CRUD çağrısı
        reviews = await review_crud.get_by_watch(db, watch_id=watch_id, skip=skip, limit=limit)
    else:
        # CRUD çağrısı
        reviews = await review_crud.get_multi(db, skip=skip, limit=limit)
    return reviews

# 2. YORUM YAP (Temizlendi)
@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    *,
    review_in: ReviewCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: users = Depends(deps.get_current_user)
) -> Any:
    """
    Sadece giriş yapmış kullanıcılar yorum yapabilir.
    """
    # Tüm iş mantığı ve veritabanı modellemesi CRUD'a devredildi.
    review = await review_crud.create_review_with_user(
        db,
        obj_in=review_in,
        user=current_user # Kullanıcı nesnesini CRUD'a gönderiyoruz
    )
    return review

# 3. YORUM SİL (Temizlendi)
@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: int,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: users = Depends(deps.get_current_user)
) -> None:
    """
    Sadece giriş yapmış kullanıcılar kendi yorumlarını silebilir.
    Hata kontrolü (bulunamadı, sahiplik) CRUD'a devredildi.
    """
    # Tüm iş mantığı (bulunamadı, sahiplik kontrolü) CRUD'a devredildi.
    await review_crud.remove_review_with_ownership_check(
        db,
        review_id=review_id,
        current_user=current_user
    )
    # Hata fırlatma veya başarı durumunda 204'ü FastAPI/APIRouter otomatik halleder.
    return None