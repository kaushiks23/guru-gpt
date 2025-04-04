🧘 ZenBot.AI

ZenBot.AI is a lightweight mindfulness chatbot built using Gemini 2.0 Flash, Sentence Transformers, and FAISS. It retrieves insights from over 11k curated spiritual and mindfulness texts, delivering context-aware answers in real time.

🚀 Live Demo
[🌐 Try zenbot.ai](https://zen-ai-gpt.streamlit.app)
📂 GitHub Repo

⚙️ How It Works
Embeddings: Text chunks embedded using all-MiniLM-L6-v2

Similarity Search: Fast lookup with FAISS index

Answer Generation: Handled by Gemini 2.0 Flash model

Frontend: Built with Streamlit

Backend: FastAPI deployed via Railway

🛠️ Setup & Run
bash
Copy
Edit
# 1. Clone the repo
git clone https://github.com/kaushiks23/zen-gpt.git
cd zen-gpt

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the frontend
streamlit run frontend.py

🔐 Environment Variables
Set these before running:

GEMINI_API_KEY=your_google_api_key

FILE_ID=your_google_drive_file_id

💡 Future Improvements

Replace Google Drive + gdown with cloud storage like S3

Add user conversation memory for follow-up questions

🙌 Credits

Built by Kaushik Shankar.



