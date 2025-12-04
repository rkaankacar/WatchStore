from typing import Optional, TypeVar, Generic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from fastapi import HTTPException, status # <-- HATA FIIRLATMAYI BURAYA TAŞIYORUZ

from backend.crud.base import CRUDBase
from backend.models import Users
from backend.schemas import UserCreate, UserUpdate
from pydantic import BaseModel

# CRUDBase'den gelen T modelini Generic olarak tanımlama
ModelType = TypeVar("ModelType", bound=Users)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CRUDUser(CRUDBase[Users, UserCreate, UserUpdate]):
    
    # 1. KULLANICI OLUŞTURMA (Taşındı)
    async def create_user_with_check(self, db: AsyncSession, *, obj_in: UserCreate) -> Users:
        """
        Email kontrolü yapar, varsa 400 hatası fırlatır ve sonra kullanıcıyı hashleyerek oluşturur.
        """
        # Email kontrolü (Endpoint'ten taşındı)
        existing_user = await self.get_by_email(db, email=obj_in.email)
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, # 400 Bad Request
                detail="Bu email adresi zaten kullanılıyor."
            )
            
        # Orijinal create metodunun mantığı
        create_data = obj_in.model_dump(by_alias=True)
        plain_password = create_data.pop("Password")
        hashed_password = pwd_context.hash(plain_password)
        
        db_obj = Users(**create_data, Password=hashed_password)
        
        db.add(db_obj)
        await db.commit() 
        await db.refresh(db_obj)
        return db_obj

    # 3. KULLANICI DETAYI (Taşındı: 404 kontrolü)
    async def get_or_404(self, db: AsyncSession, *, id: int) -> ModelType:
        """
        Kullanıcıyı ID ile getirir. Bulunamazsa 404 HTTP hatası fırlatır.
        """
        user = await self.get(db, id=id)
        if user is None:
            # Hata fırlatma (Endpoint'ten taşındı)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Kullanıcı bulunamadı"
            )
        return user
        
    # 4. KULLANICI GÜNCELLEME (Taşındı: 404 kontrolü)
    async def update_or_404(
        self,
        db: AsyncSession,
        *,
        id: int, 
        obj_in: UserUpdate 
    ) -> Users:
        
        # Varlık kontrolü (404 fırlatma)
        user = await self.get_or_404(db, id=id)

        # Güncelleme işlemini gerçekleştirme
        return await super().update(db, db_obj=user, obj_in=obj_in)

    # 5. KULLANICI SİLME (Taşındı: 404 kontrolü)
    async def remove_or_404(self, db: AsyncSession, *, id: int) -> None:
        """
        Kullanıcıyı ID ile siler. Bulunamazsa 404 HTTP hatası fırlatır.
        """
        # Varlık kontrolü (404 fırlatma)
        await self.get_or_404(db, id=id)

        # Silme işlemini gerçekleştirme
        await super().remove(db, id=id)

    # Aşağıdaki fonksiyonlar zaten CRUD'daydı (değişmedi)
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[Users]:
        """Email ile kullanıcı bul (Async)"""
        query = select(Users).where(Users.Email == email)
        result = await db.execute(query)
        return result.scalars().first()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> Users:
         # Bu fonksiyon, artık create_user_with_check tarafından sarılacağı için
         # orijinal haliyle bırakılabilir (Base.CRUD'u çağırır). 
         # Ancak biz endpoint'te direk create_user_with_check'i kullanacağız.
         # (Orijinal hali, şifre hashleme mantığı içerdiği için bu dosyadaki CREATE'i kullanıyoruz.)
        create_data = obj_in.model_dump(by_alias=True)
        plain_password = create_data.pop("Password")
        hashed_password = pwd_context.hash(plain_password)
        
        db_obj = Users(**create_data, Password=hashed_password)
        
        db.add(db_obj)
        await db.commit() 
        await db.refresh(db_obj)
        return db_obj
        
    async def authenticate(self, db: AsyncSession, *, email: str, password: str) -> Optional[Users]:
        """Login kontrolü (Async)"""
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not pwd_context.verify(password, user.Password):
            return None
            
        return user

user = CRUDUser(Users)