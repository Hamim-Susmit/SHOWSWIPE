import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class VoteType(str, enum.Enum):
    like = "like"
    nope = "nope"
    super = "super"
    skip = "skip"


class Vote(Base):
    __tablename__ = "votes"
    __table_args__ = (UniqueConstraint("show_id", "user_id", name="uq_show_user_vote"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    show_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("shows.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    circle_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("circles.id", ondelete="CASCADE"), nullable=False, index=True)
    vote_type: Mapped[VoteType] = mapped_column(Enum(VoteType, name="vote_type"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
