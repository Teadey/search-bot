from datetime import datetime
from sqlalchemy import String, DateTime, BigInteger, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    tip: Mapped[str] = mapped_column(String(), nullable=True)
    number: Mapped[int] = mapped_column(BigInteger(), nullable=False)
    place: Mapped[str] = mapped_column(String(), nullable=True)
    birka: Mapped[str] = mapped_column(String(), nullable=True)
    comment: Mapped[str] = mapped_column(String(), nullable=True)
    gps: Mapped[str] = mapped_column(String(), nullable=True)
    copy_box_number: Mapped[str] = mapped_column(String(), nullable=True)
    created_on: Mapped[datetime] = mapped_column(DateTime(), default=func.now())
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(), default=func.now(), onupdate=func.now()
    )
