
import os
import json
import faiss
import logging
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

# Initialize FastAPI
app = FastAPI(title="GuruGPT", description="GuruGPT – Enlightenment, now in beta. Ask away, oh seeker of wisdom (or just mildly curious procrastinator)")

# Load Sentence Transformer Model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Configure Gemini AI
GEMINI_API_KEY = "AIzaSyBLdog6KK4fDICicMQreR2dd01XISBrdy8"  # Replace with actual key
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-pro")

# FAISS index file
INDEX_PATH = "spiritual_index.faiss"

# Use FAISS's on-disk index to reduce RAM usage
if os.path.exists(INDEX_PATH):
    index = faiss.read_index(INDEX_PATH, faiss.IO_FLAG_ONDISK_SAME_DIR)
    index.nprobe = 10
    logging.info("Loaded FAISS index from file.")
else:
    raise RuntimeError("FAISS index file not found!")

# Google Drive file ID for text_chunks.json

TEXT_CHUNKS_PATH = "text_chunks.json"
URL = f"https://drive.google.com/uc?export=download&id=1WDYlSFMKAL7tKxm8gAc_E6ct1yBb45i_"

# Download text_chunks.json if not already downloaded
if not os.path.exists(TEXT_CHUNKS_PATH):
    print("Downloading text_chunks.json from Google Drive...")
    response = requests.get(URL)
    if response.status_code == 200:
        with open(TEXT_CHUNKS_PATH, "wb") as f:
            f.write(response.content)
        print("Download complete.")
    else:
        raise RuntimeError("Failed to download text_chunks.json!")

# Function to read JSON in batches
def read_json_in_batches(filename, batch_size=100):
    with open(filename, "r", encoding="utf-8") as f:
        batch = []
        for line in f:
            try:
                chunk = json.loads(line)
                batch.append(chunk)
            except json.JSONDecodeError as e:
                print(f"JSON error: {e}, Line: {line}")  # Debugging line
            if len(batch) >= batch_size:
                yield batch  
                batch = []
        if batch:
            yield batch


# Define request model
class QueryRequest(BaseModel):
    question: str

# Function to retrieve context using batch processing
def get_context(query, batch_size=100):
    query_embedding = embedding_model.encode([query], convert_to_numpy=True).astype('float32')
    
    best_match = None
    best_score = float('inf')

    for batch in read_json_in_batches(TEXT_CHUNKS_PATH, batch_size=batch_size):
        print("DEBUG: Batch received =", batch)  # Debugging print

        if not isinstance(batch, list):  # Ensure batch is a list
            print("ERROR: Batch is not a list! Received:", type(batch), batch)
            continue  # Skip processing
        
        batch_texts = [chunk["text"] for chunk in batch]  # Extract text only
        batch_embeddings = embedding_model.encode(batch_texts, convert_to_numpy=True).astype('float32')

        _, indices = index.search(batch_embeddings, 1)  # Find closest match
        for i, idx in enumerate(indices):
            if idx < len(batch) and idx < best_score:
                best_match = batch[idx]["text"]
                best_score = idx

    return best_match or "No relevant context found."

# API Endpoint for chatbot
@app.post("/ask")
async def ask_chatbot(request: QueryRequest):
    context = get_context(request.question)
    response = gemini_model.generate_content(f"You are a spiritual guide providing insights.\nContext: {context}\nQuestion: {request.question}")

    return {"response": response.text}

