from typing import List
from uuid import UUID

from authx import TokenPayload
from fastapi import APIRouter, Depends, HTTPException

from deps import get_admin_service, auth
from model.transaction import Transaction
from model.user_role import UserRole
from service.admin_service import AdminService

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.get(
    path="/transactions/all",
    description="Получение транзакций всех пользователей",
    response_model=List[Transaction]
)
def get_all_transactions(admin_service: AdminService = Depends(get_admin_service), payload: TokenPayload = Depends(auth.access_token_required), limit: int = 10):
    role = payload.role
    if role != UserRole.ADMIN.name:
        raise HTTPException(403, "Недостаточно прав доступа")
    return admin_service.get_all_transactions(limit)

@router.patch(
    path="/transactions/approve/{transaction_id}",
    description="Одобрение транзакции"
)
def approve_transaction(transaction_id: str, admin_service: AdminService = Depends(get_admin_service), payload: TokenPayload = Depends(auth.access_token_required)):
    role = payload.role
    if role != UserRole.ADMIN.name:
        raise HTTPException(403, "Недостаточно прав доступа")
    admin_service.approve_transaction(UUID(transaction_id))
    return {"result": "ok"}

@router.patch(
    path="/transactions/decline/{transaction_id}",
    description="Отклонение транзакции"
)
def decline_transaction(transaction_id: str, admin_service: AdminService = Depends(get_admin_service), payload: TokenPayload = Depends(auth.access_token_required)):
    role = payload.role
    if role != UserRole.ADMIN.name:
        raise HTTPException(403, "Недостаточно прав доступа")
    admin_service.decline_transaction(UUID(transaction_id))
    return {"result": "ok"}
