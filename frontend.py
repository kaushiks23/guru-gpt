

# In[1]:


import streamlit as st
import requests

# API endpoint for FastAPI backend
API_URL = "https://zen-gpt-production.up.railway.app/ask"

st.title("ZenBot.AI – Mindfulness meets Machine!")
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
with st.expander("🙋‍♂️ About Me"):
    st.image("https://i.imgur.com/xyzABC.jpg", width=150)  # Replace with your actual Imgur link
    st.markdown("""
Hi, I’m Kaushik — a Data Scientist with 12+ years of experience working across AI, Machine Learning, NLP, and a healthy dose of curiosity.  

This chatbot is an experimental project close to my heart — a blend of AI and mindfulness. The goal isn’t to replace human wisdom, but to make it more accessible, spark reflection, and maybe even offer a moment of calm in a noisy world. It’s a work in progress, and I plan to keep improving it by refining the prompts and adding more relevant knowledge chunks over time.

I’m especially interested in how AI can support emotional wellbeing and self-awareness — when done thoughtfully, I believe it can help us reconnect with what makes us human.

Outside of work, you’ll probably find me jamming to classic rock, chasing mountains and beaches, or lifting just enough to justify my next snack. I like my code clean, my humor dry, and my life balanced.

Got feedback or ideas? I’d genuinely love to hear from you:

---

[Email](mailto:kaushiks.s23@gmail.com) | [GitHub](https://github.com/kaushiks23) | [LinkedIn](https://www.linkedin.com/in/kaushikshankar)
""")




