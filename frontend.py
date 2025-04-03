import streamlit as st
import requests
import html

# API endpoint for FastAPI backend
API_URL = "https://zen-gpt-production.up.railway.app/ask"

st.set_page_config(page_title="ZenBot.AI", page_icon="🧘‍♂️")

st.title("ZenBot.AI – Mindfulness meets Machine!")
st.write("Ask your questions, oh seeker of peace (or just someone dodging deadlines with purpose!).")

user_question = st.text_input("Enter your question:")

if st.button("Ask"):
    if user_question.strip():
        import html
        response = requests.post(API_URL, json={"question": user_question})
        
        if response.status_code == 200:
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


# 👤 About Me Expander

with st.expander("🙋‍♂️ About Me"):
    st.markdown(
        """
        <div style="display: flex; align-items: flex-start; gap: 20px;">
            <img src="https://i.imgur.com/IsQ3stK.jpeg" width="150" style="border-radius: 10px; min-width: 150px;"/>
            <div style="flex: 1;">
                Hi, I’m Kaushik — a Data Scientist with 12+ years of experience working across AI, Machine Learning, NLP, and a healthy dose of curiosity.

                <p>This chatbot is an experimental project close to my heart — a blend of AI and mindfulness. The goal isn’t to replace human wisdom, but to make it more accessible, spark reflection, and maybe even offer a moment of calm in a noisy world. It’s a work in progress, and I plan to keep improving it by refining the prompts and adding more relevant knowledge chunks over time.</p>

                <p>I’m especially interested in how AI can support emotional wellbeing and self-awareness — when done thoughtfully, I believe it can help us reconnect with what makes us human.</p>

                <p>Outside of work, I’m usually strumming classic rock on the guitar, hitting the gym just enough to not feel guilty about my next snack, or enjoying the mountains and beaches whenever I get the chance. I’m also a huge Seinfeld fan and love playing a good game of badminton. I try to keep my code clean, my humor dry, and life somewhere between hustle and peace.</p>

                <p>Got feedback or ideas? I’d genuinely love to hear from you.</p>
                <hr style="margin-top: 1em; margin-bottom: 0.5em;" />
                <a href="mailto:kaushik.s23@gmail.com">Email</a> |
                <a href="https://github.com/kaushiks23" target="_blank">GitHub</a> |
                <a href="https://www.linkedin.com/in/kaushik-sh" target="_blank">LinkedIn</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
