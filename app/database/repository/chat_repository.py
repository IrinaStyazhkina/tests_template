from typing import List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.database import session_factory
from database.models.chat import ChatOrm
from model.chat import Chat, ChatWithMessages


class ChatRepository:
    def __init__(self):
        self._session = session_factory

    def create_chat(self, user_id: UUID, chat_name: str) -> Chat:
        new_chat = ChatOrm(
            user_id=user_id,
            title = chat_name,
        )
        with self._session() as session:
            session.add(new_chat)
            session.commit()

            session.flush()
            return Chat.model_validate(new_chat, from_attributes=True)

    def get_chats_with_messages_by_user_id(self, user_id: UUID) -> List[ChatWithMessages]:
        with self._session() as session:
            query = select(ChatOrm).filter(ChatOrm.user_id == user_id).options(selectinload(ChatOrm.messages))
            result = session.execute(query)
            raw_chats = list(result.scalars().all())
            return [ChatWithMessages.model_validate(chat, from_attributes=True) for chat in raw_chats]
