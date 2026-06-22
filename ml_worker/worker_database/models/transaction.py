from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from worker_config.database import Base
from worker_database.models.transaction_status import TransactionStatus
from worker_database.models.transaction_type import TransactionType
from worker_database.models.types import uuid_pk, created_dt, updated_dt


class TransactionOrm(Base):
    __tablename__ = "transaction"

    id: Mapped[uuid_pk]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    created_at: Mapped[created_dt]
    updated_at: Mapped[updated_dt]
    amount: Mapped[float]
    transaction_type: Mapped[TransactionType]
    transaction_status: Mapped[TransactionStatus]

    user: Mapped["UserOrm"] = relationship(
        back_populates="transactions"
    )