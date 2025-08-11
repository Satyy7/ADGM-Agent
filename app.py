import streamlit as st
import requests
import json
import os
import time

API_URL = "http://127.0.0.1:8000/review"

st.set_page_config(page_title="ADGM Corporate Agent", layout="wide")

st.title("ADGM Corporate Agent: AI Compliance Review")
st.caption("Upload one or more .docx documents for a compliance check against ADGM regulations.")

uploaded_files = st.file_uploader(
    "Drag and drop your ADGM legal documents here (.docx only)",
    type=["docx"],
    accept_multiple_files=True
)

if 'report_data' not in st.session_state:
    st.session_state.report_data = None

if uploaded_files:
    if st.button("Start Full Review", type="primary"):
        with st.spinner("The AI agent is analyzing your documents... This may take a moment."):
            files_for_api = [
                ("files", (f.name, f.getvalue(), "application/vnd.openxmlformats-officedocument.wordprocessingml.document"))
                for f in uploaded_files
            ]

            try:
                resp = requests.post(API_URL, files=files_for_api, timeout=300)
                st.session_state.report_data = resp.json()
            except requests.exceptions.ConnectionError:
                st.error("Connection Failed: Cannot connect to the backend API. Ensure the FastAPI server is running.", icon="🚨")
                st.session_state.report_data = None
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}", icon="🔥")
                st.session_state.report_data = None


if st.session_state.report_data:
    data = st.session_state.report_data
    
    st.success("Review Complete!")
    st.markdown("---")

    

    st.subheader("Checklist Verification")

    process = data.get('process', 'Unknown')
    if process != "Unknown" and process == "Company Incorporation":
        uploaded_count = data.get('documents_uploaded', 0)
        required_count = data.get('required_documents', 0)
        missing_docs = data.get('missing_documents', [])

        
        st.info(
            f"It appears that you’re trying to incorporate a company in ADGM. "
            f"Based on our reference list, you have uploaded {uploaded_count} out of {required_count} required documents."
        )

        if len(missing_docs) == 1:
           
            st.error(f"The missing document appears to be: **‘{missing_docs[0]}’**")
        elif len(missing_docs) > 1:
            st.error("The missing documents appear to be:")
            for doc in missing_docs:
                st.write(f"- **{doc}**")
        else:
            st.success("You have uploaded all the required documents for Company Incorporation.")

    elif process != "Unknown":
         st.success(f"Process detected: **{process}**. No missing document check is required for this process type.")
    
    else:
        st.warning("Could not automatically determine the legal process based on the uploaded documents.")

    
    
    st.markdown("---")
    st.subheader("Downloads and Detailed Analysis")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.write("**Downloadable Files**")
        json_bytes = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
        st.download_button(
            "Download Full JSON Report",
            data=json_bytes,
            file_name=f"adgm_report_{int(time.time())}.json",
            mime="application/json"
        )
        
        reviewed_docs = data.get("reviewed_documents", {})
        if reviewed_docs:
            for filename, filepath in reviewed_docs.items():
                if os.path.exists(filepath):
                    with open(filepath, "rb") as f:
                        st.download_button(
                            f"Download reviewed_{filename}",
                            data=f.read(),
                            file_name=f"reviewed_{filename}",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )

    with col2:
        st.write("**Issue Breakdown by Document**")
        all_issues = data.get("issues_found", [])
        if not all_issues:
            st.info("No specific issues were flagged in the uploaded documents.")
        else:
            for issue in all_issues:
                doc_name = issue.get("document", "Unknown Document")
                with st.expander(f"Issue in **{doc_name}**"):
                    severity = issue.get("severity", "Unknown")
                    color = {"High": "red", "Medium": "orange", "Low": "blue"}.get(severity, "grey")
                    section = issue.get('section', 'N/A')
                    citation = issue.get('citation', 'N/A')
                    
                    st.markdown(f"**<span style='color:{color};'>[{severity.upper()}]</span> in Section: *{section}***", unsafe_allow_html=True)
                    st.markdown(f"**Issue:** {issue.get('issue', 'No description')}")
                    st.markdown(f"**Legal Basis:** {citation}")
                    st.markdown(f"**Suggestion:** {issue.get('suggestion', 'No suggestion')}")