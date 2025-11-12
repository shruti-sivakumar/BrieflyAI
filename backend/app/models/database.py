from sqlalchemy import Column, String, Integer, Float, Text, DateTime, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base

class Summary(Base):
    __tablename__ = "summaries"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=True)
    source_type = Column(String(20), nullable=False)
    source_url = Column(Text, nullable=True)
    original_text = Column(Text, nullable=False)
    original_length = Column(Integer)
    bart_summary = Column(Text)
    pegasus_summary = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("source_type IN ('text','url','file')", name="check_source_type"),
    )
