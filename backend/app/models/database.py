from sqlalchemy import Column, String, Integer, Float, Text, DateTime, CheckConstraint
from sqlalchemy.sql import func
from app.core.database import Base
import uuid

class Summary(Base):
    __tablename__ = "summaries"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=True)

    # Input data
    source_type = Column(String(20), nullable=False)
    source_url = Column(Text, nullable=True)
    original_text = Column(Text, nullable=False)
    original_length = Column(Integer)

    # Summaries
    bart_summary = Column(Text)
    pegasus_summary = Column(Text)
    selected_summary = Column(String(50))  # bart or pegasus
    user_rating = Column(Integer)
    feedback_text = Column(Text)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("source_type IN ('text','url','file')", name="check_source_type"),
        CheckConstraint("user_rating >= 1 AND user_rating <= 5 OR user_rating IS NULL", name="check_rating"),
    )