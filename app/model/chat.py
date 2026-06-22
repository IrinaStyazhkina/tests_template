from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from model.message import Message


class Chat(BaseModel):
    id: UUID
    user_id: UUID
    created_at: datetime
    title: str

class ChatWithMessages(Chat):
    messages: list["Message"]
