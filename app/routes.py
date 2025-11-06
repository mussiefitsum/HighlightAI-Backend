from flask import Blueprint, request, jsonify
from .services.storage import allowed, ensure_dirs, save_upload
from .services.extract import extract_pages
from .services.ocr import ocr_pdf_to_pages
from .services import nlp
from .services import highlight as hi

api = Blueprint("api", __name__)

@api.get("/health")
def health():
    return {"ok": True, "service": "HighlightAI", "version": "0.4.0"}

@api.post("/upload")
def upload():
    ensure_dirs()
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file provided. Use form field 'file'."}), 400
    if not allowed(file.filename):
        return jsonify({"error": "Only .pdf files are allowed."}), 400

    name, path = save_upload(file)

    # 1) extract text/blocks
    pages = extract_pages(path)
    if all((not (p["text"] or "").strip()) for p in pages):
        pages = ocr_pdf_to_pages(path)

    # 2) score phrases
    scores = nlp.score_keyphrases(pages)  # dict {phrase: score}

    # 3) map to rectangles
    rects = hi.spans_to_rects(pages, scores, per_page_cap=10)

    # build safe/light response
    preview = []
    for p in pages:
        t = (p["text"] or "").strip()
        preview.append({
            "page_num": p["page_num"],
            "chars": len(t),
            "preview": t[:250]
        })

    return jsonify({
        "message": "Upload OK",
        "filename": name,
        "stored_path": path,
        "pages": len(pages),
        "top_phrases": sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:20],
        "text_preview": preview,
        "highlights": [
            {"page": r["page"], "rect": r["rect"], "phrase": r["phrase"]}
            for r in rects
        ]
    }), 201