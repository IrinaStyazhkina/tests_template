from uuid import UUID

from authx import TokenPayload
from fastapi import APIRouter, Depends, HTTPException, Body

from configuration.constants import RESPONSE_COST
from deps import get_ml_service, auth, get_user_service
from service.ml_service import MLService
from service.user_service import UserService

router = APIRouter(prefix="/api/ml", tags=["ML Service"])

@router.post(
    path="/predict/{chat_id}",
    description="Запрос ответа от ML-сервиса",
)
def predict(
        chat_id: str,
        message:str = Body(..., embed=True),
        ml_service: MLService = Depends(get_ml_service),
        payload: TokenPayload = Depends(auth.access_token_required),
        user_service: UserService = Depends(get_user_service)):
    user_id = UUID(payload.sub)
    if user_service.get_user_balance(user_id).amount < RESPONSE_COST:
        raise HTTPException(400, "You don't have enough balance")
    user_service.withdraw_for_prediction(user_id)
    return { "request_id": ml_service.predict(message, UUID(chat_id), user_id)}

@router.get(
    path="/answer/{message_id}",
    description="Получение ответа от ML-сервиса",
)
def get_answer(message_id: str, ml_service: MLService = Depends(get_ml_service), payload: TokenPayload = Depends(auth.access_token_required)):
    id_from_token = payload.sub
    return { "message": ml_service.get_answer(UUID(message_id), UUID(id_from_token))}

