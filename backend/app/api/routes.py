from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel, HttpUrl
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

# --- URL summarization ---
class SummarizeURLRequest(BaseModel):
    url: HttpUrl
    user_id: str | None = None

@router.post("/summarize/url")
async def summarize_url(request: SummarizeURLRequest, db: Session = Depends(get_db)):
    result = await summarization_service.summarize_url(str(request.url))
    new_summary = Summary(
        id=str(uuid.uuid4()),
        user_id=request.user_id,
        source_type="url",
        source_url=str(request.url),
        original_text=result["bart"]["summary"],  # store summary, not full article
        original_length=result["original_length"],
        bart_summary=result["bart"]["summary"],
        pegasus_summary=result["pegasus"]["summary"]
    )
    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)
    result["summary_id"] = new_summary.id
    return result


# --- File summarization ---
@router.post("/summarize/file")
async def summarize_file(
    file: UploadFile = File(...),
    user_id: str | None = None,
    db: Session = Depends(get_db)
):
    allowed_types = [
        "text/plain",
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    file_bytes = await file.read()
    result = await summarization_service.summarize_file(file_bytes, file.content_type)

    new_summary = Summary(
        id=str(uuid.uuid4()),
        user_id=user_id,
        source_type="file",
        original_text=f"File: {file.filename}",
        original_length=result["original_length"],
        bart_summary=result["bart"]["summary"],
        pegasus_summary=result["pegasus"]["summary"]
    )
    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)

    result["summary_id"] = new_summary.id
    result["filename"] = file.filename
    return result
