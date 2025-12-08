from typing import List, Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api import deps
# CRUD IMPORTLARI GÜNCELLENDİ:
# Hem saati (watch_crud) hem de resim işlemlerini (image_crud) import ediyoruz.
from backend.crud.crud_watch import watch as watch_crud, watch_image as image_crud

# SCHEMA IMPORTLARI GÜNCELLENDİ:
# WatchImageCreate ve WatchImageSimpleResponse eklendi.
from backend.schemas import (
    WatchCreate, 
    WatchUpdate, 
    WatchResponse, 
    WatchSimpleResponse,
    WatchImageCreate, 
    WatchImageSimpleResponse
)

router = APIRouter()

# ==========================================
# 1. SAATLER (WATCHES) İŞLEMLERİ
# ==========================================

# 1. SAATLERİ LİSTELE
@router.get("/", response_model=List[WatchSimpleResponse])
async def read_watches(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(deps.get_async_db)
) -> Any:
    """
    Tüm saatleri listeler.
    """
    watches = await watch_crud.get_multi(db, skip=skip, limit=limit)
    return watches

# 2. YENİ SAAT EKLE
@router.post("/", response_model=WatchResponse, status_code=status.HTTP_201_CREATED)
async def create_watch(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    watch_in: WatchCreate,
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """
    Yeni saat oluşturur. Sadece Admin yapabilir.
    """
    new_watch = await watch_crud.create(db, obj_in=watch_in)
    return new_watch

# 3. SAAT DETAYI
@router.get("/{watch_id}", response_model=WatchResponse)
async def read_watch(
    watch_id: int,
    db: AsyncSession = Depends(deps.get_async_db)
) -> Any:
    """
    Tek bir saatin tüm detaylarını getirir.
    """
    watch = await watch_crud.get_or_404(db, id=watch_id)
    return watch

# 4. SAAT GÜNCELLE
@router.put("/{watch_id}", response_model=WatchResponse)
async def update_watch(
    watch_id: int,
    watch_in: WatchUpdate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    updated_watch = await watch_crud.update_or_404(db, id=watch_id, obj_in=watch_in)
    return updated_watch

# 5. SAAT SİL
@router.delete("/{watch_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_watch(
    watch_id: int,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: Any = Depends(deps.get_current_admin_user)
) -> None:
    await watch_crud.remove_or_404(db, id=watch_id)
    return None


# ==========================================
# 2. GALERİ RESİMLERİ (WATCH IMAGES) İŞLEMLERİ
# ==========================================

@router.post("/watch_images/", response_model=WatchImageSimpleResponse, status_code=status.HTTP_201_CREATED)
async def create_watch_image(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    image_in: WatchImageCreate,
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """
    Bir saate ait yeni bir galeri resmi ekler.
    Frontend buraya { "WatchID": 1, "ImageUrl": "..." } yollar.
    """
    # crud_watch dosyasındaki watch_image nesnesini (image_crud) kullanıyoruz
    new_image = await image_crud.create(db, obj_in=image_in)
    return new_image

# 🎯 YENİ ENDPOINT: SADECE CİNSİYETE GÖRE SAATLERİ GETİRİR
@router.get("/by_gender/", response_model=List[WatchSimpleResponse])
async def read_watches_by_gender(
    gender: str, # Artık Optional değil, zorunlu bir filtre bekliyoruz
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(deps.get_async_db)
) -> Any:
    """
    Belirtilen cinsiyete (Erkek/Kadın/Unisex) ait saatleri listeler.
    """
    watches = await watch_crud.get_multi_by_gender(db, gender=gender, skip=skip, limit=limit)
    return watches

# 🎯 YENİ ENDPOINT: SADECE MARKA ID'SİNE GÖRE SAATLERİ GETİRİR
@router.get("/by_brand/", response_model=List[WatchSimpleResponse])
async def read_watches_by_brand(
    # frontend'den /api/v1/watches/by_brand/?brand_id=5 şeklinde gelecek
    brand_id: int, 
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(deps.get_async_db)
) -> Any:
    """
    Belirtilen Marka ID'sine ait saatleri listeler (Koleksiyon Detay Sayfası için).
    """
    # Yeni CRUD metodunu çağırıyoruz
    watches = await watch_crud.get_multi_by_brand(db, brand_id=brand_id, skip=skip, limit=limit)
    return watches