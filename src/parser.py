from pathlib import Path
import docx2txt
import pdfplumber

def parse_document(file_path: Path) -> str:
    ext = file_path.suffix.lower()
    if ext == ".docx":
        return docx2txt.process(str(file_path))
    elif ext == ".pdf":
        text = ""
        with pdfplumber.open(str(file_path)) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    else:
        raise ValueError(f"Unsupported file format: {ext}")
