from typing import List
from uuid import UUID

from authx import TokenPayload
from fastapi import APIRouter, Depends, HTTPException, Body

from deps import get_user_service, auth
from model.balance import Balance
from model.chat import ChatWithMessages, Chat
from model.transaction import Transaction
from model.user import User
from service.user_service import UserService

router = APIRouter(prefix="/api/users", tags=["User"])

@router.get(
    path="/current",
    description="Получение текущего пользователя",
    response_model=User
)
def get_current_user(user_service: UserService = Depends(get_user_service), payload: TokenPayload = Depends(auth.access_token_required)):
    id_from_token = payload.sub
    return user_service.get_user_by_id(UUID(id_from_token))

@router.get(
    path="/balance",
    description="Получение баланса пользователя",
    response_model=Balance
)
def get_balance(user_service: UserService = Depends(get_user_service), payload: TokenPayload = Depends(auth.access_token_required)):
    id_from_token = payload.sub
    return user_service.get_user_balance(UUID(id_from_token))

@router.post(
    path="/balance/add",
    description="Пополнение баланса",
)
def add_money_to_balance(amount: float = Body(..., embed=True), user_service: UserService = Depends(get_user_service), payload: TokenPayload = Depends(auth.access_token_required)):
    id_from_token = payload.sub
    try:
        user_service.add_money_to_balance(UUID(id_from_token), amount)
        return {"result": "ok"}
    except ValueError:
        raise HTTPException(400, "Не получилось пополнить баланс")

@router.get(
    path="/transactions",
    description="Получение всех транзакций текущего пользователя",
    response_model=List[Transaction]
)
def get_user_transactions(user_service: UserService = Depends(get_user_service), payload: TokenPayload = Depends(auth.access_token_required)):
    id_from_token = payload.sub
    return user_service.get_user_transactions(UUID(id_from_token))

@router.get(
    path="/chats",
    description="Получение всех чатов пользователя",
    response_model=List[ChatWithMessages]
)
def get_user_chats(user_service: UserService = Depends(get_user_service), payload: TokenPayload = Depends(auth.access_token_required)):
    id_from_token = payload.sub
    return user_service.get_user_chats(id_from_token)

@router.post(
    path="/chats/create",
    description="Создание чата",
    response_model=Chat
)
def create_chat(title: str = Body(..., embed=True), user_service: UserService = Depends(get_user_service), payload: TokenPayload = Depends(auth.access_token_required)):
    id_from_token = payload.sub
    return user_service.create_chat(UUID(id_from_token), title)
