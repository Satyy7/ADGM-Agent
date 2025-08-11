import re
import requests
from pathlib import Path
import docx2txt
import pdfplumber
from tqdm import tqdm
from src.utils import embed_texts, chroma_client

DATA_SRC_DOCX = Path("Data Sources.docx")
DOWNLOAD_DIR = Path("data_sources")
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

def extract_links_from_docx(docx_path):
    text = docx2txt.process(str(docx_path))
    return list(dict.fromkeys(re.findall(r'(https?://[^\s)]+)', text)))

def download_file(url):
    local_path = DOWNLOAD_DIR / Path(url.split("?")[0]).name
    if local_path.exists():
        return local_path
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        with open(local_path, "wb") as f:
            f.write(r.content)
        return local_path
    except Exception as e:
        print(f"Download failed for {url}: {e}")
        return None

def extract_text(path):
    if path.suffix.lower() == ".docx":
        return docx2txt.process(str(path))
    elif path.suffix.lower() == ".pdf":
        text = ""
        with pdfplumber.open(str(path)) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    return ""

def chunk_text(text, size=800, overlap=100):
    words = text.split()
    return [
        " ".join(words[i:i + size])
        for i in range(0, len(words), size - overlap)
    ]

def ingest():
    links = extract_links_from_docx(DATA_SRC_DOCX)
    print(f"Found {len(links)} links in {DATA_SRC_DOCX.name}")
    all_chunks = []
    for url in tqdm(links, desc="Processing links"):
        file_path = download_file(url)
        if not file_path:
            continue
        text = extract_text(file_path)
        if not text:
            continue
        for i, chunk in enumerate(chunk_text(text)):
            all_chunks.append({
                "id": f"{file_path.stem}_{i}",
                "text": chunk,
                "meta": {"source": file_path.name, "url": url}
            })
    if not all_chunks:
        print("No content to index.")
        return

    try:
        col = chroma_client.get_collection("adgm_docs")
    except Exception:
        col = chroma_client.create_collection("adgm_docs")

    col.add(
        ids=[c["id"] for c in all_chunks],
        embeddings=embed_texts([c["text"] for c in all_chunks]),
        metadatas=[c["meta"] for c in all_chunks],
        documents=[c["text"] for c in all_chunks]
    )
    print(f"Ingestion complete. {len(all_chunks)} chunks added to Chroma.")


if __name__ == "__main__":
    ingest()
