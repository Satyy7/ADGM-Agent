from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pathlib import Path
import tempfile
import json
import time
import shutil

from src.parser import parse_document
from src.classifier import classify_document
from src.retriever import retrieve_reference
from src.missing_docs_checker import check_missing_documents
from src.red_flag_detector import detect_red_flags, add_comments_to_docx  

app = FastAPI(title="ADGM Corporate Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)
TEMP_DIR = Path(tempfile.gettempdir())

@app.post("/review")
async def review_documents(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")

    all_issues_found = []
    detected_doc_types = []
    output_file_paths = {}

    for file in files:
        if not file.filename.lower().endswith(".docx"):
            continue

        tmp_path = TEMP_DIR / f"{int(time.time())}_{file.filename}"
        with open(tmp_path, "wb") as f:
            f.write(await file.read())

        
        text = parse_document(tmp_path)

      
        doc_type = classify_document(text)
        detected_doc_types.append(doc_type)

       
        ref_text, meta = retrieve_reference(text, doc_type=doc_type)

       
        issues = detect_red_flags(text, ref_text)

        
        commented_docx_path = OUTPUT_DIR / f"reviewed_{file.filename}"
        try:
            add_comments_to_docx(tmp_path, issues, commented_docx_path, debug=True)
        except Exception as e:
            print(f"[main.py] Failed to add comments to {file.filename}: {e}")
            shutil.copy(tmp_path, commented_docx_path)

        output_file_paths[file.filename] = str(commented_docx_path)

        
        for issue in issues:
            issue["document"] = file.filename
            all_issues_found.append(issue)

   
    missing_docs_report = check_missing_documents(detected_doc_types)

    
    result = {
        "process": missing_docs_report["process"],
        "documents_uploaded": len(detected_doc_types),
        "required_documents": missing_docs_report["required_count"],
        "missing_documents": missing_docs_report["missing_docs"],
        "issues_found": all_issues_found,
        "reviewed_documents": output_file_paths,
    }

    json_path = OUTPUT_DIR / f"report_{int(time.time())}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return JSONResponse(content=result)
