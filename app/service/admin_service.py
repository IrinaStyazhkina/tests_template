from typing import List
from uuid import UUID

from database.repository.transaction_repository import TransactionRepository
from database.repository.user_repository import UserRepository
from model.transaction import Transaction


class AdminService:
    def __init__(self,  user_repository: UserRepository, transaction_repository: TransactionRepository,):
        self._user_repository = user_repository
        self._transaction_repository = transaction_repository


    def approve_transaction(self, transaction_id: UUID):
        self._transaction_repository.approve_transaction(transaction_id)

    def decline_transaction(self, transaction_id: UUID):
        self._transaction_repository.decline_transaction(transaction_id)

    def get_all_transactions(self, limit: int = 10)-> List[Transaction]:
        return self._transaction_repository.get_transactions(limit)
