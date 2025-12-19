from typing import TypeVar, List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy import delete
from sqlalchemy.orm import selectinload

# Modelleri import et
from backend.crud.base import CRUDBase
from backend.models import watches, watches_images, reviews, users, brands
from backend.schemas import WatchCreate, WatchUpdate, WatchImageCreate, WatchImageUpdate
from backend.crud.crud_cart import cart_crud
from backend.crud.crud_review import review
from backend.crud.crud_favorite import favorites_crud
from backend.exceptions import WatchNotFound
ModelType = TypeVar("ModelType", bound=watches)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

# --- SAATLER ---
class CRUDWatch(CRUDBase[watches, WatchCreate, WatchUpdate]):
    
    # Tüm ilişkileri yükleyen temel sorgu yapısı (MissingGreenlet çözümü)
    def _select_with_relationships(self):
        # KRİTİK DÜZELTME: Yorumları ve Yorumların içindeki kullanıcıları yüklüyoruz.
        return select(watches).options(
            selectinload(watches.brand),
            selectinload(watches.images),
            selectinload(watches.reviews).selectinload(reviews.user)
        )
    
    # -------------------------------------------------------------
    # 1. GET METOTLARI (EAGER LOADING EKLEME)
    # -------------------------------------------------------------
    
    async def get(self, db: AsyncSession, id: Any) -> Optional[watches]:
        query = self._select_with_relationships().where(watches.WatchID == id)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 100) -> List[watches]:
        query = self._select_with_relationships().offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    # -------------------------------------------------------------
    # 2. CREATE METODUNU OVERRIDE EDİYORUZ
    # -------------------------------------------------------------
    async def create(self, db: AsyncSession, *, obj_in: WatchCreate) -> watches:
        db_obj = await super().create(db, obj_in=obj_in)
        return await self.get(db, id=db_obj.WatchID)


    # -------------------------------------------------------------
    # 3. ÖZEL FİLTRE METOTLARI
    # -------------------------------------------------------------

    async def get_or_404(self, db: AsyncSession, *, id: int) -> ModelType:
        watch = await self.get(db, id=id)
        if watch is None:
            raise WatchNotFound()
        return watch

    async def update_or_404(
        self,
        db: AsyncSession,
        *,
        id: int,
        obj_in: WatchUpdate
    ) -> watches:
        watch = await self.get_or_404(db, id=id)
        return await super().update(db, db_obj=watch, obj_in=obj_in)

    async def remove_or_404(self, db: AsyncSession, *, id: int) -> None:
        
        await self.get_or_404(db, id=id)
        await cart_crud.remove_by_watch_id(db, watch_id=id)
        await review.remove_by_watch_id(db, watch_id=id)
        await watch_image.remove_by_watch_id(db, watch_id=id)
        await favorites_crud.remove_by_watch_id(db, watch_id=id)
        await super().remove(db, id=id)
        
    async def get_multi_by_gender(
        self,
        db: AsyncSession,
        *,
        gender: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[watches]:
        query = self._select_with_relationships()
        query = query.where(watches.Gender == gender)
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_multi_by_brand(
        self,
        db: AsyncSession,
        *,
        brand_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[watches]:
        query = self._select_with_relationships()
        query = query.where(watches.BrandID == brand_id)
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def search_watches(
        self,
        db: AsyncSession,
        *,
        query_str: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[watches]:
        """
        ModelName veya BrandName içerisinde arama yapar (Case Insensitive).
        """
        from sqlalchemy import or_

        stmt = self._select_with_relationships()
        stmt = stmt.join(watches.brand)  # Brand ile join yapilmali
        
        # ILIKE ile case-insensitive arama
        search_filter = or_(
            watches.ModelName.ilike(f"%{query_str}%"),
            brands.BrandName.ilike(f"%{query_str}%")
        )
        
        stmt = stmt.where(search_filter)
        stmt = stmt.offset(skip).limit(limit)
        
        result = await db.execute(stmt)
        return result.scalars().all()

# --- INSTANCE TANIMLAMALARI (En alta taşındı) ---

watch = CRUDWatch(watches)

class CRUDWatchImage(CRUDBase[watches_images, WatchImageCreate, WatchImageUpdate]):
    pass

    async def remove_by_watch_id(self, db: AsyncSession, *, watch_id: int) -> None:
        """Belirtilen WatchID'ye ait tüm resimleri siler."""
        stmt = delete(watches_images).where(watches_images.WatchID == watch_id)
        await db.execute(stmt)

watch_image = CRUDWatchImage(watches_images)