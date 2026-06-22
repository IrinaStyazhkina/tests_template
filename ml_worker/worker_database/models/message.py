from uuid import UUID

from sqlalchemy.orm import Mapped

from worker_config.database import Base
from worker_database.models.message_status import MessageStatus
from worker_database.models.message_type import MessageType
from worker_database.models.types import uuid_pk, str_3000, created_dt


class MessageOrm(Base):
    __tablename__ = "message"

    id: Mapped[uuid_pk]
    chat_id: Mapped[UUID]
    content: Mapped[str_3000]
    message_type: Mapped[MessageType]
    created_at: Mapped[created_dt]
    message_status: Mapped[MessageStatus]