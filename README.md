# 🧠 Dual-Method Multimodal RAG Engine for PDFs

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![Framework](https://img.shields.io/badge/Framework-Streamlit-red.svg)

This project implements a **Multimodal Retrieval-Augmented Generation (RAG)** system to interactively **chat with any PDF** — whether it's text-heavy, image-rich, or both.

It combines **CLIP-based semantic embeddings** with **LLM (GPT-4o-mini)** powered summarization, enabling two powerful retrieval strategies through a unified Streamlit interface.

> 🔎 Choose between **raw CLIP semantic search** or **contextual GPT summary search** — all via a simple web UI.

---

## 🚀 Features

- ### 🧠 Dual Retrieval Modes
  - **GPT-4o Summary Search**  
    Uses GPT-4o-mini to generate semantic-rich summaries from text and image blocks. Queries are matched with these for context-aware answers.
  - **CLIP Embedding Search**  
    Uses OpenAI’s CLIP model to embed raw visual and textual content for direct semantic matching.

- ### 🖼️ Multimodal Understanding  
  Parses and processes **both text and images** for true multimodal search.

- ### 🎛️ Streamlit UI  
  Toggle between retrieval modes and interactively ask questions about any PDF.

- ### 📄 Bring Your Own PDF  
  Drop in your own PDF file and run the ingestion pipeline to get started.

- ### 🧩 Modular Architecture  
  Clean separation of frontend and backend logic for extensibility and scalability.

---

## 🧪 Jupyter/Colab Notebook Method (Quick Test via Ngrok)

You can run the entire project from **Colab or Jupyter Notebook** without setting up the full directory manually.

### Steps:

1. **Run the `.ipynb` notebook** to perform PDF ingestion and launch ngrok.
2. **Create a file named `stream.py`** with the following contents:

   ```python
   # stream.py
   import os

   # Replace with your actual ngrok URL from the last cell of the notebook
   public_url = "https://your-ngrok-link.ngrok-free.app"

   # Launch Streamlit app locally via ngrok
   os.system(f"streamlit run frontend/app.py --server.headless true --server.port 8501 --browser.serverAddress {public_url}")
3. **Paste the ngrok link shown in the last notebook cell into the `public_url` variable**.
4. **Run `stream.py`** to launch the UI locally and tunnel it via ngrok.

---

##  Workflow Diagram

This diagram illustrates the complete user workflow, from placing a PDF to querying it with either the GPT or CLIP method.

```mermaid
graph TD
    A[Start] --> B{1. Place Your PDF};
    B --> C{2. Run Ingestion Script};

    subgraph "Data Ingestion (One-Time Setup)"
        C --> D["python -m backend.ingest --method gpt"];
        D --> E[Process PDF (Text & Images)];
        E --> F[Generate Summaries with GPT-4o];
        F --> G[Generate OpenAI Embeddings];
        G --> H[(Qdrant GPT DB)];

        C --> I["python -m backend.ingest --method clip"];
        I --> J[Process PDF (Text & Images)];
        J --> K[Generate CLIP Embeddings];
        K --> L[(Qdrant CLIP DB)];
    end

    M{3. Launch Streamlit App} --> N["streamlit run frontend/app.py"];

    subgraph "Interactive Querying"
        N --> O{User Interface};
        O --> P[Enter Query];
        P --> Q{Select Method: GPT or CLIP};
        Q -- GPT --> R[Query Qdrant GPT DB];
        Q -- CLIP --> S[Query Qdrant CLIP DB];
        R --> T[Display Results];
        S --> T;
    end

    H --> Q;
    L --> Q;
```
---

### 🗂️ Project Directory Structure

```plaintext
multimodal-rag-app/
├── backend/
│   ├── config.py             # All configurations, paths, and model names
│   ├── ingest.py             # Script to process PDFs and create vector databases
│   └── query_handler.py      # Functions to handle the core search logic
├── frontend/
│   └── app.py                # The Streamlit user interface code
├── resources/
│   └── pdfs/
│       └── 6._price_trends.pdf  # << PLACE YOUR PDF HERE
├── .env                      # For storing your secret OpenAI API key
├── .gitignore                # Specifies files and folders for Git to ignore
├── requirements.txt          # All project dependencies
└── README.md                 # This file

---

## Setup and Installation

1. **Clone the repository**
2. **Create and Activate a Virtual Environment:**
**For Windows**
```python
    python -m venv venv
    venv\Scripts\activate
```
**For MacOS**
```python
    python3 -m venv venv
    source venv/bin/activate
```
3. **Install Dependencies:**
```python
pip install -r requirements.txt
```
**Debian/Ubuntu::**
```python
sudo apt-get install poppler-utils

```
**MacOS:**
```python
brew install poppler

```
4. **Setup Environment Variable:**
```python
OPENAI_API_KEY="sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```
## ▶️ How to Run the Application

The application runs in two main stages: a **one-time data ingestion** for your chosen PDF, followed by launching the **interactive query app**.

### Stage 1: Place Your PDF

Navigate to the `resources/pdfs/` directory. You can delete the existing PDF and **place your own PDF file** in this folder. The `ingest.py` script is configured to automatically pick it up.

### Stage 2: Run Data Ingestion (One-Time per PDF)

Before you can query the document, you must process it and create the vector databases. You need to run the ingestion command for **both methods**.

Run these commands from the **root directory** of the project.

1.  **Create the GPT Summaries Database:**
    This command will read the PDF, generate summaries for all text and images using GPT-4o, and store their embeddings in the `qdrant_gpt_summaries_db` folder.

    ```bash
    python -m backend.ingest --method gpt
    ```

2.  **Create the CLIP Embeddings Database:**
    This command will read the PDF, generate CLIP embeddings for all raw text and images, and store them in the `qdrant_clip_db` folder.

    ```bash
    python -m backend.ingest --method clip
    ```

### Stage 3: Launch the Frontend Application

Once the ingestion is complete for both methods, you can start the interactive user interface.

```bash
streamlit run frontend/app.py

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

### MIT License
Copyright (c) 2024 [Your Name or Organization]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



