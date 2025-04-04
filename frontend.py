import streamlit as st
import requests
import html

# API endpoint
API_URL = "https://zen-gpt-production.up.railway.app/ask"

# Page setup
st.set_page_config(page_title="ZenBot.AI", page_icon="🧘‍♂️")

st.markdown(
    """
    <style>
    pre {
        white-space: pre-wrap !important;
        word-break: break-word !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Custom title with slightly reduced font
st.markdown(
    """
    <h1 style='font-size: 2.4rem; margin-bottom: 0.5rem;'>ZenBot.AI – Breathe. Ask. Reflect.</h1>
    <p style='font-size: 1rem; color: #ccc;'>Ask your questions, oh seeker of peace (or just someone dodging deadlines with purpose!).</p>
    """,
    unsafe_allow_html=True
)

# User input
user_question = st.text_input("Enter your question:")

if st.button("Ask"):
    if user_question.strip():
        response = requests.post(API_URL, json={"question": user_question})

        if response.status_code == 200:
            st.markdown("**You asked:**")
            st.code(user_question, language='text')  # ✅ Includes copy button

            st.markdown("**Response:**")
            cleaned_response = html.unescape(response.json()["response"]).strip().replace("</div>", "")
            st.code(cleaned_response, language='text')  # ✅ Includes copy button
        else:
            st.error("Error fetching response. Please try again.")



# 👤 About Me
with st.expander("🙋‍♂️ About Me"):
    st.image("https://i.imgur.com/IsQ3stK.jpeg", width=200)
    st.markdown("""
Hi, I’m Kaushik — a Data Scientist with 12+ years of experience working across AI, Machine Learning, NLP, and a healthy dose of curiosity.  

This chatbot is an experimental project close to my heart — a blend of AI and mindfulness. The goal isn’t to replace human wisdom, but to make it more accessible, spark reflection, and maybe even offer a moment of calm in a noisy world. It’s a work in progress, and I plan to keep improving it by refining the prompts and adding more relevant knowledge chunks over time.

I’m especially interested in how AI can support emotional wellbeing and self-awareness — when done thoughtfully, I believe it can help us reconnect with what makes us human.

Outside of work, I’m usually strumming some classic rock on the guitar, hitting the gym just enough to not feel guilty about my next snack, or enjoying the mountains and beaches whenever I get the chance. I’m also a huge Seinfeld fan and love playing a good game of badminton. I try to keep my code clean, my humor dry, and life somewhere between hustle and peace.

Got feedback or ideas? I’d genuinely love to hear from you!

---

[Email](mailto:kaushik.s23@gmail.com) | [GitHub](https://github.com/kaushiks23) | [LinkedIn](https://www.linkedin.com/in/kaushik-sh)
""")
