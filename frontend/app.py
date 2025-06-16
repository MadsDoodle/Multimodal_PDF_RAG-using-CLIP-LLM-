import streamlit as st
import os
from PIL import Image
# --- Key Change: Direct Backend Imports ---
# We are no longer using 'requests'. Instead, we import our backend functions.
from backend.query_handler import get_clients, search_documents
from backend.config import PDF_PATH

# Set the page configuration for a wider layout
st.set_page_config(layout="wide")

# --- UI Title and Description ---
st.title("🤖 Multimodal RAG Query Engine")
st.write(f"**Document Being Queried:** `{os.path.basename(PDF_PATH)}`")
st.markdown("---")


# --- Caching Backend Clients ---
# This decorator ensures our database and AI clients are loaded only once.
@st.cache_resource
def load_clients():
    """Load Qdrant and OpenAI clients once and cache them."""
    st.write("Initializing clients...")
    clients = get_clients()
    st.write("Clients initialized successfully!")
    return clients

# Load the clients
qdrant_client, openai_client = load_clients()


# --- User Input ---
query = st.text_input(
    "🔍 **Ask a question about the document:**",
    placeholder="e.g., What does the price trend chart say about CPI-AL?"
)

# --- Search and Display Results ---
if st.button("Ask"):
    if query.strip():
        st.markdown("---")
        st.subheader("✅ Search Results")

        with st.spinner("Searching for relevant text and images..."):
            # This now calls our Python function directly
            search_results = search_documents(query, qdrant_client, openai_client)

            if not search_results:
                st.warning("No relevant results found.")
            else:
                # Loop through the results and display them
                for i, hit in enumerate(search_results):
                    # Use two columns for a cleaner layout
                    col1, col2 = st.columns([3, 1])
                    payload = hit.payload

                    with col1:
                        # Display the summary text from the payload
                        st.markdown(f"**Result {i+1} (Score: {hit.score:.4f})**")
                        st.write(payload.get("text", "[No summary available]"))
                        st.caption(f"Source Type: {payload.get('type', 'N/A')}")

                    with col2:
                        # Check for an image and display it if the path exists
                        file_path = payload.get("file_path")
                        if file_path and os.path.exists(file_path):
                            try:
                                image = Image.open(file_path)
                                st.image(image, caption=os.path.basename(file_path), use_column_width=True)
                            except Exception as e:
                                st.error(f"Could not display image: {e}")

                    st.markdown("---") # Separator for each result
    else:
        st.warning("Please enter a query.")

