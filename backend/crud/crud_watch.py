from typing import Optional, TypeVar, Generic
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from pydantic import BaseModel

from backend.crud.base import CRUDBase
from backend.models import Watches, Watches_Images
from backend.schemas import WatchCreate, WatchUpdate, WatchImageCreate, WatchImageUpdate

# CRUDBase'den gelen T modelini Generic olarak tanımlama (T = Watches)
ModelType = TypeVar("ModelType", bound=Watches)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

# --- SAATLER ---
class CRUDWatch(CRUDBase[Watches, WatchCreate, WatchUpdate]):
    
    # 3. Endpoint için: Saat detayını getirir, bulunamazsa hata fırlatır.
    async def get_or_404(self, db: AsyncSession, *, id: int) -> ModelType:
        """
        Saati ID ile getirir. Bulunamazsa 404 HTTP hatası fırlatır.
        """
        watch = await self.get(db, id=id)
        if watch is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Saat bulunamadı"
            )
        return watch

    # 4. Endpoint için: Saati günceller, önce varlığını kontrol eder.
    async def update_or_404(
        self,
        db: AsyncSession,
        *,
        id: int, # Güncellenecek saatin ID'si
        obj_in: WatchUpdate # Güncelleme verisi
    ) -> Watches:
        
        # Önce saatin varlığını kontrol et ve 404 fırlat
        watch = await self.get_or_404(db, id=id)

        # Varsa, CRUDBase'deki orijinal update metodunu çağır
        return await super().update(db, db_obj=watch, obj_in=obj_in)

    # 5. Endpoint için: Saati siler, önce varlığını kontrol eder.
    async def remove_or_404(self, db: AsyncSession, *, id: int) -> None:
        """
        Saati ID ile siler. Bulunamazsa 404 HTTP hatası fırlatır.
        """
        # Önce saatin varlığını kontrol et (get_or_404 zaten hata fırlatacak)
        await self.get_or_404(db, id=id)

        # Varsa, CRUDBase'deki orijinal remove metodunu çağır
        await super().remove(db, id=id)

watch = CRUDWatch(Watches)

# --- SAAT RESİMLERİ (Değişmedi) ---
class CRUDWatchImage(CRUDBase[Watches_Images, WatchImageCreate, WatchImageUpdate]):
    pass

watch_image = CRUDWatchImage(Watches_Images)