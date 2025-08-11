# ADGM Corporate Agent -- AI Compliance Review System

## Overview

The **ADGM Corporate Agent** is an AI-powered compliance review system
designed to analyze ADGM (Abu Dhabi Global Market) legal documents.\
It performs **document classification**, **regulatory compliance
verification**, **red flag detection**, and **inline commenting**
directly in `.docx` files based on **official ADGM references**.

The system uses **Google Gemini** for natural language processing,
**ChromaDB** for reference document retrieval, and a **FastAPI backend
with a Streamlit frontend** to deliver a complete end-to-end review
experience.

------------------------------------------------------------------------

## Key Features

-   **Automatic Document Classification**\
    Identifies uploaded ADGM legal documents (e.g., Shareholder
    Resolution, Articles of Association).

-   **Compliance Verification**\
    Checks if all required documents are submitted for a given ADGM
    process (e.g., Company Incorporation).

-   **Reference-Based Red Flag Detection**\
    Compares uploaded documents against official ADGM reference
    templates.

-   **Inline Commenting in DOCX**\
    Highlights problematic text in `.docx` files and adds comments with
    citations.

-   **Interactive Web Interface**\
    Streamlit frontend for document upload, compliance status, and
    download of reviewed documents.

-   **JSON Report Generation**\
    Generates a downloadable JSON compliance report.

------------------------------------------------------------------------

## Project Structure
    app.py                  # Streamlit frontend
    main.py                 # FastAPI backend
    src/
    │
    ├── classifier.py           # Classifies document type
    ├── compliance_checker.py   # Checks for missing clauses
    ├── doc_requirements.py     # Required clauses mapping
    ├── missing_doc_requirements.py # Required docs per process
    ├── red_flag_detector.py    # Detects red flags and adds inline comments
    ├── retriever.py            # Retrieves reference documents
    ├── utils.py                # Embeddings, Gemini API, and ChromaDB setup
    ├── parser.py               # Extracts text from DOCX
    ├── data_ingest.py          # Loads reference documents into ChromaDB
    ├── reference_matcher.py    # Matches uploaded docs to references
    └── process_requirements.py # Process-specific document requirements

------------------------------------------------------------------------

## Installation & Setup

### 1️⃣ Prerequisites

-   Python 3.10+
-   Google Gemini API Key (store in `.env` as `GEMINI_API_KEY`)
-   ChromaDB persistent storage directory (`data_sources/chroma_store`)

### 2️⃣ Clone the Repository

``` bash
git clone https://github.com/Satyy7/ADGM-Agent.git
cd ADGM Agent Submission
```

### 3️⃣ Create Virtual Environment

``` bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 4️⃣ Install Dependencies

``` bash
pip install -r requirements.txt
```

### 5️⃣ Environment Variables

Create a `.env` file in the project root:

``` env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 6️⃣ Ingest Reference Documents

Before running the server, ingest official ADGM reference documents into
ChromaDB:

``` bash
python src/data_ingest.py
```

### 7️⃣ Run the FastAPI Backend (Uvicorn)

``` bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### 8️⃣ Run the Streamlit Frontend

``` bash
streamlit run src/app.py
```

------------------------------------------------------------------------

## API Endpoint

**POST** `/review`\
Uploads `.docx` files for analysis.

**Example using `curl`**:

``` bash
curl -X POST "http://127.0.0.1:8000/review"   -F "files=@/path/to/document.docx"
```

------------------------------------------------------------------------

## Flow Diagram (Insert Below)

![alt text](Flowchat(RAG).drawio-2.png)
------------------------------------------------------------------------

## Output Files

-   **reviewed\_\<filename\>.docx** → Original file with inline comments
    and highlights.
-   **report_timestamp.json** → Detailed compliance report.

------------------------------------------------------------------------

## Example Use Cases

-   **Law firms** verifying client documents for ADGM incorporation.
-   **Corporate compliance teams** ensuring all regulatory clauses are
    met.
-   **Regulators** reviewing submissions efficiently.

------------------------------------------------------------------------


