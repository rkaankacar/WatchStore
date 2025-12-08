from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from fastapi import HTTPException, status # <-- status'ü de ekledik

from backend.crud.base import CRUDBase
from backend.models import orders, ordersdetails, cart, watches, users # Users modelini de import etmeliyiz (opsiyonel)
from backend.schemas import OrderCreate, OrderUpdate, OrderDetailCreate, OrderDetailUpdate

# Sepet ve Saat CRUD'larını import ediyoruz
from backend.crud.crud_cart import cart_crud 
from backend.crud.crud_watch import watch as watch_crud 

# --- SİPARİŞ DETAYLARI (Değişmedi) ---
class CRUDOrderDetail(CRUDBase[ordersdetails, OrderDetailCreate, OrderDetailUpdate]):
    pass

order_detail = CRUDOrderDetail(ordersdetails)

# --- SİPARİŞLER (ANA SINIF) ---
class CRUDOrder(CRUDBase[orders, OrderCreate, OrderUpdate]):
    
    # Yeni Fonksiyon: 3. Endpoint için güvenlik ve varlık kontrolünü sağlar.
    async def get_order_by_user_id_or_404(
        self, 
        db: AsyncSession, 
        *, 
        order_id: int, 
        current_user: users
    ) -> orders:
        """
        Siparişi ID ile getirir. Yoksa 404, kullanıcıya ait değilse 403 fırlatır.
        """
        # Siparişi bul
        order = await self.get(db, id=order_id) 

        # 1. Varlık Kontrolü (Endpoint'ten taşındı)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Sipariş bulunamadı"
            )
            
        # 2. Sahiplik Kontrolü (Endpoint'ten taşındı)
        if order.UserID != current_user.UserID:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Bu siparişi görüntüleme yetkiniz yok."
            )
            
        return order


    # Diğer mevcut fonksiyonlar (Değişmedi/Zaten temizdi)
    async def create_from_cart(
        self, 
        db: AsyncSession, 
        user_id: int, 
        shipping_address: str
    ) -> orders:
        # ... (Önceki iş mantığı, stok kontrolü vb. burada kalır)
        cart_items = await cart_crud.get_multi_by_user(db, user_id=user_id)

        if not cart_items:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sepetiniz boş, sipariş verilemez.")
        
        # Karmaşık iş mantığı burada devam ediyor...
        total_amount = 0
        order_details_data = []

        for item in cart_items:
            watch = await watch_crud.get(db, id=item.WatchID) 
            
            if not watch:
                continue 
                
            if watch.Stock < item.Quantity:
                 raise HTTPException(
                     status_code=status.HTTP_400_BAD_REQUEST, 
                     detail=f"Stok yetersiz: {watch.ModelName} (Kalan: {watch.Stock})"
                 )

            line_total = watch.Price * item.Quantity
            total_amount += line_total
            
            order_details_data.append({
                "WatchID": watch.id,
                "Quantity": item.Quantity,
                "UnitPrice": watch.Price
            })
            
            # Stoktan düş
            watch.Stock -= item.Quantity
            db.add(watch)

        # Ana Sipariş Kaydını Oluştur
        new_order = orders(
            UserID=user_id,
            OrderDate=datetime.now(),
            TotalAmount=total_amount,
            Status="Hazırlanıyor",
            ShippingAddress=shipping_address
        )
        
        db.add(new_order)
        await db.flush() 
        await db.refresh(new_order)

        # Sipariş Detaylarını Kaydet
        for detail in order_details_data:
            new_detail = ordersdetails(
                OrderID=new_order.OrderID,
                WatchID=detail["WatchID"],
                Quantity=detail["Quantity"],
                UnitPrice=detail["UnitPrice"]
            )
            db.add(new_detail)

        # Sepeti Boşalt
        for item in cart_items:
            await cart_crud.remove(db, id=item.id)

        # Tüm işlemleri onayla
        await db.commit()
        await db.refresh(new_order)
        
        return new_order
    
    async def get_multi_by_user(self, db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100) -> List[orders]:
        query = select(self.model).where(self.model.UserID == user_id).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()


order = CRUDOrder(orders)