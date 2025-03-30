<<<<<<< HEAD
#!/usr/bin/env python
# coding: utf-8

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


# Load FAISS index
INDEX_PATH = "spiritual_index.faiss"
TEXT_CHUNKS_PATH = "text_chunks.json"

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Configure Gemini AI
GEMINI_API_KEY = "AIzaSyBLdog6KK4fDICicMQreR2dd01XISBrdy8"  # Replace with actual key
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-pro")

# Check if FAISS index file exists
if os.path.exists(INDEX_PATH):
    index = faiss.read_index(INDEX_PATH)
    logging.info("Loaded FAISS index from file.")
else:
    raise RuntimeError("FAISS index file not found!")

# Load text chunks
if os.path.exists(TEXT_CHUNKS_PATH):
    with open(TEXT_CHUNKS_PATH, "r") as f:
        text_chunks = json.load(f)  # Load stored text chunks
else:
    raise RuntimeError("Text chunks file not found!")

# Function to retrieve context from FAISS
def get_context(query):
    query_embedding = embedding_model.encode([query], convert_to_numpy=True).astype('float32')
    _, I = index.search(query_embedding, 3)  # Top 3 matches

    valid_indices = [i for i in I[0] if 0 <= i < len(text_chunks)]  # Prevent out-of-range errors
    if not valid_indices:
        return "No relevant context found."

    return " ".join([text_chunks[i][0] + f" (Source: {text_chunks[i][1]})" for i in valid_indices])

# Define request model
class QueryRequest(BaseModel):
    question: str

# API Endpoint for chatbot
@app.post("/ask")
async def ask_chatbot(request: QueryRequest):
    context = get_context(request.question)
    response = gemini_model.generate_content(f"You are a spiritual guide providing insights.\nContext: {context}\nQuestion: {request.question}")

    return {"response": response.text}


# In[9]:




=======
#!/usr/bin/env python
# coding: utf-8

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


# Load FAISS index
INDEX_PATH = "spiritual_index.faiss"
TEXT_CHUNKS_PATH = "text_chunks.json"

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Configure Gemini AI
GEMINI_API_KEY = "AIzaSyBLdog6KK4fDICicMQreR2dd01XISBrdy8"  # Replace with actual key
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-pro")

# Check if FAISS index file exists
if os.path.exists(INDEX_PATH):
    index = faiss.read_index(INDEX_PATH)
    logging.info("Loaded FAISS index from file.")
else:
    raise RuntimeError("FAISS index file not found!")

# Load text chunks
if os.path.exists(TEXT_CHUNKS_PATH):
    with open(TEXT_CHUNKS_PATH, "r") as f:
        text_chunks = json.load(f)  # Load stored text chunks
else:
    raise RuntimeError("Text chunks file not found!")

# Function to retrieve context from FAISS
def get_context(query):
    query_embedding = embedding_model.encode([query], convert_to_numpy=True).astype('float32')
    _, I = index.search(query_embedding, 3)  # Top 3 matches

    valid_indices = [i for i in I[0] if 0 <= i < len(text_chunks)]  # Prevent out-of-range errors
    if not valid_indices:
        return "No relevant context found."

    return " ".join([text_chunks[i][0] + f" (Source: {text_chunks[i][1]})" for i in valid_indices])

# Define request model
class QueryRequest(BaseModel):
    question: str

# API Endpoint for chatbot
@app.post("/ask")
async def ask_chatbot(request: QueryRequest):
    context = get_context(request.question)
    response = gemini_model.generate_content(f"You are a spiritual guide providing insights.\nContext: {context}\nQuestion: {request.question}")

    return {"response": response.text}


# In[9]:




>>>>>>> 0cb9a91 (Added FastAPI backend)
