import streamlit as st
import os
import google.generativeai as genai

import base64


def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    page_bg = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)

add_bg_from_local("AI.jpg")

st.markdown("""
    <style>

    /* Transparent select box (dropdown) */
    div[data-testid="stSelectbox"] > div {
        background: transparent !important;
        color: #00ffcc !important;      /* Text color */
        border: 1px solid #00ffcc !important;
        border-radius: 8px;
        font-size: 16px;
        font-family: 'Poppins', sans-serif;
        width: 500px;
        -webkit-text-fill-color: #0a0a0a;
    }

    /* Dropdown list menu color */
    div[data-testid="stSelectbox"] div[role="listbox"] {
        background-color: rgba(15, 32, 39, 0.95) !important;  /* dark transparent background */
        color: #00ffcc !important;  /* item text color */
    }

    /* Each list item hover effect */
    div[data-testid="stSelectbox"] div[role="option"]:hover {
        background-color: rgba(0, 255, 204, 0.2) !important;
        color: #ffffff !important;
    }

    /* Transparent text area */
    textarea[data-testid="stTextArea"] {
        background: transparent !important;
        color: #00ffcc !important;
        border: 1px solid #00ffcc !important;
        border-radius: 10px;
        font-size: 15px;
        font-family: 'Courier New', monospace;
        # font-family: 'Poppins', sans-serif;
        padding: 10px;
    }

    /* Placeholder text color in text area */
    textarea[data-testid="stTextArea"]::placeholder {
        color: #88cccc;
        opacity: 0.6;
    }

    /* Optional: make buttons glow */
    button[kind="primary"] {
        background-color: #00ffcc !important;
        color: #ffffff !important;
        border-radius: 8px;
        border: none;
        font-weight: bold;
    }
    ul, ol {
        color: #00ffcc !important;
        # font-family: 'Poppins', sans-serif;
    }
    li::marker {
        color: #FFFFFF !important;
    }

    </style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
h1, h3, [data-testid="stSelectbox"], p, warning {
  background: -webkit-linear-gradient(45deg, #00ffcc, #ff00cc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0px 0px 10px rgba(255,255,255,0.3);
  color: #00ffcc;
  border-radius: 8px;
  padding: 8px;
}
</style>


<style>
[data-testid="stSelectbox"] {
    width: 500px;
    -webkit-text-fill-color: #FFFFFF;
}
</style>

<style>
[data-testid="stTextArea"] {
    width: 500px;
    -webkit-text-fill-color: #0a0a0a;
}
</style>

<style>
code {
    color: #00ffcc !important;
    background-color: rgba(0, 255, 204, 0.15) !important;
    padding: 3px 5px;
    border-radius: 5px;
}

pre {
    color: #00ffcc !important;
    background-color: rgba(0, 255, 204, 0.12) !important;
    padding: 10px;
    border-radius: 10px;
    border: 1px solid #00ffcc;
}

table, th, td {
    color: #00ffcc !important;
    border: 1px solid #00ffcc !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #00ffcc !important;
}

p {
    color: #00ffcc !important;
}
</style>

""", unsafe_allow_html=True)



st.set_page_config(page_title="Gemini Text Generator", layout="wide")
st.title("🤖 Google Gemini Text-to-Text Generator")


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("No API key found. Set it first using: setx GEMINI_API_KEY 'your_api_key'")
    st.stop()

genai.configure(api_key=api_key)


model_name = st.selectbox(
    "Choose Gemini Model:",
    [
        "models/gemini-2.5-flash-lite-preview-06-17",
        "models/gemini-2.5-flash-lite-preview-09-2025",
    ]
)

prompt = st.text_area("💬 Enter your prompt:", height=150, placeholder="Ask me anything...")

if "history" not in st.session_state:
    st.session_state.history = [] 

if st.button("🚀 Generate Response"):
    if not prompt.strip():
        st.warning("Please enter a prompt first.")
    else:
        try:
            model = genai.GenerativeModel(model_name)
            with st.spinner("Generating response..."):
                response = model.generate_content(prompt)
                text = response.text if hasattr(response, "text") else str(response)
                st.markdown("""
                            <hr style="border: 2px solid #00ffcc; border-radius: 5px;">
                            """, unsafe_allow_html=True)
                st.markdown("### 🧾 Response:")
                st.write(text)
                st.session_state.history.append({"prompt": prompt, "response": text})
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("""
<hr style="border: 2px solid #00ffcc; border-radius: 5px;">
""", unsafe_allow_html=True)

st.subheader("📜 Conversation History")

if st.session_state.history:
    for i, h in enumerate(reversed(st.session_state.history[-10:]), 1):
        with st.expander(f"Prompt {len(st.session_state.history) - i + 1}: {h['prompt'][:40]}..."):
            st.write("**Prompt:**", h["prompt"])
            st.write("**Response:**", h["response"])
else:
    st.info("No history yet. Generate a response to see history here!")

st.markdown("""
<p style="text-align:center; font-weight:600; color:#00ffcc; margin:8px 0;">
  @copyright Piyush Gupta
</p>
""", unsafe_allow_html=True)
