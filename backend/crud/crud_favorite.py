from typing import List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select 
from sqlalchemy.orm import selectinload 
from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import delete
# CRUDBase'i kullanmıyorsun, bu yüzden bu import kaldırıldı
# from backend.crud.base import CRUDBase 

# 🎯 DÜZELTME 1: Model Sınıfını (Favorites) ve diğerlerini doğru yoldan import ediyoruz
from backend.models import favorites as FavoritesModel # Model Sınıfına yeni isim verdik
from backend.models import users, watches 
from backend.schemas import FavoriteCreate, FavoriteResponse

class CRUDFavorites:

    # Tüm ilişkileri yükleyen temel sorgu yapısı
    def _select_with_relationships(self):
        # 🎯 KRİTİK DÜZELTME 2: select() içine CRUD nesnesi değil, MODEL SINIFI verilir.
        return select(FavoritesModel).options(
            # İlişkilerde de Model Sınıfının ilişkileri kullanılır (FavoritesModel.user)
            selectinload(FavoritesModel.user),
            
            # Watch'ı ve içindeki Brand'ı yüklüyoruz.
            selectinload(FavoritesModel.watch).selectinload(watches.brand)
        )

    # -------------------------------------------------------------
    # 1. GET METOTLARI (EAGER LOADING)
    # -------------------------------------------------------------
    
    # Geri dönüş tiplerinde de model sınıfı kullanıldı (favorites -> FavoritesModel)
    async def get(self, db: AsyncSession, id: Any) -> Optional[FavoritesModel]:
        query = self._select_with_relationships().where(FavoritesModel.FavoriteID == id)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_by_user_and_watch(
        self, db: AsyncSession, *, user_id: int, watch_id: int
    ) -> Optional[FavoritesModel]:
        query = self._select_with_relationships().where(
            FavoritesModel.UserID == user_id, 
            FavoritesModel.WatchID == watch_id
        )
        result = await db.execute(query)
        return result.scalars().first()

    async def get_multi_by_user(
        self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[FavoritesModel]:
        query = (
            self._select_with_relationships()
            .where(FavoritesModel.UserID == user_id)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()


    # -------------------------------------------------------------
    # 2. CREATE METOTLARI (Yeniden Çekme Garantisi)
    # -------------------------------------------------------------

    async def create_or_get_existing(
        self, db: AsyncSession, *, obj_in: FavoriteCreate, user_id: int
    ) -> FavoritesModel:
        
        # 1. Var mı kontrol et
        existing_fav = await self.get_by_user_and_watch(
            db, user_id=user_id, watch_id=obj_in.watch_id
        )
        if existing_fav:
            return existing_fav

        # 2. Yoksa oluştur
        db_obj = FavoritesModel( # 🎯 DÜZELTME: favorites yerine FavoritesModel kullanıldı
            UserID=user_id,
            WatchID=obj_in.watch_id
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        # FIX: Objenin tam yüklü halini döndür
        return await self.get(db, id=db_obj.FavoriteID) # favoriteID yerine FavoriteID kullanılmalı


    # -------------------------------------------------------------
    # 3. DELETE METOTLARI
    # -------------------------------------------------------------
    
    async def remove_by_id_with_ownership_check(
        self, db: AsyncSession, *, favorite_id: int, current_user: users
    ) -> None:
        
        fav_to_remove = await self.get(db, id=favorite_id)

        if not fav_to_remove:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favori öğesi bulunamadı"
            )

        if fav_to_remove.UserID != current_user.UserID:
              raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bu favori öğesini silme yetkiniz yok"
            )

        await db.delete(fav_to_remove)
        await db.commit()
    async def remove_by_watch_id(self, db: AsyncSession, *, watch_id: int) -> None:
        """Belirtilen WatchID'ye ait tüm favori kayıtlarını siler."""
        
        # SORGULAMA: Favorite modelini ve WatchID sütununu kullanarak DELETE sorgusu oluşturma
        stmt = delete(FavoritesModel).where(FavoritesModel.WatchID == watch_id)
        await db.execute(stmt)

# 🎯 KRİTİK DÜZELTME 3: CRUD nesnesini çakışmayacak şekilde adlandır
favorites_crud = CRUDFavorites()