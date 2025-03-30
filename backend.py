

# In[7]:


from fastapi import FastAPI
from pydantic import BaseModel
import faiss
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import json
import os
import logging

# Initialize FastAPI
app = FastAPI(title="GuruGPT", description="GuruGPT – Enlightenment, now in beta. Ask away, oh seeker of wisdom (or just mildly curious procrastinator)")



embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Configure Gemini AI
GEMINI_API_KEY = "AIzaSyBLdog6KK4fDICicMQreR2dd01XISBrdy8"  # Replace with actual key
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-pro")

# Check if FAISS index file exists
INDEX_PATH = "spiritual_index.faiss"

# Use FAISS's on-disk index to reduce RAM usage
if os.path.exists(INDEX_PATH):
    index = faiss.read_index(INDEX_PATH, faiss.IO_FLAG_ONDISK_SAME_DIR)
    index.nprobe = 10
    logging.info("Loaded FAISS index from file.")
else:
    raise RuntimeError("FAISS index file not found!")

# JSON file (Load in chunks to prevent memory overload)
TEXT_CHUNKS_PATH = "text_chunks.json"

def read_json_in_chunks(filename):
    with open(filename, "r") as f:
        for line in f:
            yield json.loads(line)  # Process each line separately

chunks = read_json_in_chunks(TEXT_CHUNKS_PATH)


# Define request model
class QueryRequest(BaseModel):
    question: str

# API Endpoint for chatbot
@app.post("/ask")
async def ask_chatbot(request: QueryRequest):
    context = get_context(request.question)
    response = gemini_model.generate_content(f"You are a spiritual guide providing insights.\nContext: {context}\nQuestion: {request.question}")

    return {"response": response.text}


