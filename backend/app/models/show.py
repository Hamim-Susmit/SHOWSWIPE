import uuid
from datetime import datetime

from sqlalchemy import Date, DateTime, Float, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Show(Base):
    __tablename__ = "shows"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tmdb_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    original_language: Mapped[str] = mapped_column(String(8), default="en")
    poster_path: Mapped[str | None] = mapped_column(String(255))
    backdrop_path: Mapped[str | None] = mapped_column(String(255))
    overview: Mapped[str | None] = mapped_column(Text)
    tagline: Mapped[str | None] = mapped_column(Text)
    first_air_date: Mapped[datetime | None] = mapped_column(Date)
    vote_average: Mapped[float] = mapped_column(Float, default=0)
    vote_count: Mapped[int] = mapped_column(Integer, default=0)
    seasons: Mapped[int] = mapped_column(Integer, default=1)
    genres: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    platforms: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    cast: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    crew: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    soundtrack: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    trailer_key: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
