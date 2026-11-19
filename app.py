import uuid
import textwrap
import os
import time
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Milo | Your AI Companion",
    page_icon="🫧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CHATBOT PERSONALITY
SYSTEM_INSTRUCTION = """
You are Milo, a warm, friendly and thoughtful AI companion.

Your responsibilities:
1. Remember the user's name, interests, preferences and goals.
2. Use previous conversation messages to maintain context.
3. Respond naturally and personally.
4. Never invent information about the user.
5. If you do not know something, politely ask.
6. Keep responses conversational, helpful and concise.
7. Make the user feel comfortable sharing their thoughts.

You have short-term memory through the conversation history.
"""

# CUSTOM CSS
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600&display=swap');

.stApp {
    background:
        radial-gradient(
            ellipse at 8% 4%,
            #e1e5ff 0%,
            transparent 35%
        ),
        radial-gradient(
            ellipse at 95% 15%,
            #d4eaff 0%,
            transparent 35%
        ),
        linear-gradient(
            145deg,
            #f8faff,
            #edf4ff,
            #e9edff
        );

    font-family: 'DM Sans', sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.main .block-container {
    max-width: 1150px;
    width: 94%;
    padding-top: 1.2rem;
    padding-bottom: 5rem;
    min-height: 100vh;
    margin: auto;
}

footer {
    visibility: hidden;
}

/* HEADER */

.milo-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 2px 20px;
    margin-bottom: 20px;
    border-bottom: 1px solid rgba(116,151,199,0.2);
}

.milo-brand {
    display: flex;
    align-items: center;
    gap: 13px;
}

.milo-mini-orb {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: radial-gradient(
        circle at 35% 30%,
        #ffffff,
        #ffd4f0 35%,
        #b6ddff 70%,
        #a6b5ee
    );
    box-shadow: 0 5px 25px rgba(151,172,238,0.4);
    position: relative;
}

.milo-mini-orb:after {
    content: '•  •';
    position: absolute;
    top: 13px;
    left: 12px;
    color: #263b5e;
    font-size: 13px;
    letter-spacing: 3px;
}

.milo-name {
    font-family: 'Playfair Display', serif;
    font-size: 1.7rem;
    color: #1c355d;
    font-weight: 600;
}

.milo-tagline {
    font-size: 0.78rem;
    color: #7185a6;
}

.online-status {
    background: rgba(255,255,255,0.7);
    border: 1px solid rgba(116,151,199,0.2);
    border-radius: 30px;
    padding: 8px 13px;
    color: #64849b;
    font-size: 0.75rem;
}

/* MILO FLOATING ANIMATION */

.milo-orb {
    animation: miloFloat 3s ease-in-out infinite;
}

@keyframes miloFloat {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-9px);
    }
}

/* BLINKING EYES */

.milo-orb:before {
    animation: miloBlink 4s infinite;
    transform-origin: center;
}

@keyframes miloBlink {
    0%, 94%, 100% {
        transform: scaleY(1);
    }

    96% {
        transform: scaleY(0.12);
    }

    98% {
        transform: scaleY(1);
    }
}

/* WELCOME CARD */

.welcome-card {
    text-align: center;
    padding: 45px 30px;
    margin: 15px 0 30px;
    width: 100%;
    box-sizing: border-box;
    border-radius: 32px;

    background: linear-gradient(
        125deg,
        rgba(255,255,255,0.88),
        rgba(225,237,255,0.82)
    );

    border: 1px solid rgba(255,255,255,0.95);

    box-shadow:
        0 18px 48px rgba(100,130,181,0.12),
        inset 0 1px 0 white;
}

.milo-orb {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    margin: 0 auto 20px;
    position: relative;

    background:
        radial-gradient(circle at 34% 25%,
        white 0%, rgba(255,255,255,0.7) 12%, transparent 27%),
        radial-gradient(circle at 35% 35%,
        #ffd4f1, #f2c9f4 30%, #b8dcff 70%, #a7b9f4);

    box-shadow:
        0 0 25px rgba(242,190,239,0.5),
        0 0 55px rgba(151,195,255,0.45),
        inset -8px -10px 24px rgba(110,143,213,0.18);
}

.milo-orb:before {
    content: '';
    position: absolute;
    width: 7px;
    height: 7px;
    background: #203456;
    border-radius: 50%;
    top: 47%;
    left: 36%;
    box-shadow: 21px 0 0 #203456;
}

.milo-orb:after {
    content: '';
    position: absolute;
    width: 22px;
    height: 11px;
    border-bottom: 2.5px solid #203456;
    border-radius: 0 0 50% 50%;
    top: 59%;
    left: 42%;
    transform: translateX(-10%);
}

.welcome-card h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: #1c355d;
    font-weight: 500;
    margin-bottom: 8px;
}

.welcome-card p {
    color: #7084a5;
    font-size: 0.92rem;
}

/* SECTION TITLE */

.section-title {
    color: #60799d;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin: 25px 2px 13px;
}

