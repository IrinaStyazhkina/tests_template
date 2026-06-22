from uuid import UUID

from configuration.constants import RESPONSE_COST
from database.repository.chat_repository import ChatRepository
from database.repository.user_repository import UserRepository
from typing import List, Optional

from model.balance import Balance
from model.chat import Chat, ChatWithMessages
from model.transaction import Transaction
from model.transaction_type import TransactionType
from model.user import User


class UserService:
    def __init__(self, user_repository: UserRepository, transaction_repository, chat_repository: ChatRepository):
        self._user_repository = user_repository
        self._transaction_repository = transaction_repository
        self._chat_repository = chat_repository

    def get_users(self) -> List[User]:
        return self._user_repository.get_users()

    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        return self._user_repository.get_user_by_id(user_id)

    def add_money_to_balance(self, user_id: UUID, amount: float):
        if amount < 0:
            raise ValueError("Invalid sum to add")
        self._transaction_repository.create_transaction(
            user_id=user_id,
            amount=amount,
            type=TransactionType.DEPOSIT
        )

    def withdraw_for_prediction(self, user_id: UUID):
        transaction_result = self._transaction_repository.create_transaction(
            user_id=user_id,
            amount=RESPONSE_COST,
            type = TransactionType.WITHDRAWAL,
        )
        self._transaction_repository.approve_transaction(transaction_result.id)

    def get_user_transactions(self, user_id: UUID) -> List[Transaction]:
        return self._transaction_repository.get_transactions_by_user_id(user_id)

    def get_user_chats(self, user_id: UUID) -> List[ChatWithMessages]:
        return self._chat_repository.get_chats_with_messages_by_user_id(user_id)

    def get_user_balance(self, user_id: UUID) -> Optional[Balance]:
        return self._user_repository.get_user_balance(user_id)

    def create_chat(self, user_id: UUID, chat_name: str) -> Chat:
        return self._chat_repository.create_chat(user_id, chat_name)
