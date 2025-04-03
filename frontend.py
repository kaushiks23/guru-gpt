

# In[1]:


import streamlit as st
import requests

# API endpoint for FastAPI backend
API_URL = "https://zen-gpt-production.up.railway.app/ask"


st.title("ZenBot.AI – Mindfulness meets Machine!")
st.write("Ask your questions, oh seeker of peace (or just someone dodging deadlines with purpose!).")

user_question = st.text_input("Enter your question:")

if st.button("Ask"):
    if user_question.strip():
        # Send request to FastAPI
        response = requests.post(API_URL, json={"question": user_question})
        
        if response.status_code == 200:
            import html
            st.markdown("**Response:**")
            
            # Sanitize and style the Gemini response
            cleaned_response = html.unescape(response.json()["response"])
            
            st.markdown(
                f"""
                <div style="background-color:#262730; padding: 20px; border-radius: 10px; color: white; font-size: 16px;">
                    {cleaned_response}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.error("Error fetching response. Please try again.")

with st.expander("🙋‍♂️ About Me"):
    st.image("https://i.imgur.com/YbHypJc.jpeg", width=200)  # Replace with your actual Imgur link
    st.markdown("""
Hi, I’m Kaushik — a Data Scientist with 12+ years of experience working across AI, Machine Learning, NLP, and a healthy dose of curiosity.  

This chatbot is an experimental project close to my heart — a blend of AI and mindfulness. The goal isn’t to replace human wisdom, but to make it more accessible, spark reflection, and maybe even offer a moment of calm in a noisy world. It’s a work in progress, and I plan to keep improving it by refining the prompts and adding more relevant knowledge chunks over time.

I’m especially interested in how AI can support emotional wellbeing and self-awareness — when done thoughtfully, I believe it can help us reconnect with what makes us human.

Outside of work, I’m usually strumming some classic rock on the guitar, planning my next mountain or beach escape, or hitting the gym just enough to not feel guilty about my next snack. I try to keep my code clean, my humor dry, and life somewhere between hustle and peace.

Got feedback or ideas? I’d genuinely love to hear from you!

---

[Email](mailto:kaushik.s23@gmail.com) | [GitHub](https://github.com/kaushiks23) | [LinkedIn](https://www.linkedin.com/in/kaushikshankar)
""")




