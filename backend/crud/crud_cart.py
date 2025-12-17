from typing import Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload 
from fastapi import HTTPException, status
from sqlalchemy import delete
from backend.crud.base import CRUDBase
# 🎯 DÜZELTME 1: Model sınıfını CartModel olarak yeniden adlandırarak içeri alıyoruz
from backend.models import users, watches 
from backend.models import cart as CartModel # Cart model sınıfını çekiyoruz
from backend.schemas import CartCreate, CartUpdate
from backend.exceptions import CartItemNotFound, CartAccessDenied

# 🎯 DÜZELTME 2: CRUDBase'i Model Sınıfı olan CartModel ile başlatıyoruz
class CRUDCart(CRUDBase[CartModel, CartCreate, CartUpdate]):
    
    # -------------------------------------------------------------
    # 🎯 FIX: EAGER LOADING YARDIMCI METODU
    # -------------------------------------------------------------
    
    def _select_with_relationships(self):
        """Watch ve Watch'ın içindeki Brand ilişkisini yükler."""
        # 🎯 select() içine model sınıfını (CartModel) veriyoruz
        return select(CartModel).options( 
            selectinload(CartModel.user), # İlişkilerde model sınıfı kullanılır
            # Cart -> Watch -> Brand zincirini yüklüyoruz
            selectinload(CartModel.watch).selectinload(watches.brand) 
        )

    # -------------------------------------------------------------
    # 1. GET METOTLARI (Eager Loading için override edildi)
    # -------------------------------------------------------------
    
    # CRUDBase'den gelen temel 'get' metodu
    # Geri dönüş tipi: cart yerine CartModel
    async def get(self, db: AsyncSession, id: Any) -> Optional[CartModel]: 
        query = self._select_with_relationships().where(CartModel.CartID == id)
        result = await db.execute(query)
        return result.scalars().first()
        
    # UserID'ye göre filtreleyerek sepet öğelerini getirir
    # Geri dönüş tipi: List[cart] yerine List[CartModel]
    async def get_multi_by_user(self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 100) -> List[CartModel]: 
        query = self._select_with_relationships().where(CartModel.UserID == user_id).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    # Kullanıcının sepetinde bu saat zaten var mı diye bakar.
    async def get_by_user_and_watch(self, db: AsyncSession, *, user_id: int, watch_id: int) -> Optional[CartModel]: 
        query = select(CartModel).where(CartModel.UserID == user_id, CartModel.WatchID == watch_id)
        result = await db.execute(query)
        return result.scalars().first()

    # -------------------------------------------------------------
    # 2. ÖZEL KONTROL VE İŞLEM METOTLARI
    # -------------------------------------------------------------
    
    # Sepete ekleme veya adeti artırma
    async def add_or_update_item(self, db: AsyncSession, *, user_id: int, cart_in: CartCreate) -> CartModel: 
        
        existing_item = await self.get_by_user_and_watch(db, user_id=user_id, watch_id=cart_in.watch_id)

        if existing_item:
            # Varsa: Adeti artır
            new_quantity = existing_item.Quantity + cart_in.quantity
            update_schema = CartUpdate(Quantity=new_quantity)
            
            updated_item = await super().update(db, db_obj=existing_item, obj_in=update_schema)
            
            return await self.get(db, id=updated_item.CartID) 
        else:
            # Yoksa: Yeni satır oluştur
            db_obj = CartModel( # 🎯 Model sınıfı kullanıldı
                UserID=user_id,
                WatchID=cart_in.watch_id,
                Quantity=cart_in.quantity
            )
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            
            return await self.get(db, id=db_obj.CartID) 

    # Yeni Özel Metot 3: Varlık ve Sahiplik Kontrolü
    async def get_item_by_user_id_or_404(
        self, 
        db: AsyncSession, 
        *, 
        cart_id: int, 
        current_user_id: int
    ) -> CartModel: # Geri dönüş tipi düzeltildi
        """
        Sepet öğesini ID ile getirir. Yoksa 404, kullanıcıya ait değilse 403 fırlatır.
        """
        # 1. Sepet öğesini bul
        cart_item: Optional[CartModel] = await self.get(db, id=cart_id) # Tip düzeltildi

        # ... (Kontrollerin geri kalanı aynı) ...
        if not cart_item:
            raise CartItemNotFound()
            
        if cart_item.UserID != current_user_id:
            raise CartAccessDenied()
            
        return cart_item

    # Yeni Özel Metot 4: Sepet Güncelleme
    async def update_item_with_check(
        self,
        db: AsyncSession,
        *,
        cart_id: int,
        cart_in: CartUpdate,
        current_user_id: int
    ) -> CartModel: # Geri dönüş tipi düzeltildi
        """
        Varlık ve sahiplik kontrolü yaparak sepet öğesini günceller.
        """
        cart_item = await self.get_item_by_user_id_or_404(
            db, cart_id=cart_id, current_user_id=current_user_id
        )
        
        updated_item = await super().update(db, db_obj=cart_item, obj_in=cart_in)
        
        return await self.get(db, id=updated_item.CartID) 
        
    # Yeni Özel Metot 5: Sepetten Silme (Kontrollü)
    async def remove_item_with_check(
        self,
        db: AsyncSession,
        *,
        cart_id: int,
        current_user_id: int
    ) -> None:
        """
        Varlık ve sahiplik kontrolü yaparak sepet öğesini sile
        """
        # Kontrolleri yap (404/403 fırlatır)
        await self.get_item_by_user_id_or_404(
            db, cart_id=cart_id, current_user_id=current_user_id
        )
        
        # Silme işlemini CRUDBase'e devret
        await super().remove(db, id=cart_id)

    async def remove_by_watch_id(self, db: AsyncSession, *, watch_id: int) -> None:
        """Belirtilen WatchID'ye ait tüm sepet öğelerini siler."""
        stmt = delete(CartModel).where(CartModel.WatchID == watch_id)
        await db.execute(stmt)
# 🎯 KRİTİK DÜZELTME 3: CRUD nesnesini çakışmayacak şekilde adlandırıyoruz
cart_crud = CRUDCart(CartModel)