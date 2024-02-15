from datetime import datetime
from sqlalchemy import String, DateTime, BigInteger, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .tables import User
from .address import Address


class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(User.id, ondelete="CASCADE"), nullable=False
    )
    address_id: Mapped[int] = mapped_column(
        ForeignKey(Address.id, ondelete="CASCADE"), nullable=False
    )
    text: Mapped[str] = mapped_column(String(), nullable=False)
    created_on: Mapped[datetime] = mapped_column(DateTime(), default=func.now())
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(), default=func.now(), onupdate=func.now()
    )
