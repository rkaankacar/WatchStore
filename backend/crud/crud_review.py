from typing import List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload 

from backend.crud.base import CRUDBase
from backend.models import reviews, users, watches, brands 
from backend.schemas import ReviewCreate, ReviewUpdate

class CRUDReview(CRUDBase[reviews, ReviewCreate, ReviewUpdate]):
    
    # 🎯 KRİTİK DÜZELTME: İlişkileri 4 kademeli yükleyen temel sorgu yapısı
    def _select_with_relationships(self):
        """Yorumun bağlı olduğu user ve watch ilişkilerini, watch'ın markası dahil yükler."""
        return select(reviews).options(
            selectinload(reviews.user), 
            selectinload(reviews.watch).selectinload(watches.brand) 
        )

    # -------------------------------------------------------------
    # 1. GET METOTLARI (EAGER LOADING İLE GÜNCELLENDİ)
    # -------------------------------------------------------------
    
    async def get(self, db: AsyncSession, id: Any) -> Optional[reviews]:
        query = self._select_with_relationships().where(reviews.ReviewID == id)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 100) -> List[reviews]:
        query = self._select_with_relationships().offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
        
    async def get_by_watch(self, db: AsyncSession, *, watch_id: int, skip: int = 0, limit: int = 100) -> List[reviews]:
        """
        Belirli bir saate ait yorumları getirir (Async) ve ilişkileri yükler.
        """
        query = self._select_with_relationships().where(reviews.WatchID == watch_id).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    # -------------------------------------------------------------
    # 2. CREATE METODU (İLİŞKİ YÜKLEMEYİ SAĞLAMAK İÇİN OVERRIDE EDİLDİ)
    # -------------------------------------------------------------
    async def create_review_with_user(
        self,
        db: AsyncSession,
        *,
        obj_in: ReviewCreate,
        user: users
    ) -> reviews:
        
        db_obj = reviews(
            UserID=user.UserID,
            WatchID=obj_in.watch_id,
            Rating=obj_in.rating,
            Comment=obj_in.comment
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        
        # Tam yüklenmiş objeyi döndür
        return await self.get(db, id=db_obj.ReviewID)

    # -------------------------------------------------------------
    # 3. REMOVE METODU (Aynı kaldı)
    # -------------------------------------------------------------
    async def remove_review_with_ownership_check(
        self,
        db: AsyncSession,
        *,
        review_id: int,
        current_user: users
    ) -> None:
        
        review_to_delete: Optional[reviews] = await self.get(db, id=review_id)
        
        if not review_to_delete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Yorum bulunamadı")
        
        if review_to_delete.UserID != current_user.UserID:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sadece kendi yorumunuzu silebilirsiniz.")
        
        await self.remove(db, id=review_id)

review = CRUDReview(reviews)