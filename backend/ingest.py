# backend/ingest.py
import os
import base64
from PIL import Image
from tqdm import tqdm
import openai
from qdrant_client import QdrantClient, models
from unstructured.partition.pdf import partition_pdf
from . import config

# --- INITIALIZATION ---
print("Initializing clients and models...")
# Initialize OpenAI client
try:
    openai_client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
    print("OpenAI client initialized.")
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    exit()

# Initialize Qdrant client
qdrant_client = QdrantClient(path=config.QDRANT_DB_PATH)
print("Qdrant client initialized.")

# --- HELPER FUNCTIONS ---
def get_openai_embedding(text):
    response = openai_client.embeddings.create(input=text, model=config.EMBEDDING_MODEL)
    return response.data[0].embedding

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# --- MAIN INGESTION LOGIC ---
def run_ingestion():
    # 1. SETUP DIRECTORIES AND COLLECTIONS
    print("Setting up directories and Qdrant collections...")
    os.makedirs(config.IMAGE_EXTRACTION_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(config.QDRANT_DB_PATH), exist_ok=True)

    qdrant_client.recreate_collection(
        collection_name=config.QDRANT_COLLECTION_NAME,
        vectors_config=models.VectorParams(size=config.EMBEDDING_DIM, distance=models.Distance.COSINE),
    )
    print(f"Qdrant collection '{config.QDRANT_COLLECTION_NAME}' is ready.")

    # 2. PARTITION PDF AND EXTRACT ELEMENTS
    print(f"Partitioning PDF: {config.PDF_PATH}")
    chunks = partition_pdf(
        filename=config.PDF_PATH,
        extract_images_in_pdf=True,
        infer_table_structure=True,
        chunking_strategy="by_title",
        extract_image_block_output_dir=config.IMAGE_EXTRACTION_DIR
    )

    # 3. GENERATE SUMMARIES
    all_summaries = []
    
    # Summarize text chunks
    print("Summarizing text chunks...")
    text_elements = [el.text for el in chunks if hasattr(el, "text") and el.text.strip()]
    for text in tqdm(text_elements, desc="Text Summarization"):
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Summarize this technical document section briefly and clearly."},
                {"role": "user", "content": text}
            ]
        )
        summary = response.choices[0].message.content
        all_summaries.append({"text": summary, "type": "text_summary"})

    # Summarize image chunks
    print("Summarizing image figures...")
    image_files = [f for f in os.listdir(config.IMAGE_EXTRACTION_DIR) if f.endswith(('.jpg', '.png'))]
    for fname in tqdm(image_files, desc="Image Summarization"):
        path = os.path.join(config.IMAGE_EXTRACTION_DIR, fname)
        base64_image = encode_image_to_base64(path)
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Describe the figure in the image as if explaining it to a researcher."},
                {"role": "user", "content": [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]}
            ]
        )
        summary = response.choices[0].message.content
        all_summaries.append({"text": summary, "file_path": path, "type": "figure_summary"})

    # 4. EMBED AND UPLOAD TO QDRANT
    print("Generating embeddings and uploading to Qdrant...")
    points_to_upsert = []
    for i, data in enumerate(tqdm(all_summaries, desc="Embedding and Upserting")):
        embedding = get_openai_embedding(data["text"])
        point = models.PointStruct(id=i, vector=embedding, payload=data)
        points_to_upsert.append(point)

    qdrant_client.upsert(
        collection_name=config.QDRANT_COLLECTION_NAME,
        points=points_to_upsert,
        wait=True
    )

    print("\n✅ Ingestion complete!")
    print(f"Processed {len(text_elements)} text chunks and {len(image_files)} images.")
    print(f"Total summaries stored in Qdrant: {len(all_summaries)}")

if __name__ == "__main__":
    run_ingestion()