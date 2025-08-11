
from src.doc_requirements import DOC_REQUIREMENTS

def _infer_doc_type(text_lower: str):
    best = None
    best_score = 0
    for doc_type, fields in DOC_REQUIREMENTS.items():
        score = sum(1 for f in fields if f.lower() in text_lower)
        if score > best_score:
            best_score = score
            best = doc_type
    
    return best if best_score > 0 else None

def check_compliance(uploaded_text: str, reference_text: str = None, doc_type: str = None):
    text_lower = uploaded_text.lower()
    if not doc_type:
        doc_type = _infer_doc_type(text_lower)
    required = DOC_REQUIREMENTS.get(doc_type, []) if doc_type else []

    if not required:
        return {
            "doc_type": doc_type or "Unknown",
            "score": 0,
            "missing": ["Unknown document type"],
            "recommendations": ["Update DOC_REQUIREMENTS mapping or provide doc_type"]
        }

    missing = []
    recs = []
    penalty = max(1, 100 // len(required))
    score = 100

    for field in required:
        if field.lower() not in text_lower:
            missing.append(field)
            recs.append(f"Add {field}")
            score -= penalty

    
    if "[" in uploaded_text or "{insert" in uploaded_text.lower():
        if "Placeholders not filled" not in missing:
            missing.append("Placeholders not filled")
            recs.append("Fill all placeholders before submission")
            score -= 5

    if score < 0:
        score = 0

    return {
        "doc_type": doc_type,
        "score": score,
        "missing": missing,
        "recommendations": recs
    }
