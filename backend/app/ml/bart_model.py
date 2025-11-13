from transformers import BartForConditionalGeneration, BartTokenizer
import torch
import time

class BARTSummarizer:
    def __init__(self):
        self.model_name = "facebook/bart-large-cnn"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading {self.model_name} on {self.device}")
        self.tokenizer = BartTokenizer.from_pretrained(self.model_name)
        self.model = BartForConditionalGeneration.from_pretrained(self.model_name).to(self.device)

    def summarize(self, text: str, max_length: int = 200, min_length: int = 50):
        start_time = time.time()
        inputs = self.tokenizer(text, return_tensors="pt", max_length=1024, truncation=True).to(self.device)
        summary_ids = self.model.generate(
            inputs["input_ids"],
            num_beams=4,
            length_penalty=2.0,
            max_length=max_length,
            min_length=min_length,
            early_stopping=True
        )
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return {
            "model": "BART-large-CNN",
            "summary": summary,
            "processing_time": round(time.time() - start_time, 2)
        }

_bart_model = None
def get_bart_model():
    global _bart_model
    if _bart_model is None:
        _bart_model = BARTSummarizer()
    return _bart_model