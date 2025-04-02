

import os
import json
import faiss
import logging
import gdown
import requests
import numpy as np
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from concurrent.futures import ThreadPoolExecutor

# Initialize FastAPI
app = FastAPI(
    title="ZenBot.AI",
    description="ZenBot – Mindfulness meets machine. Ask your questions, oh seeker of peace (or just someone dodging deadlines with purpose)."
)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup logging
logging.basicConfig(level=logging.INFO)

# Constants with hardcoded values
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
FILE_ID = "1_OfpC4Nymam7UqPxJm8-IxBR440RkxGj"
TEXT_CHUNKS_PATH = "text_chunks.json"
INDEX_PATH = "spiritual_index.faiss"

# Initialize models
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel(model_name="gemini-2.0-flash")

# Global variables
text_chunks = []
index = None

# Download text_chunks.json if not present
def download_file():
    if not os.path.exists(TEXT_CHUNKS_PATH):
        logging.info("Downloading text_chunks.json from Google Drive using gdown...")
        url = f"https://drive.google.com/uc?id={FILE_ID}"
        gdown.download(url, TEXT_CHUNKS_PATH, quiet=False)

# Load JSON file
def load_json(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"Error loading {filename}: {e}")

# Preload everything once at startup
@app.on_event("startup")
def on_startup():
    global text_chunks, index

    if not os.path.exists(INDEX_PATH):
        raise RuntimeError("FAISS index file not found!")
    index = faiss.read_index(INDEX_PATH, faiss.IO_FLAG_ONDISK_SAME_DIR)
    index.nprobe = 10
    logging.info("FAISS index loaded.")

    download_file()
    text_chunks = load_json(TEXT_CHUNKS_PATH)
    logging.info(f"Loaded {len(text_chunks)} text chunks.")

# Define request model
class QueryRequest(BaseModel):
    question: str

# Context Retrieval Function (optimized with ThreadPoolExecutor)
def get_context(query):
    query_embedding = embedding_model.encode([query], convert_to_numpy=True).astype('float32')
    _, indices = index.search(query_embedding, 3)  # Top 3 matches for speed

    def fetch_chunk_text(idx):
        return text_chunks[idx][0] if idx < len(text_chunks) else ""

    with ThreadPoolExecutor() as executor:
        top_chunks = list(executor.map(fetch_chunk_text, indices[0]))

    return "\n".join(filter(None, top_chunks)).strip()

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
        if not question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        context = get_context(question)
        response = gemini_model.generate_content(
            f"You are a spiritual guide providing insights.\nContext: {context}\nQuestion: {question}"
        )

        return {"response": response.text}

    except Exception as e:
        logging.error(f"Error in /ask endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
