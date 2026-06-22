import logging

from sqlalchemy import select
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import selectinload

from database.database import session_factory
from database.models.message import MessageOrm
from model.message import Message
from model.message_status import MessageStatus
from model.message_type import MessageType


class MessageRepository:

    def __init__(self):
        self._session = session_factory

    def add_message_to_chat(self, chat_id: UUID, input_data: str, message_type: MessageType, message_status: MessageStatus) -> Message:
        with self._session() as session:
            new_message = MessageOrm(
                    chat_id = chat_id,
                    content = input_data,
                    message_type = message_type,
                    message_status = message_status
                )
            session.add(new_message)
            session.commit()

            session.flush()
            return Message.model_validate(new_message, from_attributes=True)

    def get_message(self, message_id: UUID, user_id: UUID) -> Optional[Message]:
        with self._session() as session:
            query = select(MessageOrm).filter(MessageOrm.id == str(message_id)).options(selectinload(MessageOrm.chat))
            result = session.execute(query)
            raw_message = result.scalar_one_or_none()
            logging.warning(f"mes: {raw_message}")
            if raw_message and raw_message.chat.user_id == user_id:
                return Message.model_validate(raw_message, from_attributes=True)
            return None

