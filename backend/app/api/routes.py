from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Query
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

    # --- Extract text based on file type ---
    if file.content_type == "text/plain":
        extracted_text = file_bytes.decode("utf-8", errors="ignore")

    elif file.content_type == "application/pdf":
        extracted = await summarization_service.extractor.extract_from_pdf(file_bytes)
        extracted_text = extracted["text"]

    elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        extracted = await summarization_service.extractor.extract_from_docx(file_bytes)
        extracted_text = extracted["text"]

    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract readable text from file")

    # --- Summarize extracted text ---
    result = await summarization_service.summarize_text(extracted_text)

    # --- Save to database (store ORIGINAL EXTRACTED TEXT) ---
    new_summary = Summary(
        id=str(uuid.uuid4()),
        user_id=user_id,
        source_type="file",
        source_url=None,
        original_text=extracted_text[:5000],   # store first 5k chars to avoid DB overload
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

@router.get("/summaries/{user_id}")
async def get_user_summaries(
    user_id: str,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Fetch all summaries for a given user"""
    summaries = (
        db.query(Summary)
        .filter(Summary.user_id == user_id)
        .order_by(Summary.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "user_id": user_id,
        "count": len(summaries),
        "summaries": [
            {
                "id": s.id,
                "source_type": s.source_type,
                "source_url": s.source_url,
                "bart_summary": s.bart_summary,
                "pegasus_summary": s.pegasus_summary,
                "selected_summary": s.selected_summary,
                "user_rating": s.user_rating,
                "feedback_text": s.feedback_text,
                "created_at": s.created_at.isoformat() if s.created_at else None,
            }
            for s in summaries
        ],
    }

@router.post("/summaries/{summary_id}/feedback")
async def submit_feedback(
    summary_id: str,
    selected_model: str = Query(..., regex="^(bart|pegasus)$"),
    rating: int | None = Query(None, ge=1, le=5),
    feedback_text: str | None = None,
    db: Session = Depends(get_db)
):
    """Save user feedback and model preference"""
    summary = db.query(Summary).filter(Summary.id == summary_id).first()
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    summary.selected_summary = selected_model
    summary.user_rating = rating
    summary.feedback_text = feedback_text
    db.commit()

    return {"message": "Feedback saved successfully"}
