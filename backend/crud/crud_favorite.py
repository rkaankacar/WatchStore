from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status # <-- Hata fırlatma için gerekli

from backend.models.Favorite import Favorites
from backend.schemas import FavoriteCreate
from backend.models import Users # Sahiplik kontrolü için gerekli

class CRUDFavorites:
    
    # 3. YENİ FONKSİYON: FAVORİYE EKLEME (İş Mantığı Taşındı)
    async def create_or_get_existing(
        self, 
        db: AsyncSession, 
        obj_in: FavoriteCreate, 
        user_id: int
    ) -> Favorites:
        """
        Favori kaydının varlığını kontrol eder. Varsa mevcut olanı döner. Yoksa yeni oluşturur.
        Bu işlem, endpoint'teki idempotency (tekrar edilebilirliği) sağlar.
        """
        # 1. Varlık Kontrolü (Endpoint'ten taşındı)
        existing_fav = await self.get_by_user_and_watch(
            db, user_id=user_id, watch_id=obj_in.watch_id
        )

        if existing_fav:
            return existing_fav # Zaten varsa, mevcut olanı dön

        # 2. Yoksa: Yeni oluştur (Endpoint'ten taşındı)
        db_obj = Favorites(
            UserID=user_id,
            WatchID=obj_in.watch_id
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    # 4. YENİ FONKSİYON: FAVORİDEN ÇIKAR (İş Mantığı ve Güvenlik Kontrolü Taşındı)
    async def remove_by_id_with_ownership_check(
        self, 
        db: AsyncSession, 
        favorite_id: int, 
        current_user: Users
    ) -> None:
        """
        Favori kaydını ID ile siler. Silmeden önce varlık ve sahiplik kontrolü yapar.
        """
        # 1. Favori kaydını getir (get metodu zaten CRUD'da)
        fav_item: Optional[Favorites] = await self.get(db, id=favorite_id)

        # 2. Varlık Kontrolü (Endpoint'ten taşındı)
        if not fav_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Favori bulunamadı"
            )

        # 3. Sahiplik Kontrolü (Endpoint'ten taşındı)
        if fav_item.UserID != current_user.UserID:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Bu işlem için yetkiniz yok."
            )

        # 4. Silme işlemi
        await self.remove(db, id=favorite_id)
        # Geriye veri dönmeyeceği için None döndürebiliriz.

    # --- Mevcut Fonksiyonlar (Aşağıdakiler değişmedi) ---
    async def get_multi_by_user(
        self, db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Favorites]:
        query = select(Favorites).where(Favorites.UserID == user_id).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get(self, db: AsyncSession, id: int) -> Optional[Favorites]:
        query = select(Favorites).where(Favorites.id == id)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_user_and_watch(
        self, db: AsyncSession, user_id: int, watch_id: int
    ) -> Optional[Favorites]:
        query = select(Favorites).where(
            Favorites.UserID == user_id,
            Favorites.WatchID == watch_id
        )
        result = await db.execute(query)
        return result.scalars().first()

    async def create(
        self, db: AsyncSession, obj_in: FavoriteCreate, user_id: int
    ) -> Favorites:
        # Bu fonksiyon, artık create_or_get_existing tarafından sarılacağı için
        # orijinal haliyle bırakılabilir (ama kullanılmayacak).
        db_obj = Favorites(
            UserID=user_id,
            WatchID=obj_in.watch_id
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, id: int) -> Favorites:
        obj = await self.get(db, id=id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

favorites = CRUDFavorites()