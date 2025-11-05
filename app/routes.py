from flask import Blueprint, request, jsonify
from .services.storage import allowed, ensure_dirs, save_upload
from .services.extract import extract_pages
from .services.ocr import ocr_pdf_to_pages

api = Blueprint("api", __name__)

@api.get("/health")
def health():
    return {"ok": True, "service": "HighlightAI", "version": "0.3.0"}

@api.post("/upload")
def upload():
    ensure_dirs()

    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file provided. Use form field 'file'."}), 400
    if not allowed(file.filename):
        return jsonify({"error": "Only .pdf files are allowed."}), 400

    name, path = save_upload(file)

    pages = extract_pages(path)

    if all((not p["text"].strip()) for p in pages):
        pages = ocr_pdf_to_pages(path)

    preview = []
    for p in pages:
        t = p["text"].strip()
        preview.append({
            "page_num": p["page_num"],
            "chars": len(t),
            "preview": t[:300]
        })

    return jsonify({
        "message": "Upload OK",
        "filename": name,
        "stored_path": path,
        "pages": len(pages),
        "text_preview": preview
    }), 201