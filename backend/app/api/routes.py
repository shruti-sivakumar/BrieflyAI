from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.summarization import summarization_service
from app.models.database import Summary
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
import uuid

router = APIRouter()

class SummarizeTextRequest(BaseModel):
    text: str
    user_id: str | None = None  # optional

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/summarize/text")
async def summarize_text(request: SummarizeTextRequest, db: Session = Depends(get_db)):
    """Summarize text and save result to database"""
    if len(request.text.split()) < 50:
        raise HTTPException(status_code=400, detail="Text too short. Minimum 50 words required.")

    result = await summarization_service.summarize_text(request.text)

    # Save to database
    new_summary = Summary(
        id=str(uuid.uuid4()),
        user_id=request.user_id,
        source_type="text",
        original_text=request.text,
        original_length=result["original_length"],
        bart_summary=result["bart"]["summary"],
        pegasus_summary=result["pegasus"]["summary"]
    )

    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)

    result["summary_id"] = new_summary.id
    result["created_at"] = new_summary.created_at

    return result