/* CHAT MESSAGES */

[data-testid="stChatMessage"] {
    border: 1px solid rgba(255,255,255,0.9);
    border-radius: 22px;
    padding: 1rem 1.15rem;
    background: rgba(255,255,255,0.72);
    box-shadow: 0 8px 24px rgba(94,125,177,0.08);
    margin-bottom: 13px;
}

[data-testid="stChatMessage"] p {
    color: #263d60;
    font-size: 0.96rem;
    line-height: 1.7;
}

/* CHAT INPUT */

[data-testid="stChatInput"] {
    border: 1px solid rgba(126,158,202,0.35) !important;
    border-radius: 20px !important;
    background: rgba(255,255,255,0.9) !important;
    box-shadow: 0 12px 34px rgba(90,123,178,0.13) !important;
}

[data-testid="stChatInput"] textarea {
    color: #263d60 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #8b9bb5 !important;
}

/* BUTTONS */

.stButton > button {
    width: 100%;
    min-height: 46px;

    border: 1px solid #d2def3 !important;
    border-radius: 16px !important;

    color: #526f99 !important;
    background: rgba(255,255,255,0.75) !important;

    padding: 12px 15px;

    transition: all 0.2s ease;
}

.stButton > button:hover {
    border-color: #9bbce5 !important;
    color: #294a78 !important;
    background: #ffffff !important;

    transform: translateY(-2px);
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #eff5ff, #e7edff);
    border-right: 1px solid rgba(130,160,207,0.2);
}

/* FOOTER */

.milo-footer {
    text-align: center;
    color: #91a0b8;
    font-size: 0.72rem;
    margin-top: 25px;
}


/* AUTOMATIC LIGHT AND DARK THEME SUPPORT */

.stApp {
    background: var(--background-color);
    color: var(--text-color);
}

/* MAIN CONTENT */

[data-testid="stAppViewContainer"] {
    background: var(--background-color);
}

[data-testid="stMain"] {
    background: transparent;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: var(--secondary-background-color);
    border-right: 1px solid
        color-mix(in srgb, var(--text-color) 15%, transparent);
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: var(--text-color);
}

/* WELCOME CARD */

.welcome-card {
    background: var(--secondary-background-color);
    border: 1px solid
        color-mix(in srgb, var(--text-color) 12%, transparent);
}

/* HEADINGS AND TEXT */

.milo-name,
.welcome-card h1 {
    color: var(--text-color);
}

.milo-tagline,
.welcome-card p,
.milo-footer,
.section-title {
    color: var(--text-color);
}

/* CHAT MESSAGES */

[data-testid="stChatMessage"] {
    background: var(--secondary-background-color);
    border: 1px solid
        color-mix(in srgb, var(--text-color) 12%, transparent);
}

[data-testid="stChatMessage"] p {
    color: var(--text-color);
}

/* CHAT INPUT AND BOTTOM AREA */

[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"] {
    background: var(--background-color) !important;
}

[data-testid="stChatInput"] {
    background: var(--secondary-background-color) !important;
    border: 1px solid
        color-mix(in srgb, var(--text-color) 20%, transparent) !important;
}

[data-testid="stChatInput"] textarea {
    color: var(--text-color) !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-color) !important;
    opacity: 0.6;
}

/* BUTTONS */

.stButton > button {
    background: var(--secondary-background-color);
    color: var(--text-color);
    border: 1px solid
        color-mix(in srgb, var(--text-color) 18%, transparent);
}

.stButton > button:hover {
    border-color: var(--primary-color);
    color: var(--text-color);
}

/* HEADER */

.milo-header {
    border-bottom: 1px solid
        color-mix(in srgb, var(--text-color) 15%, transparent);
}

.online-status {
    background: var(--secondary-background-color);
    color: var(--text-color);
}


