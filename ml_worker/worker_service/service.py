from uuid import UUID

from worker_config.constants import RESPONSE_COST
from worker_database.repository.message_repository import MessageRepository
from worker_database.repository.transaction_repository import TransactionRepository


class Service:
    def __init__(self,
                 message_repository: MessageRepository,
                 transaction_repository: TransactionRepository,
                 ):
        self._message_repository = message_repository
        self._transaction_repository = transaction_repository


    async def process_success_result(self, message_id: UUID, prediction: str):
        await self._message_repository.add_prediction_to_message(message_id, prediction)

    async def process_unsuccess_result(self, message_id: UUID, user_id: UUID):
        await self._message_repository.set_message_unprocessed_status(message_id)
        await self._transaction_repository.create_refund_transaction(user_id, RESPONSE_COST)



