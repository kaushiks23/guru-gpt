# backend.py

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Minimal app is running!"}

@app.post("/ask")
async def ask_mock():
    return {"response": "Mock response"}
