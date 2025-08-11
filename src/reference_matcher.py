from src.utils import chroma_client, embed_texts

def match_reference(text, top_k=1):
    try:
        col = chroma_client.get_collection("adgm_docs")
    except Exception:
        return None, None

    emb = embed_texts([text])
    res = col.query(query_embeddings=emb, n_results=top_k)
    if not res or not res.get("documents") or not res["documents"][0]:
        return None, None

    doc_text = res["documents"][0][0]
    meta = res["metadatas"][0][0] if res.get("metadatas") and res["metadatas"][0] else {}
    return doc_text, meta
