from http.client import HTTPException
from typing import List, Optional, Any, Dict, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from backend.crud.base import CRUDBase
# Yeni Import'lar: ordersdetails ve watches modelleri, ürün adını çekmek için gerekli
from backend.models import returns, users, orders, ordersdetails, watches 
from backend.schemas import ReturnCreate, ReturnUpdate
from backend.models.orders import orders # İlişki yüklemesi için orders modelini açıkça import et
from backend.exceptions import ReturnNotFound

class CRUDReturn(CRUDBase[returns, ReturnCreate, ReturnUpdate]):
    
    # İade objesinden ürün adını çekmek için YENİ EAGER LOADING ZİNCİRİ
    def _get_eager_options(self):
        """
        Returns -> Order -> OrderDetails -> Watch -> Brand zincirini kurar
        """
        return [
            # 1. İlişki: İade -> Sipariş (OrderID ile)
            selectinload(self.model.order) 
                # 2. İlişki: Sipariş -> Sipariş Detayları
                .selectinload(orders.order_details) 
                # 3. İlişki: Sipariş Detayları -> Saat (Ürün)
                .selectinload(ordersdetails.watch)  
                # 4. İlişki: Saat -> Marka
                .selectinload(watches.brand),
            
            # Yeni: OrderDetail ilişkisi
            selectinload(self.model.order_detail)
                .selectinload(ordersdetails.watch)
                .selectinload(watches.brand),
                
            # Diğer İlişki
            selectinload(self.model.user)
        ]

    # 1. Kullanıcının kendi taleplerini getir (Eager Loading zinciri artık burada çalışacak)
    async def get_multi_by_user(
        self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[returns]:
        query = (
            select(self.model)
            .where(self.model.UserID == user_id)
            .options(*self._get_eager_options()) # Güncellenmiş zinciri kullan
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().unique().all()
    
    # 🌟 EKLENEN METOT: Kullanıcı ID'sini ekleyerek yeni talep oluşturma
    async def create_with_owner(
        self,
        db: AsyncSession,
        *,
        obj_in: ReturnCreate,
        user_id: int
    ) -> returns:
        # Pydantic objesini sözlüğe çevirirken, Alias'ları (Büyük harfleri) kullan
        obj_in_data = obj_in.model_dump(by_alias=True)
        
        # UserID'yi token'dan gelen güvenli ID ile ekle
        obj_in_data["UserID"] = user_id
        
        # SQLAlchemy modelini oluştur ve kaydet
        db_obj = self.model(**obj_in_data)
        
        db.add(db_obj)
        await db.commit()
        # await db.refresh(db_obj) # Lazy loading hatasına neden oluyor
        
        # Refresh yerine eager loading ile tekrar çekiyoruz
        query = select(self.model).where(self.model.ReturnID == db_obj.ReturnID).options(*self._get_eager_options())
        result = await db.execute(query)
        db_obj = result.scalars().first()
        
        return db_obj


    # 2. Admin için tüm talepleri getir (Eager Loading zinciri artık burada çalışacak)
    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[returns]:
        query = (
            select(self.model)
            .options(*self._get_eager_options()) # Güncellenmiş zinciri kullan
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().unique().all()

    # 3. Durum Güncelleme (Admin için)
    async def update_status(
        self, db: AsyncSession, *, return_id: int, status_in: ReturnUpdate
    ) -> returns:
        db_obj = await self.get(db, id=return_id)
        
        if not db_obj:
            raise ReturnNotFound()
            
        update_data = status_in.model_dump(exclude_unset=True, by_alias=True)
        
        if "Status" in update_data:
            db_obj.Status = update_data["Status"]
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
        
        # Güncel halini ilişkilerle tekrar çekmek için Eager Loading kullanıyoruz
        query = select(self.model).where(self.model.ReturnID == return_id).options(*self._get_eager_options())
        res = await db.execute(query)
        return res.scalars().first()

return_crud = CRUDReturn(returns)