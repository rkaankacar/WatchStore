from typing import List, Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api import deps
from backend.crud.crud_cart import cart as cart_crud # Sadece CRUD'u çağırıyoruz
from backend.schemas import CartCreate, CartUpdate, CartResponse
from backend.models import Users 
# HTTPException artık endpoint'te kullanılmayacağı için importu kaldırılabilir.

router = APIRouter()

# 1. SEPETİMİ GÖR (Zaten temizdi)
@router.get("/", response_model=List[CartResponse])
async def read_cart_items(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: Users = Depends(deps.get_current_user)
) -> Any:
    """
    CRUD'dan sadece kullanıcının sepetini getirir.
    """
    my_items = await cart_crud.get_multi_by_user(
        db, user_id=current_user.UserID, skip=skip, limit=limit
    )
    return my_items

# 2. SEPETE EKLE (Zaten temizdi)
@router.post("/", response_model=CartResponse, status_code=status.HTTP_201_CREATED)
async def add_to_cart(
    *,
    cart_in: CartCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: Users = Depends(deps.get_current_user)
) -> Any:
    """
    Kullanıcının sepetine ürün ekler veya mevcut ürünü günceller (Tüm mantık CRUD'da).
    """
    updated_item = await cart_crud.add_or_update_item(
        db, user_id=current_user.UserID, cart_in=cart_in
    )
    return updated_item

# 3. SEPET GÜNCELLE (Temizlendi: 404 ve 403 kontrolü kaldırıldı)
@router.put("/{cart_id}", response_model=CartResponse)
async def update_cart_item(
    cart_id: int,
    cart_in: CartUpdate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: Users = Depends(deps.get_current_user)
) -> Any:
    """
    Sepet öğesini günceller. Varlık ve sahiplik kontrolü CRUD'a taşındı.
    """
    # Tüm kontrol ve güncelleme mantığı CRUD'a devredildi.
    updated_item = await cart_crud.update_item_with_check(
        db, 
        cart_id=cart_id, 
        cart_in=cart_in, 
        current_user_id=current_user.UserID # Kullanıcı ID'sini paslıyoruz
    )
    return updated_item

# 4. SEPETTEN SİL (Temizlendi: 404 ve 403 kontrolü kaldırıldı)
@router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart_item(
    cart_id: int,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: Users = Depends(deps.get_current_user)
) -> None:
    """
    Sepet öğesini siler. Varlık ve sahiplik kontrolü CRUD'a taşındı.
    """
    # Tüm kontrol ve silme mantığı CRUD'a devredildi.
    await cart_crud.remove_item_with_check(
        db, 
        cart_id=cart_id, 
        current_user_id=current_user.UserID # Kullanıcı ID'sini paslıyoruz
    )
    return None