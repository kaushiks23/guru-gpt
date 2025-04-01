import os
import json
import faiss
import logging
import requests
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import gdown

# Initialize FastAPI
app = FastAPI(
    title="GuruGPT",
    description="GuruGPT – Enlightenment, now in beta. Ask away, oh seeker of wisdom (or just mildly curious procrastinator)"
)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Sentence Transformer Model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Configure Gemini AI
GEMINI_API_KEY = "AIzaSyBLdog6KK4fDICicMQreR2dd01XISBrdy8"
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-pro")

# FAISS index file
INDEX_PATH = "spiritual_index.faiss"

if os.path.exists(INDEX_PATH):
    index = faiss.read_index(INDEX_PATH, faiss.IO_FLAG_ONDISK_SAME_DIR)
    index.nprobe = 10
    logging.info("Loaded FAISS index from file.")
else:
    raise RuntimeError("FAISS index file not found!")

# Google Drive file ID for text_chunks.json
FILE_ID = "1WDYlSFMKAL7tKxm8gAc_E6ct1yBb45i_"
TEXT_CHUNKS_PATH = "text_chunks.json"

def download_file():
    print("Downloading text_chunks.json from Google Drive using gdown...")
    url = f"https://drive.google.com/uc?id={FILE_ID}"
    gdown.download(url, TEXT_CHUNKS_PATH, quiet=False)

if not os.path.exists(TEXT_CHUNKS_PATH):
    download_file()

if os.path.exists(TEXT_CHUNKS_PATH):
    file_size = os.path.getsize(TEXT_CHUNKS_PATH)
    print(f"File size: {file_size} bytes")

    if file_size == 0:
        raise RuntimeError("Downloaded text_chunks.json is empty!")

    try:
        with open(TEXT_CHUNKS_PATH, "r", encoding="utf-8") as f:
            first_100_chars = f.read(100)
            print(f"First 100 chars of JSON: {first_100_chars}")
            if "<!DOCTYPE html>" in first_100_chars:
                raise RuntimeError("Google Drive is returning an HTML page instead of JSON!")
    except Exception as e:
        raise RuntimeError(f"Error reading file: {e}")

def load_json(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"Error loading {filename}: {e}")

def read_json_in_batches(data, batch_size=100):
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]

class QueryRequest(BaseModel):
    question: str

# Load text_chunks once at startup
text_chunks = []

@app.on_event("startup")
def load_data():
    global text_chunks
    raw_chunks = load_json(TEXT_CHUNKS_PATH)
    # Convert list-of-lists to list-of-dicts if needed
    if isinstance(raw_chunks[0], list) and len(raw_chunks[0]) == 2:
        text_chunks = [{"text": item[0], "url": item[1]} for item in raw_chunks]
    elif isinstance(raw_chunks[0], dict):
        text_chunks = raw_chunks
    else:
        raise RuntimeError("Unsupported text_chunks format!")

    print(f"Loaded {len(text_chunks)} chunks into memory.")


def get_context(query, batch_size=100):
    start_time = time.time()

    query_embedding = embedding_model.encode([query], convert_to_numpy=True).astype('float32')
    best_match = None
    best_score = float('inf')

    for batch in read_json_in_batches(text_chunks, batch_size=batch_size):
        batch_texts = [chunk["text"] for chunk in batch]
        batch_embeddings = embedding_model.encode(batch_texts, convert_to_numpy=True).astype('float32')

        _, indices = index.search(batch_embeddings, 1)

        for i, idx_list in enumerate(indices):
            idx = int(idx_list[0])
            if 0 <= idx < len(batch) and idx < best_score:
                best_match = batch_texts[i]
                best_score = idx

    elapsed = time.time() - start_time
    logging.info(f"get_context() took {elapsed:.2f} seconds")
    return best_match or "No relevant context found."

@app.get("/")
async def root():
    return {"message": "Guru-GPT backend is running!"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/ask")
async def ask_chatbot(request: QueryRequest):
    try:
        question = request.question

        if not question or not question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        context = get_context(question)
        response = gemini_model.generate_content(
            f"You are a spiritual guide providing insights.\nContext: {context}\nQuestion: {question}"
        )

        return {"response": response.text}

    except Exception as e:
        logging.error(f"Error in /ask endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
