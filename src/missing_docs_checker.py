REQUIRED_DOCS = {
    "Company Incorporation": [
        "Articles of Association",
        "Memorandum of Association",
        "Board Resolution",
        "Shareholder Resolution",
        "Incorporation Application Form",
        "UBO Declaration Form",
        "Register of Members and Directors",
        "Change of Registered Address Notice"
    ],
    "Licensing": [
        "License Application Form",
        "Business Plan",
        "Proof of Registered Address",
        "Regulatory Compliance Questionnaire"
    ],
    "Regulatory Filings": [
        "Annual Return",
        "Financial Statements",
        "Directors Report",
        "Auditors Report",
        "UBO Declaration Form"
    ],
    "Employment / HR": [
        "Employment Contract",
        "Employee Handbook",
        "Board Resolution (HR)",
        "HR Policy Manual"
    ],
    "Commercial Agreements": [
        "Sales Agreement",
        "Service Agreement",
        "Non-Disclosure Agreement",
        "Joint Venture Agreement"
    ],
    "Compliance / Risk Policies": [
        "Anti-Money Laundering Policy",
        "Risk Management Policy",
        "Data Protection Policy",
        "Health and Safety Policy"
    ]
}

def check_missing_documents(uploaded_doc_types: list):
    best_proc = "Unknown"
    max_matches = 0
    
    for proc, docs in REQUIRED_DOCS.items():
        matches = sum(1 for doc_type in uploaded_doc_types if doc_type in docs)
        if matches > max_matches:
            max_matches = matches
            best_proc = proc

    if best_proc == "Unknown":
        return {"process": "Unknown", "required_count": 0, "missing_docs": []}

    required = REQUIRED_DOCS[best_proc]
    missing = [doc for doc in required if doc not in uploaded_doc_types]

    return {
        "process": best_proc,
        "required_count": len(required),
        "missing_docs": missing
    }