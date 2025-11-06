from typing import Dict, List
import re

def _phrase_hits_in_text(text: str, phrase: str) -> bool:
    return phrase.lower() in (text or "").lower()

def spans_to_rects(pages: List[dict], scored_phrases: Dict[str, float], per_page_cap: int = 12):
    """
    For each phrase found on a page, highlight the enclosing text block.
    It's fast and robust. We can refine to exact spans later using search_for().
    Returns: list of {page, rect: (x0,y0,x1,y1), phrase}
    """
    results: List[dict] = []
    phrases_sorted = [k for k,_ in sorted(scored_phrases.items(), key=lambda kv: kv[1], reverse=True)]

    for page in pages:
        used = 0
        page_text = page.get("text", "") or ""
        if not page_text.strip():
            continue

        # Only consider phrases that actually occur in this page's text
        local_phrases = [ph for ph in phrases_sorted if _phrase_hits_in_text(page_text, ph)]
        for ph in local_phrases:
            if used >= per_page_cap:
                break
            # find a block containing the phrase
            lower = ph.lower()
            for block in page.get("blocks", []):
                if lower in (block.get("text","") or "").lower():
                    x0,y0,x1,y1 = block["bbox"]
                    results.append({"page": page["page_num"], "rect": (x0,y0,x1,y1), "phrase": ph})
                    used += 1
                    break
    return results