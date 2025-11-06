from typing import List, Dict
import spacy
import yake
from sklearn.feature_extraction.text import TfidfVectorizer

# Load once
_nlp = spacy.load("en_core_web_sm") 
_kw = yake.KeywordExtractor(lan="en", n=1, top=20)

def _ner_weights():
    # heuristic weights; tweak later
    return {"ORG": 1.4, "PERSON": 1.2, "GPE": 1.3, "DATE": 1.1, "CARDINAL": 1.05}

def ner_phrases(text: str) -> Dict[str, float]:
    doc = _nlp(text)
    weights = _ner_weights()
    out: Dict[str, float] = {}
    for ent in doc.ents:
        k = ent.text.strip()
        if not k:
            continue
        out[k] = max(out.get(k, 0.0), 0.8 * weights.get(ent.label_, 1.0))
    return out

def yake_phrases(text: str) -> Dict[str, float]:
    # YAKE gives lower = more important, invert into [0,1]
    out: Dict[str, float] = {}
    for key, score in _kw.extract_keywords(text):
        out[key] = 1.0 / (1.0 + score)
    return out

def tfidf_phrases(page_texts: List[str]) -> Dict[str, float]:
    vec = TfidfVectorizer(ngram_range=(1,2), max_features=5000, stop_words="english")
    X = vec.fit_transform(page_texts)
    mean_scores = X.mean(axis=0).A1
    vocab = vec.get_feature_names_out()
    return {vocab[i]: float(mean_scores[i]) for i in range(len(vocab))}

def score_keyphrases(pages: List[Dict]) -> Dict[str, float]:
    """Blend YAKE + TF-IDF + NER to a single dict {phrase: score}."""
    full_text = "\n".join(p["text"] or "" for p in pages)
    if not full_text.strip():
        return {}

    yake_scores = yake_phrases(full_text)        # broad topicality
    tfidf_scores = tfidf_phrases([p["text"] or "" for p in pages])  # per-doc salience
    ner_scores = ner_phrases(full_text)          # important entities

    scores: Dict[str, float] = {}

    def add(d: Dict[str, float], w: float):
        for k, s in d.items():
            if not k or len(k) < 3:
                continue
            scores[k] = scores.get(k, 0.0) + w * float(s)

    # blend weights — tune to taste
    add(yake_scores, 0.5)
    add(tfidf_scores, 0.35)
    add(ner_scores, 0.15)

    # keep top N
    return dict(sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:80])
