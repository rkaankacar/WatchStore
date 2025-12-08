from typing import List, Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
# HTTPException artık sadece CRUD'da kullanıldığı için buradan kaldırılabilir (Ancak FastAPI'dan geliyor, o yüzden kalması sorun değil)
# from fastapi import HTTPException, status 

from backend.api import deps
from backend.crud.crud_order import order as order_crud 
from backend.schemas import OrderResponse
from backend.models import users, orders 

router = APIRouter()

# 1. SİPARİŞ OLUŞTUR / CHECKOUT (Zaten temizdi)
@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    *,
    shipping_address: str, 
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: users = Depends(deps.get_current_user)
) -> Any:
    """
    Sepetteki ürünleri alır ve Siparişe dönüştürür.
    """
    # CRUD çağrısı (Tüm iş mantığı, stok kontrolü vs. CRUD'da)
    new_order = await order_crud.create_from_cart(
        db, 
        user_id=current_user.UserID, 
        shipping_address=shipping_address
    )
    
    return new_order

# 2. SİPARİŞLERİMİ GÖR (Zaten temizdi)
@router.get("/", response_model=List[OrderResponse])
async def read_my_orders(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: users = Depends(deps.get_current_user)
) -> Any:
    """
    Sadece giriş yapmış kullanıcının kendi geçmiş siparişlerini listeler.
    """
    # CRUD çağrısı (Filtreleme CRUD'da)
    orders = await order_crud.get_multi_by_user(
        db, user_id=current_user.UserID, skip=skip, limit=limit
    )
    return orders

# 3. SİPARİŞ DETAYI GÖR (Temizlendi: Varlık ve Sahiplik Kontrolü kaldırıldı)
@router.get("/{order_id}", response_model=OrderResponse)
async def read_order_detail(
    order_id: int,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: users = Depends(deps.get_current_user)
) -> Any:
    """
    Tek bir siparişin detayını getirir. Başkasının siparişini göstermez (Kontrol CRUD'da).
    """
    # Yeni CRUD metodunu kullanıyoruz. 404 veya 403 hatasını CRUD fırlatır.
    order = await order_crud.get_order_by_user_id_or_404(
        db, 
        order_id=order_id,
        current_user=current_user # Kontrol için kullanıcıyı CRUD'a paslıyoruz
    )
    
    return order