</style>
""", unsafe_allow_html=True)


# HEADER
st.markdown(
    textwrap.dedent("""
    <div class="milo-header">
        <div class="milo-brand">
            <div class="milo-mini-orb"></div>
            <div>
                <div class="milo-name">milo</div>
                <div class="milo-tagline">
                    a little space to think out loud
                </div>
            </div>
        </div>
        <div class="online-status">
            <span style="color:#64b99a;">●</span>
            here with you
        </div>
    </div>
    """),
    unsafe_allow_html=True
)



# INITIALIZE MULTIPLE CONVERSATIONS

if "chats" not in st.session_state:
    first_id = str(uuid.uuid4())

    st.session_state.chats = {
        first_id: {
            "title": "New chat",
            "messages": []
        }
    }

    st.session_state.active_chat_id = first_id

if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = next(
        iter(st.session_state.chats)
    )


# GET ACTIVE CONVERSATION

active_chat = st.session_state.chats[
    st.session_state.active_chat_id
]

messages = active_chat["messages"]

# SIDEBAR

with st.sidebar:

    st.markdown("## 🫧 Milo")
    st.caption("Your AI Companion")

    # NEW CHAT BUTTON
    if st.button("＋  New chat", use_container_width=True):

        new_id = str(uuid.uuid4())

        st.session_state.chats[new_id] = {
            "title": "New chat",
            "messages": []
        }

        st.session_state.active_chat_id = new_id
        st.rerun()

    st.markdown("---")

    st.markdown("### Recent conversations")

    # DISPLAY CHAT HISTORY
    for chat_id, chat in reversed(
        list(st.session_state.chats.items())
    ):

        title = chat["title"]

        if len(title) > 28:
            title = title[:28] + "..."

        if st.button(
            "💬  " + title,
            key=f"chat_{chat_id}",
            use_container_width=True
        ):

            st.session_state.active_chat_id = chat_id
            st.rerun()

    st.markdown("---")

    st.markdown("---")

    st.caption(
        "Milo remembers your conversations "
        "while your session is active."
    )

# GEMINI CONFIGURATION
api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

try:
    api_key = st.secrets.get("GEMINI_API_KEY", api_key)
    model_name = st.secrets.get("GEMINI_MODEL", model_name)
except Exception:
    pass


if not api_key:

    st.error("Milo needs a Gemini API key to start.")

    st.code(
        "GEMINI_API_KEY=your_api_key_here\n"
        "GEMINI_MODEL=gemini-2.5-flash"
    )

    st.stop()

    # INITIALIZE GEMINI CLIENT

if "client" not in st.session_state:
    st.session_state.client = genai.Client(
        api_key=api_key
    )



# WELCOME SCREEN
if not active_chat["messages"]:

    st.markdown(
        textwrap.dedent("""
        <div class="welcome-card">
            <div class="milo-orb"></div>
            <h1>Hi, I'm Milo! </h1>
            <p>
               Your little AI companion, always ready to listen.
            Let's get to know each other!
            </p>
        </div>

        <div class="section-title">
            A FEW WAYS TO BEGIN
        </div>
        """),
        unsafe_allow_html=True
    )

    prompts = [
        "Let's get to know each other",
        "Help me think through an idea",
        "I want to talk about my day"
    ]

    cols = st.columns(3)

    for i, label in enumerate(prompts):
        if cols[i].button(label, use_container_width=True):
            st.session_state.pending_prompt = label
            st.rerun()

# DISPLAY CHAT HISTORY
for message in active_chat["messages"]:

    is_user = message["role"] == "user"

    with st.chat_message(
        "user" if is_user else "assistant",
        avatar="🙂" if is_user else "🫧"
    ):

        st.markdown(message["content"])


# USER INPUT
prompt = st.chat_input("Write a message to Milo...")

if not prompt and "pending_prompt" in st.session_state:

    prompt = st.session_state.pop("pending_prompt")


# PROCESS MESSAGE
if prompt:
        # GIVE EACH CONVERSATION ITS OWN TITLE
    if len(active_chat["messages"]) == 0:
        active_chat["title"] = prompt[:32]

    active_chat["messages"].append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user", avatar="🙂"):
        st.markdown(prompt)


    # SEND COMPLETE CONVERSATION HISTORY
    history = [

        types.Content(
            role="user" if item["role"] == "user" else "model",
            parts=[
                types.Part.from_text(
                    text=item["content"]
                )
            ]
        )

        for item in active_chat["messages"]
    ]


    try:

        with st.chat_message("assistant", avatar="🫧"):

            with st.spinner("Milo is gathering its thoughts..."):

                response = None

                # RETRY TEMPORARY API ERRORS
                for attempt in range(3):

                    try:

                        response = (
                            st.session_state.client.models.generate_content(
                                model=model_name,
                                contents=history,
                                config=types.GenerateContentConfig(
                                    system_instruction=SYSTEM_INSTRUCTION,
                                    temperature=0.7,
                                    max_output_tokens=800
                                )
                            )
                        )

                        break

                    except Exception as exc:

                        error_text = str(exc)

                        temporary = any(
                            token in error_text
                            for token in [
                                "503",
                                "UNAVAILABLE",
                                "429",
                                "RESOURCE_EXHAUSTED"
                            ]
                        )

                        if not temporary or attempt == 2:
                            raise

                        time.sleep(2 ** attempt)


                answer = (
                    response.text.strip()
                    if response and response.text
                    else "I couldn't respond just now. Please try again."
                )

                st.markdown(answer)


        # SAVE ASSISTANT RESPONSE
        active_chat["messages"].append({
            "role": "assistant",
            "content": answer
        })


    except Exception as error:

        active_chat["messages"].pop()

        st.error("Milo couldn't reach Gemini just now.")

        st.caption(
            "This may be temporary service overload "
            "or an API quota issue. Please try again."
        )

        with st.expander("Technical details"):
            st.code(str(error))


# FOOTER
st.markdown(
    textwrap.dedent("""
    <div class="milo-footer">
        Milo remembers within this conversation.
        Your chat starts fresh when you reset it.
    </div>
    """),
    unsafe_allow_html=True
)
