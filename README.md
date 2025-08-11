# ADGM Corporate Agent -- AI Compliance Review System
📽 **Demo Video:** [Watch Here](https://drive.google.com/file/d/1ANWuYHTdw4anvLKB5ovKtA5qTJ7cYDTf/view?usp=sharing)
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

## Retrieval-Augmented Generation (RAG) in This Project

This system uses **Retrieval-Augmented Generation (RAG)** to ensure all AI-driven compliance checks are grounded in **official ADGM reference documents** rather than relying solely on the model’s internal knowledge. This greatly increases accuracy, transparency, and explainability.

### How RAG Works Here
1. **Document Ingestion**  
   All official ADGM legal templates, regulations, and process guidelines are stored in a **ChromaDB** vector database. These references are converted into embeddings using the Google Gemini embedding API.

2. **Retrieval Phase**  
   When a user uploads a `.docx` document, the system:
   - Extracts the text.
   - Converts it into embeddings.
   - Retrieves the most semantically similar clauses, sections, or templates from the ChromaDB reference store.

3. **Generation Phase**  
   The retrieved reference materials are combined with the uploaded document’s text and sent to **Google Gemini**. This augmented context allows the model to:
   - Classify the document type.
   - Verify compliance with ADGM regulations.
   - Detect red flags.
   - Suggest clause modifications based on the most relevant legal references.

4. **Inline Commenting & Reporting**  
   The model’s findings are added directly as **inline comments in the DOCX file**, each comment citing the specific ADGM reference that triggered it. A downloadable JSON compliance report is also generated.

### Why RAG?
- **Improved Accuracy**: Ensures recommendations are based on the latest ADGM legal content.
- **Explainability**: All AI outputs are backed by direct references.
- **Adaptability**: Updating the ChromaDB store with new regulations instantly updates the system without retraining the model.

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
