import os
import time
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
st.set_page_config(page_title="Milo", page_icon="🤖", layout="centered",
                   initial_sidebar_state="collapsed")

SYSTEM_INSTRUCTION = """
You are Milo, a friendly conversational assistant with short-term memory.
Use the complete conversation history to remember details the user shares
during this active chat, such as their name, interests, preferences, and goals.
Use remembered details naturally when relevant. Never invent personal details
or claim to remember information that is not in the conversation. If a detail
has not been shared, say you do not know yet. Keep replies warm and concise.
"""

st.markdown("""
<style>
.stApp {background:#fff}
.main .block-container {max-width:900px;padding-top:1.25rem;padding-bottom:6rem}
header[data-testid="stHeader"] {background:#fff}
[data-testid="stChatMessage"] {border-radius:18px;padding:1rem 1.1rem;margin-bottom:1rem}
[data-testid="stChatInput"] {border-radius:16px}
.milo-heading {display:flex;align-items:center;gap:12px;padding:4px 0 18px;
border-bottom:1px solid #eee;margin-bottom:22px}
.milo-icon {width:44px;height:44px;display:flex;align-items:center;
justify-content:center;border-radius:13px;background:#f06b35;font-size:23px}
.milo-name {font-size:1.35rem;font-weight:650;color:#202124}
.milo-subtitle {font-size:.88rem;color:#777;margin-top:2px}
footer {visibility:hidden}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="milo-heading">
  <div class="milo-icon">🤖</div>
  <div><div class="milo-name">Milo</div>
  <div class="milo-subtitle">Your chat, with a memory.</div></div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("Milo")
    st.caption("Multi-turn Memory Chatbot · Problem Statement 20")
    st.write("Milo remembers details you share during this active conversation.")
    st.info("Memory is session-based. Clearing the chat or restarting the session resets it.")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
if not api_key:
    st.error("Gemini API key not found.")
    st.caption("Create a .env file in the project folder and add:")
    st.code("GEMINI_API_KEY=your_api_key_here\nGEMINI_MODEL=gemini-2.5-flash")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=api_key)

for message in st.session_state.messages:
    user_msg = message["role"] == "user"
    with st.chat_message("user" if user_msg else "assistant",
                         avatar="🙂" if user_msg else "🤖"):
        st.markdown(message["content"])

prompt = st.chat_input("Message Milo...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🙂"):
        st.markdown(prompt)

    history = [
        types.Content(
            role="user" if item["role"] == "user" else "model",
            parts=[types.Part.from_text(text=item["content"])],
        )
        for item in st.session_state.messages
    ]

    try:
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Milo is thinking..."):
                response = None
                for attempt in range(3):
                    try:
                        response = st.session_state.client.models.generate_content(
                            model=model_name,
                            contents=history,
                            config=types.GenerateContentConfig(
                                system_instruction=SYSTEM_INSTRUCTION,
                                temperature=0.7,
                                max_output_tokens=800,
                            ),
                        )
                        break
                    except Exception as exc:
                        msg = str(exc)
                        temporary = any(x in msg for x in
                            ["503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED"])
                        if not temporary or attempt == 2:
                            raise
                        time.sleep(2 ** attempt)
                answer = response.text.strip() if response and response.text else "I couldn't respond just now. Please try again."
                st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
    except Exception as error:
        st.session_state.messages.pop()
        st.error("Milo couldn't reach the Gemini service right now.")
        st.caption("This may be temporary service overload or an API quota/model availability issue. Wait a moment and retry.")
        with st.expander("Technical details"):
            st.code(str(error))
