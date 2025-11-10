import os
import re
import pdfplumber
from docx import Document
from app.services.ocr import extract_text_from_image
import tempfile

async def parse_file(filename: str, content: bytes) -> str:
    suffix = filename.lower().split(".")[-1]

    if suffix == "pdf":
        return _parse_pdf(content)
    elif suffix == "docx":
        return _parse_docx(content)
    elif suffix in ["png", "jpg", "jpeg"]:
        return extract_text_from_image(content)
    else:
        raise ValueError("Format de fichier non supporté.")

def _parse_pdf(content: bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(content)
        tmp.close()
        with pdfplumber.open(tmp.name) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)

    os.remove(tmp.name)

    if not text.strip():
        text = extract_text_from_image(content)

    return text

def _parse_docx(content: bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx", mode="wb") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    doc = Document(tmp_path)
    text = "\n".join(paragraph.text for paragraph in doc.paragraphs)

    try:
        os.remove(tmp_path)
    except Exception:
        pass
    
    return text

def extract_periods(text: str):
    pattern = re.compile(
        r"(?:\d{4}|\w+\.?\s?\d{4})\s?[-–à]\s?(?:\d{4}|présent|aujourd'hui|en cours)",
        re.IGNORECASE
    )
    found = pattern.findall(text)
    return list(set(found))