from typing import TypeVar, List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy.future import select 
from sqlalchemy.orm import selectinload 

from backend.crud.base import CRUDBase
from backend.models import brands
from backend.schemas import BrandCreate, BrandUpdate

ModelType = TypeVar("ModelType", bound=brands)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBrand(CRUDBase[brands, BrandCreate, BrandUpdate]):
    
    # -------------------------------------------------------------
    # 1. TEMEL GET METODLARINI GÜNCELLİYORUZ (MissingGreenlet Çözümü)
    # -------------------------------------------------------------
    
    # Tek kayıt getirirken ilişkili saatleri de yükle
    async def get(self, db: AsyncSession, id: Any) -> Optional[brands]:
        query = (
            select(brands)
            .options(selectinload(brands.watches)) 
            .where(brands.BrandID == id)
        )
        result = await db.execute(query)
        return result.scalars().first()

    # Liste getirirken ilişkili saatleri de yükle
    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[brands]:
        query = (
            select(brands)
            .options(selectinload(brands.watches))
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    # -------------------------------------------------------------
    # 2. CREATE METODUNU OVERRIDE EDİYORUZ (POST /brands/ için çözüm)
    # -------------------------------------------------------------
    async def create(
        self, db: AsyncSession, *, obj_in: BrandCreate
    ) -> brands:
        
        # 1. Objenin kendisini CRUDBase ile oluştur
        # Bu obje henüz watches ilişkisini yüklememiştir.
        db_obj = await super().create(db, obj_in=obj_in)
        
        # 2. Obje oluşturulduktan sonra, tam yüklenmiş (eagerly loaded) halini çek
        # Bu, BrandResponse'un istediği "watches" ilişkisini doldurur.
        return await self.get(db, id=db_obj.BrandID)


    # -------------------------------------------------------------
    # 3. SENİN EKLEDİĞİN ÖZEL METODLAR (Aynen koruyoruz)
    # -------------------------------------------------------------

    # Yeni Fonksiyon: 3. Endpoint için: Marka detayını getirir, bulunamazsa hata fırlatır.
    async def get_or_404(self, db: AsyncSession, *, id: int) -> ModelType:
        """
        Markayı ID ile getirir. Bulunamazsa 404 HTTP hatası fırlatır.
        """
        # Artık self.get() ilişkiyi yüklüyor.
        brand = await self.get(db, id=id)
        if brand is None:
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
    ) -> brands:
        
        # Varlık kontrolü
        brand = await self.get_or_404(db, id=id)

        # Varsa, güncelleme işlemini CRUDBase'e devret
        return await super().update(db, db_obj=brand, obj_in=obj_in)

    # Yeni Fonksiyon: 5. Endpoint için: Markayı siler, önce varlığını kontrol eder.
    async def remove_or_404(self, db: AsyncSession, *, id: int) -> None:
        """
        Markayı ID ile siler. Varlık ve sahiplik kontrolü CRUD'a taşındı.
        """
        # Varlık kontrolü
        await self.get_or_404(db, id=id)

        # Varsa, silme işlemini CRUDBase'e devret
        await super().remove(db, id=id)


brand = CRUDBrand(brands)