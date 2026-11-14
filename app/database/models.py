import uuid

from datetime import datetime, date, time, timezone

from sqlalchemy import (
    String,
    Integer,
    DateTime,
    Date,
    Time,
)
from sqlalchemy.orm import Mapped, mapped_column

# project imports
from app.database.base import Base


class Document(Base):
    __tablename__ = "documents_metadata"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    file_type: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    chunking_strategy: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    total_chunks: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class InterviewBooking(Base):
    __tablename__ = "interview_bookings"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    interview_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    interview_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
