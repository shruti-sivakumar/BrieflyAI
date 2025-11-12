from app.ml.bart_model import get_bart_model
from app.ml.pegasus_model import get_pegasus_model
import asyncio

class SummarizationService:
    def __init__(self):
        self.bart = get_bart_model()
        self.pegasus = get_pegasus_model()

    async def summarize_text(self, text: str):
        bart_task = asyncio.to_thread(self.bart.summarize, text)
        pegasus_task = asyncio.to_thread(self.pegasus.summarize, text)
        bart_result, pegasus_result = await asyncio.gather(bart_task, pegasus_task)
        return {
            "original_length": len(text.split()),
            "bart": bart_result,
            "pegasus": pegasus_result
        }

summarization_service = SummarizationService()
