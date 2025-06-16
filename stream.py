##for running the code on colab or jupyter notebook directly without going thru the hassle of directory structure - first run the .ipynb file and then create a seperate file named `stream.py` with the following code which uses ngrok tunelling.. paste the link you get from the last cell output of the .ipynb file in that stream.py file and then run it to test it locally.. configure the pdf paths as your repo structure
import streamlit as st
import requests
from PIL import Image
import base64
import os

API_URL = "https://your-ngrok-url-here"  # Replace with your ngrok URL or backend API URL

st.title("🤖 Ask Questions from Pre-uploaded PDFs")

query = st.text_input("🔍 Ask a question about the document:")

if st.button("Ask"):
    if query.strip():
        with st.spinner("Fetching response..."):
            resp = requests.post(f"{API_URL}/query", json={"query": query})

        if resp.status_code == 200:
            data = resp.json()
            results = data.get("results", [])

            if not results:
                st.warning("No results found.")
            else:
                for i, item in enumerate(results):
                    st.markdown(f"### ✅ Answer {i+1}")
                    st.markdown(f"**Summary:** {item.get('text', 'No summary')}")

                    # Optional: Show source metadata
                    if "source" in item:
                        st.markdown(f"📍 **Source:** {item['source']}")

                    # Optional: Show image if exists
                    if "file_path" in item:
                        img_path = item["file_path"]
                        if os.path.exists(img_path):
                            st.image(img_path, caption="📷 Retrieved Figure")
                        else:
                            st.warning(f"🖼️ Image not found at: {img_path}")
        else:
            st.error("Query failed. Please check your backend.")
    else:
        st.warning("Please enter a query.")