from app.ml.bart_model import get_bart_model
from app.ml.pegasus_model import get_pegasus_model
import asyncio
from app.services.extraction import TextExtractor

class SummarizationService:
    def __init__(self):
        self.bart = get_bart_model()
        self.pegasus = get_pegasus_model()
        self.extractor = TextExtractor()  # ✅ add this

    async def summarize_text(self, text: str):
        bart_task = asyncio.to_thread(self.bart.summarize, text)
        pegasus_task = asyncio.to_thread(self.pegasus.summarize, text)
        bart_result, pegasus_result = await asyncio.gather(bart_task, pegasus_task)
        return {
            "original_length": len(text.split()),
            "bart": bart_result,
            "pegasus": pegasus_result
        }

    async def summarize_url(self, url: str):
        extracted = await self.extractor.extract_from_url(url)
        return await self.summarize_text(extracted["text"])

    async def summarize_file(self, file_bytes: bytes, file_type: str):
        if file_type == "application/pdf":
            extracted = await self.extractor.extract_from_pdf(file_bytes)
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            extracted = await self.extractor.extract_from_docx(file_bytes)
        else:
            extracted = {"text": file_bytes.decode("utf-8")}
        return await self.summarize_text(extracted["text"])

summarization_service = SummarizationService()
