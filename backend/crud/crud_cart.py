from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status # <-- Hata fırlatma için gerekli

from backend.crud.base import CRUDBase
from backend.models import Cart, Users # Users modeline ihtiyaç duyulabilir (opsiyonel)
from backend.schemas import CartCreate, CartUpdate

class CRUDCart(CRUDBase[Cart, CartCreate, CartUpdate]):
    
    # Yeni Özel Metot 3: Varlık ve Sahiplik Kontrolü (PUT ve DELETE için)
    async def get_item_by_user_id_or_404(
        self, 
        db: AsyncSession, 
        *, 
        cart_id: int, 
        current_user_id: int # Doğrudan ID'yi alıyoruz
    ) -> Cart:
        """
        Sepet öğesini ID ile getirir. Yoksa 404, kullanıcıya ait değilse 403 fırlatır.
        """
        # 1. Sepet öğesini bul
        cart_item: Optional[Cart] = await self.get(db, id=cart_id) 

        # 2. Varlık Kontrolü (Endpoint'ten taşındı)
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Sepet öğesi bulunamadı"
            )
            
        # 3. Sahiplik Kontrolü (Endpoint'ten taşındı)
        if cart_item.UserID != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Bu işlem için yetkiniz yok."
            )
            
        return cart_item

    # Yeni Özel Metot 4: Sepet Güncelleme (Kontrollü)
    async def update_item_with_check(
        self,
        db: AsyncSession,
        *,
        cart_id: int,
        cart_in: CartUpdate,
        current_user_id: int
    ) -> Cart:
        """
        Varlık ve sahiplik kontrolü yaparak sepet öğesini günceller.
        """
        # Kontrolleri yap ve öğeyi al
        cart_item = await self.get_item_by_user_id_or_404(
            db, cart_id=cart_id, current_user_id=current_user_id
        )
        
        # Güncelleme işlemini CRUDBase'e devret
        return await super().update(db, db_obj=cart_item, obj_in=cart_in)
        
    # Yeni Özel Metot 5: Sepetten Silme (Kontrollü)
    async def remove_item_with_check(
        self,
        db: AsyncSession,
        *,
        cart_id: int,
        current_user_id: int
    ) -> None:
        """
        Varlık ve sahiplik kontrolü yaparak sepet öğesini siler.
        """
        # Kontrolleri yap ve öğeyi al (silinecek nesnenin varlığını kontrol etmiş oluruz)
        await self.get_item_by_user_id_or_404(
            db, cart_id=cart_id, current_user_id=current_user_id
        )
        
        # Silme işlemini CRUDBase'e devret
        await super().remove(db, id=cart_id)


    # --- Mevcut Diğer Metotlar (Değişmedi) ---

    async def get_multi_by_user(self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 100) -> List[Cart]:
        """UserID'ye göre filtreleyerek sepet öğelerini getirir."""
        query = select(self.model).where(self.model.UserID == user_id).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_user_and_watch(self, db: AsyncSession, *, user_id: int, watch_id: int) -> Optional[Cart]:
        """Kullanıcının sepetinde bu saat zaten var mı diye bakar."""
        query = select(Cart).where(Cart.UserID == user_id, Cart.WatchID == watch_id)
        result = await db.execute(query)
        return result.scalars().first()

    async def add_or_update_item(self, db: AsyncSession, *, user_id: int, cart_in: CartCreate) -> Cart:
        
        existing_item = await self.get_by_user_and_watch(db, user_id=user_id, watch_id=cart_in.watch_id)

        if existing_item:
            # Varsa: Adeti artır
            new_quantity = existing_item.Quantity + cart_in.quantity
            update_schema = CartUpdate(Quantity=new_quantity)
            updated_item = await self.update(db, db_obj=existing_item, obj_in=update_schema)
            return updated_item
        else:
            # Yoksa: Yeni satır oluştur
            db_obj = Cart(
                UserID=user_id,
                WatchID=cart_in.watch_id,
                Quantity=cart_in.quantity
            )
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj

cart = CRUDCart(Cart)