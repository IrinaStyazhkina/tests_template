from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from database.database import Base
from database.models.types import uuid_pk, created_dt, str_256


class ChatOrm(Base):
    __tablename__ = "chat"

    id: Mapped[uuid_pk]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    created_at: Mapped[created_dt]
    title: Mapped[str_256]

    user: Mapped["UserOrm"] = relationship(
        back_populates="chats"
    )

    messages: Mapped[list["MessageOrm"]] = relationship(
        back_populates="chat"
    )