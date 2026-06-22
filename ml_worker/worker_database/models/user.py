from sqlalchemy.orm import Mapped, relationship

from worker_config.database import Base
from worker_database.models.types import uuid_pk, str_50, str_256
from worker_database.models.user_role import UserRole


class UserOrm(Base):
    __tablename__ = "user"

    id: Mapped[uuid_pk]
    name: Mapped[str_50]
    surname: Mapped[str_256]
    email: Mapped[str_50]
    passwordHash: Mapped[str]
    role: Mapped[UserRole]

    balance: Mapped["BalanceOrm"] = relationship(
        back_populates="user",
    )

    transactions: Mapped[list["TransactionOrm"]] = relationship(
        back_populates="user",
    )

