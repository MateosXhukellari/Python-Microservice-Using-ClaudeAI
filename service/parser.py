import pdfplumber
import httpx
from docx import Document
from io import BytesIO

def parse_pdf(file_bytes: bytes) -> str:
    text = ""
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def parse_docx(file_bytes: bytes) -> str:
    doc = Document(BytesIO(file_bytes))
    text = ""
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text + "\n"
    return text


def parse_text(file_bytes: bytes) -> str:
    return file_bytes.decode("utf-8", errors="ignore")

async def download_and_parse(file_url: str, file_type: str) -> tuple[str, int]:
    async with httpx.AsyncClient() as client:
        response = await client.get(file_url)
        file_bytes = response.content

    if "pdf" in file_type.lower():
        text = parse_pdf(file_bytes)
        page_count = len(pdfplumber.open(BytesIO(file_bytes)).pages)
    elif "docx" in file_type.lower() or "wordprocessing" in file_type.lower():
        text = parse_docx(file_bytes)
        page_count + len(text.split("\n"))
    else:
        text = parse_text(file_bytes)
        page_count = 1
    
    return text, page_count