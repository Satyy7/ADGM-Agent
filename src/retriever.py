
from src.utils import chroma_client, embed_texts

def retrieve_reference(doc_text, doc_type=None, top_k=1):
    try:
        col = chroma_client.get_collection("adgm_docs")
    except Exception:
        return None, None

    emb = embed_texts([doc_text])

    if doc_type:
        try:
            res = col.query(query_embeddings=emb, n_results=top_k, where={"doc_type": doc_type})
            if res and res.get("documents") and res["documents"][0]:
                return res["documents"][0][0], res["metadatas"][0][0]
        except Exception:
            pass

    
    res = col.query(query_embeddings=emb, n_results=top_k)
    if not res or not res.get("documents") or not res["documents"][0]:
        return None, None
    return res["documents"][0][0], res["metadatas"][0][0]
