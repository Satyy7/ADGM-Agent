
import re
from src.utils import gemini_generate


_CANONICAL_MAP = {
    "shareholder resolution": "Shareholder Resolution",
    "shareholders' resolution": "Shareholder Resolution",
    "resolution of incorporating shareholders": "Shareholder Resolution",
    "articles of association": "Articles of Association",
    "memorandum of association": "Memorandum of Association",
    "board resolution": "Board Resolution",
    "ubo declaration": "UBO Declaration Form",
    "register of members": "Register of Members and Directors",
    "incorporation application": "Incorporation Application Form",
    "employment contract": "Employment Contract",
    "offer letter": "Offer Letter",
    "termination": "Termination Letter",
    "nda": "Non-Disclosure Agreement",
    "service agreement": "Service Agreement",
    "anti-money laundering": "Anti-Money Laundering Policy",
    "data protection": "Data Protection Policy",
    "lease agreement": "Lease Agreement"
}

def _normalize_label(s: str):
    if not s:
        return None
    s = s.lower()
    s = re.sub(r'[^a-z0-9\s\']', ' ', s)
    for key, canon in _CANONICAL_MAP.items():
        if key in s:
            return canon
    
    for key, canon in _CANONICAL_MAP.items():
        key_words = key.split()
        if all(k in s for k in key_words[:2]):  # require first 2 words
            return canon
    return None

def classify_document(text: str) -> str:
    head = text.strip().splitlines()
    
    for i in range(min(6, len(head))):
        candidate = head[i].strip()
        norm = _normalize_label(candidate)
        if norm:
            return norm
    
    norm = _normalize_label(text)
    if norm:
        return norm
    
    prompt = (
        "Identify the ADGM document type in one short label (e.g. 'Shareholder Resolution', "
        "'Articles of Association', 'Employment Contract') based on this text:\n\n"
        f"{text[:3000]}"
    )
    try:
        resp = gemini_generate(prompt)
        resp_label = resp.strip().splitlines()[0]
        norm = _normalize_label(resp_label)
        if norm:
            return norm
        
        return resp_label.strip()
    except Exception:
        return "Unknown"
