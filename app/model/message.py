from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from model.message_status import MessageStatus
from model.message_type import MessageType


class Message(BaseModel):
    id: UUID
    chat_id: UUID
    content: str
    message_type: MessageType
    created_at: datetime
    message_status: MessageStatus
