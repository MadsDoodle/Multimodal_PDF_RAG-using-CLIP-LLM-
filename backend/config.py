import os
from dotenv import load_dotenv

load_dotenv()

# --- Environment Variables ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- File Paths ---
PDF_PATH = "resources/pdfs/6._price_trends.pdf"
IMAGE_EXTRACTION_DIR = "resources/extracted_images"

# --- Qdrant Database Paths ---
QDRANT_CLIP_DB_PATH = "./qdrant_clip_db"
QDRANT_GPT_DB_PATH = "./qdrant_gpt_summaries_db"

# --- CLIP Method Settings ---
CLIP_MODEL = "ViT-B/32"
CLIP_EMBEDDING_DIM = 512
CLIP_TEXT_COLLECTION = "clip_texts"
CLIP_IMAGE_COLLECTION = "clip_figures"

# --- GPT Summary Method Settings ---
GPT_COMPLETION_MODEL = "gpt-4o-mini"
GPT_EMBEDDING_MODEL = "text-embedding-3-small"
GPT_EMBEDDING_DIM = 1536
GPT_SUMMARIES_COLLECTION = "gpt_summaries"
