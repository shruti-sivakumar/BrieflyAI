from app.ml.bart_model import get_bart_model
from app.ml.pegasus_model import get_pegasus_model
import asyncio
from app.services.extraction import TextExtractor
from app.utils.cache import get_cache
import hashlib

class SummarizationService:
    def __init__(self):
        self.bart = get_bart_model()
        self.pegasus = get_pegasus_model()
        self.extractor = TextExtractor()
        self.cache = get_cache()

    def _hash_text(self, text: str) -> str:
        return hashlib.sha256(text.encode()).hexdigest()

    async def _run_model(self, model, text: str):
        """Runs a HF summarize() inside a safe background thread."""
        return await asyncio.to_thread(model.summarize, text)

    # -----------------------------
    # TEXT SUMMARIZATION
    # -----------------------------
    async def summarize_text(self, text: str):
        content_hash = self._hash_text(text)
        cache_key = f"summary:cache:{content_hash}"

        cached = await self.cache.get(cache_key)
        if cached:
            print("Cache hit!")
            return cached

        # ❗ FIXED: RUN MODELS SEQUENTIALLY, NOT IN PARALLEL
        bart_result = await self._run_model(self.bart, text)
        pegasus_result = await self._run_model(self.pegasus, text)

        result = {
            "original_length": len(text.split()),
            "bart": bart_result,
            "pegasus": pegasus_result
        }

        await self.cache.set(cache_key, result, expire=86400)
        print("Cache stored.")
        return result

    # -----------------------------
    # URL SUMMARIZATION
    # -----------------------------
    async def summarize_url(self, url: str):
        extracted = await self.extractor.extract_from_url(url)
        text = extracted.get("text", "")

        if not text or len(text.split()) < 50:
            raise ValueError("Could not extract enough text from URL.")

        result = await self.summarize_text(text)
        result["extracted_title"] = extracted.get("title")
        result["original_length"] = extracted.get("word_count", len(text.split()))
        return result

    # -----------------------------
    # FILE SUMMARIZATION
    # -----------------------------
    async def summarize_file(self, file_bytes: bytes, mime: str):
        if mime == "text/plain":
            text = file_bytes.decode("utf-8", errors="ignore")

        elif mime == "application/pdf":
            extracted = await self.extractor.extract_from_pdf(file_bytes)
            text = extracted["text"]

        elif mime == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            extracted = await self.extractor.extract_from_docx(file_bytes)
            text = extracted["text"]

        else:
            raise ValueError(f"Unsupported file type: {mime}")

        if not text.strip():
            raise ValueError("Could not extract text from file")

        if len(text.split()) < 20:
            raise ValueError("File does not contain enough text to summarize")

        result = await self.summarize_text(text)
        result["original_length"] = len(text.split())
        return result


summarization_service = SummarizationService()