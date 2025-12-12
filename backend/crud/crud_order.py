from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload 
from datetime import datetime
from fastapi import HTTPException, status
from decimal import Decimal
from backend.crud.base import CRUDBase
# İLİŞKİSEL YÜKLEME İÇİN GEREKLİ MODELLER
from backend.models import orders, ordersdetails, cart, watches, users 
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

    # KRİTİK DÜZELTME: EAGER LOADING YARDIMCI METODU
    def _get_eager_options(self):
        """
        MissingGreenlet hatasını çözmek için gerekli 3 katmanlı Eager Loading zincirini döndürür:
        Order -> User
        Order -> OrderDetails -> Watch -> Brand
        """
        return [
            selectinload(self.model.user), # 1. Katman: User
            
            # 2. Katman: OrderDetails'i yükle
            selectinload(self.model.order_details) 
                # 3. Katman: OrderDetail içindeki Saati yükle
                .selectinload(ordersdetails.watch) 
                
                # 4. Katman: Saatin içindeki Markayı yükle (SON EKSİK PARÇA)
                .selectinload(watches.brand) 
        ]

    # -----------------------------------------------
    # 1. ADMIN LISTELEME (Zaten Düzeltildi)
    async def get_multi(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[orders]:
        """Tüm siparişleri, gerekli tüm ilişkisel verileri (Brand dahil) önceden yükleyerek getirir."""
        query = (
            select(self.model)
            .options(*self._get_eager_options())
            .offset(skip)
            .limit(limit)
        )
        
        result = await db.execute(query)
        return result.scalars().unique().all()
        
    # -----------------------------------------------
    # 2. KULLANICI LİSTELEME (Zaten Düzeltildi)
    async def get_multi_by_user(self, db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100) -> List[orders]:
        """Belirli bir kullanıcıya ait siparişleri, gerekli tüm ilişkisel verileri önceden yükleyerek getirir."""
        query = (
            select(self.model)
            .where(self.model.UserID == user_id)
            .options(*self._get_eager_options())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().unique().all()


    # -----------------------------------------------
    # 3. KULLANICI DETAY GÖRÜNTÜLEME (Zaten Düzeltildi)
    async def get_order_by_user_id_or_404(
        self, 
        db: AsyncSession, 
        *, 
        order_id: int, 
        current_user: users
    ) -> orders:
        """
        Siparişi ID ile getirir (Eager Loading kullanarak). Yoksa 404, kullanıcıya ait değilse 403 fırlatır.
        """
        query = (
            select(self.model)
            .where(self.model.OrderID == order_id)
            .options(*self._get_eager_options()) # Tüm ilişkileri yüklüyoruz
        )
        result = await db.execute(query)
        order = result.scalars().first()
        
        # 1. Varlık Kontrolü
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Sipariş bulunamadı"
            )
            
        # 2. Sahiplik Kontrolü
        if order.UserID != current_user.UserID:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Bu siparişi görüntüleme yetkiniz yok."
            )
            
        return order
    
    # -----------------------------------------------
    # 4. SİPARİŞ OLUŞTURMA (DEĞİŞMEDİ)
    async def create_from_cart(
        self, 
        db: AsyncSession, 
        user_id: int, 
        shipping_address: str
    ) -> orders:
        # ... (Stok kontrolü ve sipariş oluşturma mantığı aynı kalır) ...
        # Bu fonksiyonun içi, önceki gönderdiğiniz haliyle korunmuştur.

        cart_items = await cart_crud.get_multi_by_user(db, user_id=user_id)

        if not cart_items:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sepetiniz boş, sipariş verilemez.")
        
        # Karmaşık iş mantığı burada devam ediyor...
        total_amount = Decimal("0.0")
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

            line_total = Decimal(str(watch.Price)) * item.Quantity
            total_amount += line_total
            
            order_details_data.append({
                "WatchID": watch.WatchID,
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
            await cart_crud.remove(db, id=item.CartID)

        # Tüm işlemleri onayla
        await db.commit()
        await db.refresh(new_order)
        
        return new_order


    # -----------------------------------------------
    # 5. DURUM GÜNCELLEME (KRİTİK DÜZELTME YAPILDI)
    async def update_status(
    self,
    db: AsyncSession,
    *,
    order_id: int,
    status_in: OrderUpdate 
    ) -> orders:
        """Siparişin durumunu günceller ve güncel siparişi Eager Loading ile döndürür."""
    
    # 1. Siparişi çek (Basit çekme yeterli, sadece varlık kontrolü için)
        order = await self.get(db, id=order_id) 

        if not order:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Sipariş bulunamadı"
        )

    # 2. Güncelleme İşlemini Gerçekleştir (self.update içinde commit olmadığı varsayımıyla devam ediyoruz)
    # db_obj'yi güncelleyen metod çağrılır.
        updated_order_lazy = await self.update(db, db_obj=order, obj_in=status_in)

    
        query = (
        select(self.model)
        .where(self.model.OrderID == order_id)
        .options(*self._get_eager_options()) 
    )
        result = await db.execute(query)
        updated_order_eager = result.scalars().first()
    
    
        if not updated_order_eager:
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Sipariş güncellendi ancak ilişkili veri çekilemedi. Veritabanı hatası."
         )

        return updated_order_eager
            
            
             
    async def update_user_order_status(
    self,
    db: AsyncSession,
    *,
    order_id: int,
    status_in: OrderUpdate,
    current_user: users
) -> orders:
  
    # 1. Siparişi Eager Loading ile çek (Response için tüm veriler yüklü olmalı)
        query = select(self.model).where(self.model.OrderID == order_id).options(*self._get_eager_options())
        result = await db.execute(query)
        order = result.scalars().first()

    # Varlık kontrolü
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sipariş bulunamadı.")
    
    # Sahiplik kontrolü
        if order.UserID != current_user.UserID:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bu siparişe erişim yetkiniz yok.")

    # İptal etme kuralı kontrolü
        new_status = status_in.model_dump(exclude_unset=True, by_alias=True).get("Status")
    
        if new_status == 'İptal Edildi':
            if order.Status != 'Hazırlanıyor':
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Sipariş '{order.Status}' durumunda olduğu için iptal edilemez."
            )
            
        # Güncelleme ve Commit
            order.Status = new_status
            db.add(order)
            await db.commit()
            await db.refresh(order)
        
        # Stokları geri ekleme mantığı BURAYA EKLENMELİDİR (Gerekirse)
        # Eğer iptal edilen ürünlerin stoğu geri ekleniyorsa, o mantık buraya gelir.
        
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bu endpoint sadece 'İptal Edildi' durumu için kullanılabilir.")

    # Eager Loading ile çekilmiş siparişi döndür
    # Zaten sorguyu Eager Loading ile yaptığımız için 'order' nesnesini döndürebiliriz.
        return order
order = CRUDOrder(orders)