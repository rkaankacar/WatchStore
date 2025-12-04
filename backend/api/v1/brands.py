from typing import List, Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api import deps
from backend.crud.crud_brand import brand as brand_crud # Güncellenmiş CRUD'u import et
from backend.schemas import BrandCreate, BrandUpdate, BrandResponse, BrandSimpleResponse
# HTTPException artık endpoint'te kullanılmayacağı için importu kaldırılabilir.
# from fastapi import HTTPException 

router = APIRouter()

# 1. MARKALARI LİSTELE (Temiz - CRUDBase'den get_multi)
@router.get("/", response_model=List[BrandSimpleResponse])
async def read_brands(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(deps.get_async_db)
) -> Any:
    brands = await brand_crud.get_multi(db, skip=skip, limit=limit)
    return brands

# 2. YENİ MARKA EKLE (Temiz - CRUDBase'den create)
@router.post("/", response_model=BrandResponse, status_code=status.HTTP_201_CREATED)
async def create_brand(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    brand_in: BrandCreate,
    current_user: Any = Depends(deps.get_current_admin_user) 
) -> Any:
    brand = await brand_crud.create(db, obj_in=brand_in)
    return brand

# 3. MARKA DETAYI (Temizlendi: 404 kontrolü kaldırıldı)
@router.get("/{brand_id}", response_model=BrandResponse)
async def read_brand(
    brand_id: int,
    db: AsyncSession = Depends(deps.get_async_db)
) -> Any:
    """
    Marka detayını getirir. Bulunamazsa 404'ü CRUD fırlatır.
    """
    # Yeni CRUD metodunu kullanıyoruz.
    brand = await brand_crud.get_or_404(db, id=brand_id)
    return brand

# 4. MARKA GÜNCELLE (Temizlendi: 404 kontrolü kaldırıldı)
@router.put("/{brand_id}", response_model=BrandResponse)
async def update_brand(
    brand_id: int,
    brand_in: BrandUpdate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: Any = Depends(deps.get_current_admin_user)
) -> Any:
    """
    Markayı günceller. Varlık kontrolü CRUD'a taşındı.
    """
    # Yeni CRUD metodunu kullanıyoruz.
    updated_brand = await brand_crud.update_or_404(db, id=brand_id, obj_in=brand_in)
    return updated_brand

# 5. MARKA SİL (Temizlendi: 404 kontrolü kaldırıldı)
@router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_brand(
    brand_id: int,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: Any = Depends(deps.get_current_admin_user)
) -> None:
    """
    Markayı siler. Varlık kontrolü CRUD'a taşındı.
    """
    # Yeni CRUD metodunu kullanıyoruz.
    await brand_crud.remove_or_404(db, id=brand_id)
    return None