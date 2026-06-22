from uuid import UUID

from sqlalchemy import select

from worker_config.database import session_factory
from worker_database.models.balance import BalanceOrm
from worker_database.models.transaction import TransactionOrm
from worker_database.models.transaction_status import TransactionStatus
from worker_database.models.transaction_type import TransactionType


class TransactionRepository:

    def __init__(self):
        self._session = session_factory

    async def create_refund_transaction(self, user_id: UUID, amount: float):
        transaction = TransactionOrm(
            user_id = user_id,
            amount = amount,
            transaction_type = TransactionType.REFUND,
            transaction_status = TransactionStatus.COMPLETED,
        )

        async with self._session() as session:
            session.add(transaction)
            query = select(BalanceOrm).filter(BalanceOrm.user_id == user_id)
            result = await session.execute(query)
            balance = result.scalar_one()
            balance.amount += transaction.amount

            await session.commit()
