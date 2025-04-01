############################################
# backend.py (No large text_chunks.json)
############################################

import os
import json
import faiss
import logging
import requests
import gdown

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware

############################################
# FASTAPI SETUP
############################################
app = FastAPI(
    title="GuruGPT",
    description="GuruGPT – Enlightenment, now in beta. Ask away, oh seeker of wisdom (or just mildly curious procrastinator)",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

############################################
# LOGGING
############################################
logging.basicConfig(level=logging.DEBUG)

############################################
# MODEL SETUP
############################################
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

GEMINI_API_KEY = "AIzaSyBLdog6KK4fDICicMQreR2dd01XISBrdy8"  # <--- Put your real key here
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-pro")

############################################
# FAISS INDEX (No large text_chunks.json)
############################################
INDEX_PATH = "spiritual_index.faiss"

if not os.path.exists(INDEX_PATH):
    raise RuntimeError("FAISS index file not found!")

index = faiss.read_index(INDEX_PATH)
index.nprobe = 10
logging.info("Loaded FAISS index from file.")

############################################
# REQUEST MODEL
############################################
class QueryRequest(BaseModel):
    question: str

############################################
# ROUTES
############################################
@app.get("/")
async def root():
    return {"message": "Guru-GPT minimal backend is running without text_chunks.json!"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/ask")
async def ask_chatbot(request: QueryRequest):
    """
    Accepts JSON: { "question": "..." }
    Uses FAISS minimally, but no big text chunks loaded.
    Returns placeholder or minimal response from Gemeni.
    """
    try:
        question = request.question.strip()
        if not question:
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        # Minimal get_context: skip large file logic
        context = "No relevant context found. (text_chunks.json is skipped)"

        # Send to Gemini
        response = gemini_model.generate_content(
            f"You are a spiritual guide.\nContext: {context}\nQuestion: {question}"
        )
        
        return {"response": response.text}

    except Exception as e:
        logging.error(f"Error in /ask endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
