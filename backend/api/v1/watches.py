from typing import List, Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api import deps
# Güncellenmiş CRUD'u import ediyoruz
from backend.crud.crud_watch import watch as watch_crud 
from backend.schemas import WatchCreate, WatchUpdate, WatchResponse, WatchSimpleResponse
# Artık HTTPException'a ihtiyacımız yok
# from fastapi import HTTPException 

router = APIRouter()

# 1. SAATLERİ LİSTELE (Temiz - CRUD zaten get_multi kullanıyor)
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

# 2. YENİ SAAT EKLE (Temiz - CRUD zaten create kullanıyor)
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

# 3. SAAT DETAYI (Temizlendi: 404 kontrolü kaldırıldı)
@router.get("/{watch_id}", response_model=WatchResponse)
async def read_watch(
    watch_id: int,
    db: AsyncSession = Depends(deps.get_async_db)
) -> Any:
    """
    Tek bir saatin tüm detaylarını getirir.
    """
    # Yeni CRUD metodunu kullanıyoruz. Bulunamazsa 404'ü CRUD fırlatır.
    watch = await watch_crud.get_or_404(db, id=watch_id)
    return watch

# 4. SAAT GÜNCELLE (Temizlendi: 404 kontrolü kaldırıldı)
@router.put("/{watch_id}", response_model=WatchResponse)
async def update_watch(
    watch_id: int,
    watch_in: WatchUpdate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    # Yeni CRUD metodunu kullanıyoruz. Bulunamazsa 404'ü CRUD fırlatır.
    updated_watch = await watch_crud.update_or_404(db, id=watch_id, obj_in=watch_in)
    return updated_watch

# 5. SAAT SİL (Temizlendi: 404 kontrolü kaldırıldı)
@router.delete("/{watch_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_watch(
    watch_id: int,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: Any = Depends(deps.get_current_admin_user)
) -> None:
    # Yeni CRUD metodunu kullanıyoruz. Bulunamazsa 404'ü CRUD fırlatır.
    await watch_crud.remove_or_404(db, id=watch_id)
    return None