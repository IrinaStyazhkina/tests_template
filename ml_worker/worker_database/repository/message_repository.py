
from sqlalchemy import update
from uuid import UUID

from worker_config.database import session_factory
from worker_database.models.message import MessageOrm
from worker_database.models.message_status import MessageStatus


class MessageRepository:

    def __init__(self):
        self._session = session_factory

    async def add_prediction_to_message(self, message_id: UUID, prediction: str):
        async with self._session() as session:
            stmt = (
                update(MessageOrm)
                .where(MessageOrm.id == message_id)
                .values(content=prediction, message_status=MessageStatus.PROCESSED)
            )
            await session.execute(stmt)
            await session.commit()

    async def set_message_unprocessed_status(self, message_id: UUID):
        async with self._session() as session:
            stmt = (
                    update(MessageOrm)
                    .where(MessageOrm.id == message_id)
                    .values(message_status=MessageStatus.UNPROCESSED)
                )
            await session.execute(stmt)
            await session.commit()



