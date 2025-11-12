from newspaper import Article
from bs4 import BeautifulSoup
import aiohttp
import PyPDF2
import docx
import io
from typing import Dict

class TextExtractor:
    async def extract_from_url(self, url: str) -> Dict:
        """Extract article text from a URL using newspaper3k (with fallback)"""
        try:
            article = Article(url)
            article.download()
            article.parse()
            return {
                "text": article.text,
                "title": article.title,
                "authors": article.authors,
                "publish_date": article.publish_date,
                "top_image": article.top_image,
                "word_count": len(article.text.split())
            }
        except Exception:
            # fallback with BeautifulSoup
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            for tag in soup(["script", "style"]):
                tag.extract()
            text = " ".join(soup.get_text().split())
            return {"text": text, "title": soup.title.string if soup.title else None}

    async def extract_from_pdf(self, file_bytes: bytes) -> Dict:
        """Extract text from PDF bytes"""
        pdf_file = io.BytesIO(file_bytes)
        reader = PyPDF2.PdfReader(pdf_file)
        text = "".join(page.extract_text() or "" for page in reader.pages)
        return {"text": text, "page_count": len(reader.pages), "word_count": len(text.split())}

    async def extract_from_docx(self, file_bytes: bytes) -> Dict:
        """Extract text from DOCX bytes"""
        doc_file = io.BytesIO(file_bytes)
        document = docx.Document(doc_file)
        text = "\n".join(p.text for p in document.paragraphs)
        return {"text": text, "word_count": len(text.split())}
