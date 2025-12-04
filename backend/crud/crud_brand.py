from typing import TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from pydantic import BaseModel

from backend.crud.base import CRUDBase
from backend.models import Brands
from backend.schemas import BrandCreate, BrandUpdate

ModelType = TypeVar("ModelType", bound=Brands)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBrand(CRUDBase[Brands, BrandCreate, BrandUpdate]):
    
    # Yeni Fonksiyon: 3. Endpoint için: Marka detayını getirir, bulunamazsa hata fırlatır.
    async def get_or_404(self, db: AsyncSession, *, id: int) -> ModelType:
        """
        Markayı ID ile getirir. Bulunamazsa 404 HTTP hatası fırlatır.
        """
        brand = await self.get(db, id=id)
        if brand is None:
            # Hata fırlatma (Endpoint'ten taşındı)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Marka bulunamadı"
            )
        return brand

    # Yeni Fonksiyon: 4. Endpoint için: Markayı günceller, önce varlığını kontrol eder.
    async def update_or_404(
        self,
        db: AsyncSession,
        *,
        id: int, 
        obj_in: BrandUpdate 
    ) -> Brands:
        
        # Varlık kontrolü (get_or_404 zaten hata fırlatacak)
        brand = await self.get_or_404(db, id=id)

        # Varsa, güncelleme işlemini CRUDBase'e devret
        return await super().update(db, db_obj=brand, obj_in=obj_in)

    # Yeni Fonksiyon: 5. Endpoint için: Markayı siler, önce varlığını kontrol eder.
    async def remove_or_404(self, db: AsyncSession, *, id: int) -> None:
        """
        Markayı ID ile siler. Bulunamazsa 404 HTTP hatası fırlatır.
        """
        # Varlık kontrolü (get_or_404 zaten hata fırlatacak)
        await self.get_or_404(db, id=id)

        # Varsa, silme işlemini CRUDBase'e devret
        await super().remove(db, id=id)


brand = CRUDBrand(Brands)