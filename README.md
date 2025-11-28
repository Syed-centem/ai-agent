# 🧠 Enterprise Knowledge Base AI Agent

## Overview
This AI Agent is designed to streamline information retrieval within organizations. It allows employees to upload internal documents (PDFs such as HR policies, Technical Manuals, or Operation Guidelines) and ask natural language questions. The agent retrieves exact answers from the document, reducing the time spent searching through files.

## Features
* **Instant Document Ingestion:** Supports PDF upload and processing.
* **Semantic Search:** Uses vector embeddings to understand the *meaning* of the query, not just keyword matching.
* **Accurate Answers:** Utilizes GPT-3.5-turbo to synthesize answers based strictly on the provided document.
* **Secure:** Processes documents in-memory/temporarily.

## [cite_start]Tech Stack 
* **Language:** Python
* **LLM:** OpenAI GPT-3.5 Turbo
* **Framework:** LangChain
* **Vector Database:** FAISS (Facebook AI Similarity Search)
* **Interface:** Streamlit

## Setup Instructions
1.  Clone the repository:
    ```bash
    git clone [YOUR_REPO_LINK_HERE]
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the application:
    ```bash
    streamlit run app.py
    ```

## Future Improvements
* Add support for Word docs and Excel sheets.
* Implement persistent database storage (ChromaDB) to save indices.
* Add "Chat History" to allow follow-up questions.
