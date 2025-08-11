import os
from dotenv import load_dotenv
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from pathlib import Path

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

CHROMA_PERSIST_DIR = Path("data_sources/chroma_store")
CHROMA_PERSIST_DIR.mkdir(parents=True, exist_ok=True)
chroma_client = chromadb.PersistentClient(path=str(CHROMA_PERSIST_DIR))

def embed_texts(texts):
    
    return EMBED_MODEL.encode(texts, show_progress_bar=False).tolist()

def gemini_generate(prompt, model="gemini-2.5-pro", temperature=0.6):
    
    response = genai.GenerativeModel(model).generate_content(prompt)
    return response.text
