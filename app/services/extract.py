import fitz

def extract_pages(pdf_path: str):
    pages = []
    with fitz.open(pdf_path) as doc:
        for i, page in enumerate(doc):
            text = page.get_text("text") or ""
            blocks = []

            for b in page.get_text("blocks"):
                x0, y0, x1, y1, t, *_ = b
                blocks.append({"bbox": (float(x0), float(y0), float(x1), float(y1)), "text": t or ""})
            pages.append({"page_num": i, "text": text, "blocks": blocks})
    return pages
