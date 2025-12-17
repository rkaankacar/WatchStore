from typing import Optional, TypeVar, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from fastapi import HTTPException, status 
from pydantic import BaseModel

from backend.crud.base import CRUDBase
from backend.models import users
from backend.schemas import UserCreate, UserUpdate, UserSimpleResponse
from backend.exceptions import (
    UserNotFound, 
    UserAlreadyExists,
    PasswordIncorrect,
    PasswordMismatch,
    PasswordSame
)

# Şifre hashleme context'i
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# TypeVar'lar
ModelType = TypeVar("ModelType", bound=users)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDUser(CRUDBase[users, UserCreate, UserUpdate]):
    
    # -------------------------------------------------------------
    # 1. TEMEL KONTROL METOTLARI
    # -------------------------------------------------------------
    
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[users]:
        """Email ile kullanıcı bul (Async)"""
        # Burada obj_in'i kullanmadığımız için sorun yok.
        query = select(users).where(users.Email == email) 
        result = await db.execute(query)
        return result.scalars().first()

    # -------------------------------------------------------------
    # 2. ÖZEL CREATE METOTLARI
    # -------------------------------------------------------------
    
    async def create_user_with_check(self, db: AsyncSession, *, obj_in: UserCreate) -> users:
        """
        Email kontrolü yapar, varsa 400 hatası fırlatır ve sonra kullanıcıyı hashleyerek oluşturur.
        """
        # 1. Email kontrolü
        # obj_in.email kullanıyoruz. (Şema Pydantic standardına uyduğu için.)
        existing_user = await self.get_by_email(db, email=obj_in.email)
        
        if existing_user:
            raise UserAlreadyExists()
            
        # 2. Veriyi hazırlar ve ŞİFREYİ HASH'LER
        create_data = obj_in.model_dump(by_alias=True, exclude_unset=True) 
        
        # 🎯 FIX 1: Şifre anahtarını BÜYÜK HARFLE (Alias adı) çekiyoruz.
        # Bu, Password alanının Users modeline iki kez gitmesini önler.
        plain_password = create_data.pop("Password") 
        hashed_password = pwd_context.hash(plain_password)
        
        # 3. Model nesnesini oluşturur. (create_data'da artık şifre yok, anahtarlar Model ile uyumlu.)
        db_obj = users(**create_data, Password=hashed_password) 
        
        # 4. Kaydetme işlemi
        db.add(db_obj)
        await db.commit() 
        await db.refresh(db_obj)
        return db_obj

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> users:
        # Bu metot da aynı sorunu yaşıyordu, düzeltildi.
        create_data = obj_in.model_dump(by_alias=True)
        # 🎯 FIX 2: Şifre anahtarını BÜYÜK HARFLE (Alias adı) çekiyoruz.
        plain_password = create_data.pop("Password") 
        hashed_password = pwd_context.hash(plain_password)
        
        db_obj = users(**create_data, Password=hashed_password)
        
        db.add(db_obj)
        await db.commit() 
        await db.refresh(db_obj)
        return db_obj

    # -------------------------------------------------------------
    # 3. KULLANICI DETAY VE KONTROL METOTLARI (Aynen Kalır)
    # -------------------------------------------------------------
    
    async def get_or_404(self, db: AsyncSession, *, id: int) -> ModelType:
        
        user = await self.get(db, id=id) 
        if user is None:
            raise UserNotFound()
        return user
        
    async def update_or_404(
        self,
        db: AsyncSession,
        *,
        id: int, 
        obj_in: UserUpdate 
    ) -> users:
        """Kullanıcıyı günceller (404 kontrolü ile)"""
        user = await self.get_or_404(db, id=id)
        return await super().update(db, db_obj=user, obj_in=obj_in)

    async def remove_or_404(self, db: AsyncSession, *, id: int) -> None:
        """Kullanıcıyı siler (404 kontrolü ile)"""
        await self.get_or_404(db, id=id)
        await super().remove(db, id=id)
        
    # 4. AUTH METOTLARI
    async def authenticate(self, db: AsyncSession, *, email: str, password: str) -> Optional[users]:
        """Login kontrolü (Async)"""
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        # Not: Modelde büyük harf olduğu için user.Password kullanılır.
        if not pwd_context.verify(password, user.Password): 
            return None
            
        return user

    async def change_password_with_confirm(
        self,
        db: AsyncSession,
        *,
        user_id: int,
        current_password: str,
        new_password: str,
        new_password_again: str
    ) -> users:
        """
        Kullanıcının şifresini değiştirir.
        1) Mevcut şifre doğru mu kontrol eder.
        2) Yeni şifre tekrar ile aynı mı kontrol eder.
        3) Yeni şifreyi hashleyip günceller.
        """

        # 1. Kullanıcı var mı kontrol et
        user = await self.get_or_404(db, id=user_id)

        # 2. Mevcut şifre doğru mu?
        if not pwd_context.verify(current_password, user.Password):
            raise PasswordIncorrect()

        # 3. Yeni şifre ile tekrarı aynı mı?
        if new_password != new_password_again:
            raise PasswordMismatch()

        # 4. Yeni şifre mevcut şifre ile aynı mı? (Güvenlik kontrolü)
        if pwd_context.verify(new_password, user.Password):
            raise PasswordSame()

        # 5. Yeni şifreyi hashle
        hashed_password = pwd_context.hash(new_password)

        # 6. Şifreyi güncelle
        user.Password = hashed_password

        # 7. DB'ye kaydet
        db.add(user)
        await db.commit()
        await db.refresh(user)

        return user

    async def get_or_profile(self, db: AsyncSession, *, id: int) -> UserSimpleResponse:
        user = await self.get(db, id=id)
        if not user:
            raise UserNotFound()
        
        return UserSimpleResponse.model_validate(user, from_attributes=True)
    
user = CRUDUser(users)