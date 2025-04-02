

# In[1]:


import streamlit as st
import requests

# API endpoint for FastAPI backend
API_URL = "https://zen-gpt-production.up.railway.app/ask"

st.title("ZenBot.AI – Mindfulness meets machine")
st.write("Ask your questions, oh seeker of peace (or just someone dodging deadlines with purpose).")

# User input
user_question = st.text_input("Enter your question:")

if st.button("Ask"):
    if user_question.strip():
        # Send request to FastAPI
        response = requests.post(API_URL, json={"question": user_question})
        if response.status_code == 200:
            st.write("**Response:**")
            st.success(response.json()["response"])
        else:
            st.error("Error fetching response. Please try again.")


# In[5]:

