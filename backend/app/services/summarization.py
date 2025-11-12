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

    async def summarize_text(self, text: str):
        content_hash = self._hash_text(text)
        cache_key = f"summary:cache:{content_hash}"

        # Check cache first
        cached = await self.cache.get(cache_key)
        if cached:
            print("Cache hit!")
            return cached

        # Run both models asynchronously
        bart_task = asyncio.to_thread(self.bart.summarize, text)
        pegasus_task = asyncio.to_thread(self.pegasus.summarize, text)
        bart_result, pegasus_result = await asyncio.gather(bart_task, pegasus_task)

        result = {
            "original_length": len(text.split()),
            "bart": bart_result,
            "pegasus": pegasus_result
        }

        # Store in cache (24h)
        await self.cache.set(cache_key, result, expire=86400)
        print("Cache stored.")
        return result

summarization_service = SummarizationService()
