import os
import json
import faiss
import logging
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import gdown
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

# Ensure FAISS index exists
if os.path.exists(INDEX_PATH):
    index = faiss.read_index(INDEX_PATH, faiss.IO_FLAG_ONDISK_SAME_DIR)
    index.nprobe = 10
    logging.info("Loaded FAISS index from file.")
else:
    raise RuntimeError("FAISS index file not found!")

import os
import json
import gdown

# Google Drive file ID for text_chunks.json
FILE_ID = "1WDYlSFMKAL7tKxm8gAc_E6ct1yBb45i_"
TEXT_CHUNKS_PATH = "text_chunks.json"

# Function to download the file using gdown
def download_file():
    print("Downloading text_chunks.json from Google Drive using gdown...")
    url = f"https://drive.google.com/uc?id={FILE_ID}"
    gdown.download(url, TEXT_CHUNKS_PATH, quiet=False)

# Step 1: Check if the file exists, otherwise download it
if not os.path.exists(TEXT_CHUNKS_PATH):
    download_file()

# Step 2: Validate the downloaded file
if os.path.exists(TEXT_CHUNKS_PATH):
    file_size = os.path.getsize(TEXT_CHUNKS_PATH)
    print(f"File size: {file_size} bytes")

    if file_size == 0:
        raise RuntimeError("Downloaded text_chunks.json is empty!")

    try:
        with open(TEXT_CHUNKS_PATH, "r", encoding="utf-8") as f:
            first_100_chars = f.read(100)
            print(f"First 100 chars of JSON: {first_100_chars}")

            # If response is an HTML page instead of JSON, Google is blocking the download
            if "<!DOCTYPE html>" in first_100_chars:
                raise RuntimeError("Google Drive is returning an HTML page instead of JSON!")
    except Exception as e:
        raise RuntimeError(f"Error reading file: {e}")

# Step 3: Load JSON data
def load_json(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)  # Load full list
    except Exception as e:
        raise RuntimeError(f"Error loading {filename}: {e}")

# Function to read JSON in batches
def read_json_in_batches(data, batch_size=100):
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]  # Yield a batch of JSON objects


# Define request model
class QueryRequest(BaseModel):
    question: str

# Function to retrieve context using batch processing
def get_context(query, batch_size=100):
    query_embedding = embedding_model.encode([query], convert_to_numpy=True).astype('float32')


    text_chunks = load_json(TEXT_CHUNKS_PATH)  # Load full dataset

    best_match = None
    best_score = float('inf')

    for batch in read_json_in_batches(text_chunks, batch_size=batch_size):
        batch_texts = [chunk["text"] for chunk in batch]
        batch_embeddings = embedding_model.encode(batch_texts, convert_to_numpy=True).astype('float32')

        # Search in FAISS index
        _, indices = index.search(batch_embeddings, 1)  # Get closest match

    text_chunks = load_json(TEXT_CHUNKS_PATH)  # Load full dataset
    best_match = None
    best_score = float('inf')
    for batch in read_json_in_batches(text_chunks, batch_size=batch_size):
        batch_texts = [chunk["text"] for chunk in batch]
        batch_embeddings = embedding_model.encode(batch_texts, convert_to_numpy=True).astype('float32')
        # Search in FAISS index
        _, indices = index.search(batch_embeddings, 1)  # Get closest match

        for i, idx_list in enumerate(indices):
            idx = int(idx_list[0])  # Get best index match
            if 0 <= idx < len(batch) and idx < best_score:
                best_match = batch_texts[i]
                best_score = idx
    return best_match or "No relevant context found."

# API Endpoint for chatbot

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Guru-GPT backend is running!"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

@app.route("/ask", methods=["POST", "HEAD"])
async def ask_chatbot(request: Request):
    if request.method == "HEAD":
        return {}  # Empty response for HEAD requests
    
    try:
        request_data = await request.json()
        question = request_data.get("question")
        
        if not question:
            raise HTTPException(status_code=400, detail="Question is required")
        
        context = get_context(question)
        response = gemini_model.generate_content(
            f"You are a spiritual guide providing insights.\nContext: {context}\nQuestion: {question}"
        )
        
        return {"response": response.text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


