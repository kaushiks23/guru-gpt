

# In[1]:


import streamlit as st
import requests

# API endpoint for FastAPI backend
API_URL = "https://zen-gpt-production.up.railway.app/ask"

st.title("ZenBot.AI – Mindfulness meets machine!")
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


with st.expander("🤖 About Me"):
    st.image("my_photo.jpg", width=100)  # Replace with the correct path if needed

    st.markdown("""
    **Kaushik Shankar**

    Data Scientist with 12+ years of experience solving problems with machine learning, NLP, and a healthy dose of curiosity.  
    I’m especially interested in how AI can be applied in the realm of **mental health** — not to replace human care, but to enhance awareness, mindfulness, and emotional wellbeing. If    used right, I believe AI can actually help us become more human.

    Outside of work, you’ll find me  jamming on my guitar to classic rock, chasing mountains and beaches, meditating, or lifting just enough to earn my next snack. I like my code clean, my humor dry, and my life balanced.

    [GitHub](https://github.com/kaushiks23) | [LinkedIn](https://www.linkedin.com/in/kaushikshankar)
    """)



# In[5]:

