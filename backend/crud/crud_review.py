from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

from backend.crud.base import CRUDBase
from backend.models import Reviews, Users
from backend.schemas import ReviewCreate, ReviewUpdate

class CRUDReview(CRUDBase[Reviews, ReviewCreate, ReviewUpdate]):

    # Mevcut Fonksiyon (1. Endpoint tarafından kullanılıyor)
    async def get_by_watch(self, db: AsyncSession, *, watch_id: int, skip: int = 0, limit: int = 100) -> List[Reviews]:
        """
        Belirli bir saate ait yorumları getirir (Async).
        """
        query = select(Reviews).where(Reviews.WatchID == watch_id).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    # Yeni Fonksiyon: 2. YORUM YAP işlevinin mantığını üstlenir.
    async def create_review_with_user(
        self,
        db: AsyncSession,
        *,
        obj_in: ReviewCreate,
        user: Users
    ) -> Reviews:
        """
        Token'dan alınan UserID'yi kullanarak yeni bir yorum oluşturur.
        """
        # Veritabanı modelini oluşturma (Endpoint'ten taşındı)
        db_obj = Reviews(
            UserID=user.UserID,
            WatchID=obj_in.watch_id,
            Rating=obj_in.rating,
            Comment=obj_in.comment
        )
        # Veritabanı işlemlerini yapma (Endpoint'ten taşındı)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    # Yeni Fonksiyon: 3. YORUM SİL işlevinin mantığını üstlenir (Sahiplik Kontrolü dahil).
    async def remove_review_with_ownership_check(
        self,
        db: AsyncSession,
        *,
        review_id: int,
        current_user: Users
    ) -> None:
        """
        Yorumu siler, ancak yalnızca yorumun sahibi ise.
        """
        # Yorumu bulma (Endpoint'ten taşındı, sadece çağrı kaldı)
        review: Optional[Reviews] = await self.get(db, id=review_id)
        
        if not review:
            # Hata fırlatma (Endpoint'ten taşındı)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Yorum bulunamadı")
        
        # SAHİPLİK KONTROLÜ (Endpoint'ten taşındı)
        if review.UserID != current_user.UserID:
            # Hata fırlatma (Endpoint'ten taşındı)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sadece kendi yorumunuzu silebilirsiniz.")
        
        # Yorumu silme
        await self.remove(db, id=review_id)
        # return None (Zaten 204 No Content dönecek)


review = CRUDReview(Reviews)