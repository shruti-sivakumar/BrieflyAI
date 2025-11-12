from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch
import time

class PegasusSummarizer:
    def __init__(self):
        self.model_name = "google/pegasus-xsum"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading {self.model_name} on {self.device}")
        self.tokenizer = PegasusTokenizer.from_pretrained(self.model_name)
        self.model = PegasusForConditionalGeneration.from_pretrained(self.model_name).to(self.device)

    def summarize(self, text: str, max_length: int = 100, min_length: int = 30):
        start_time = time.time()
        tokens = self.tokenizer(text, truncation=True, padding="longest", return_tensors="pt").to(self.device)
        summary_ids = self.model.generate(**tokens, num_beams=4, max_length=max_length, min_length=min_length)
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return {
            "model": "Pegasus-XSum",
            "summary": summary,
            "processing_time": round(time.time() - start_time, 2)
        }

_pegasus_model = None
def get_pegasus_model():
    global _pegasus_model
    if _pegasus_model is None:
        _pegasus_model = PegasusSummarizer()
    return _pegasus_model