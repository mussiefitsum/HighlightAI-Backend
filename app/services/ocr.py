# app/services/ocr.py
import io
from pdf2image import convert_from_path
import pytesseract

def ocr_pdf_to_pages(pdf_path: str):
    images = convert_from_path(pdf_path)
    out = []
    for i, img in enumerate(images):
        text = pytesseract.image_to_string(img) or ""
        out.append({"page_num": i, "text": text, "blocks": []})
    return out
