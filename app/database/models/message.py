from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from database.database import Base
from database.models.types import uuid_pk, str_3000, created_dt
from model.message_status import MessageStatus
from model.message_type import MessageType


class MessageOrm(Base):
    __tablename__ = "message"

    id: Mapped[uuid_pk]
    chat_id: Mapped[UUID] = mapped_column(ForeignKey("chat.id", ondelete="CASCADE"))
    content: Mapped[str_3000]
    message_type: Mapped[MessageType]
    created_at: Mapped[created_dt]
    message_status: Mapped[MessageStatus]

    chat: Mapped["ChatOrm"] = relationship(
        back_populates="messages"
    )