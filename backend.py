import os
import json
import faiss
import logging
import gdown
import requests
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import numpy as np

# Initialize FastAPI
app = FastAPI(
    title="GuruGPT",
    description="GuruGPT – Enlightenment, now in beta. Ask away, oh seeker of wisdom (or just mildly curious procrastinator)"
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

# Constants
GEMINI_API_KEY = "AIzaSyBLdog6KK4fDICicMQreR2dd01XISBrdy8"
FILE_ID = "1WDYlSFMKAL7tKxm8gAc_E6ct1yBb45i_"
TEXT_CHUNKS_PATH = "text_chunks.json"
INDEX_PATH = "spiritual_index.faiss"

# Initialize models
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-pro")

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

# Context Retrieval Function
def get_context(query):
    query_embedding = embedding_model.encode([query], convert_to_numpy=True).astype('float32')
    _, indices = index.search(query_embedding, 3)

    context = ""
    for idx in indices[0]:
        if idx < len(text_chunks):
            context += text_chunks[idx][0] + "\n"
    return context.strip()

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
