from typing import Any, List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.api import deps
from backend.crud.crud_return import return_crud
from backend.schemas import ReturnResponse, ReturnCreate, ReturnUpdate
from backend.models import users
 
router = APIRouter()

# 1. YENİ TALEP OLUŞTUR (Müşteri)
@router.post("/", response_model=ReturnResponse)
async def create_return_request(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    return_in: ReturnCreate,
    current_user: users = Depends(deps.get_current_user)
) -> Any:
    # UserID'yi token'dan gelen kullanıcıdan alıyoruz (Güvenlik için)
    return await return_crud.create_with_owner(
        db, obj_in=return_in, user_id=current_user.UserID
    )

# 2. TALEPLERİMİ LİSTELE (Müşteri)
@router.get("/my-requests", response_model=List[ReturnResponse])
async def read_my_returns(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: users = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100
) -> Any:
    return await return_crud.get_multi_by_user(
        db, user_id=current_user.UserID, skip=skip, limit=limit
    )

# 3. TÜM TALEPLERİ GÖR (Admin)
@router.get("/admin/all", response_model=List[ReturnResponse])
async def read_all_returns(
    db: AsyncSession = Depends(deps.get_async_db),
    current_admin: users = Depends(deps.get_current_admin_user),
    skip: int = 0,
    limit: int = 100
) -> Any:
    return await return_crud.get_multi(db, skip=skip, limit=limit)

# 4. TALEP DURUMU GÜNCELLE (Admin)
@router.patch("/admin/{return_id}/status", response_model=ReturnResponse)
async def update_return_status(
    return_id: int,
    status_in: ReturnUpdate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_admin: users = Depends(deps.get_current_admin_user)
) -> Any:
    return await return_crud.update_status(db, return_id=return_id, status_in=status_in)