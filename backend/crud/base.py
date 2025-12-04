from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.session import Base 

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """ID ile veri getirir (Async)"""
        # SQLAlchemy 1.4+ Async get metodu
        return await db.get(self.model, id)

    async def get_multi(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Listeleme yapar (Async)"""
        # db.query yerine select kullanıyoruz
        query = select(self.model).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """Kayıt oluşturur (Async)"""
        obj_in_data = obj_in.model_dump(by_alias=True)
        db_obj = self.model(**obj_in_data)
        
        db.add(db_obj)
        await db.commit()      # await eklendi
        await db.refresh(db_obj) # await eklendi
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Güncelleme yapar (Async)"""
        obj_data = {c.name: getattr(db_obj, c.name) for c in db_obj.__table__.columns}
        
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True, by_alias=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        await db.commit()      # await eklendi
        await db.refresh(db_obj) # await eklendi
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> Optional[ModelType]:
        """Siler (Async)"""
        # Önce veriyi çekmemiz lazım
        obj = await db.get(self.model, id)
        if obj:
            await db.delete(obj)     # await eklendi
            await db.commit()        # await eklendi
        return obj