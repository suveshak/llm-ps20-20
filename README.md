# Milo – Multi-turn Memory Chatbot

**Problem Statement 20 | Roll No. 20**

Milo is a Streamlit chatbot that uses Gemini and the complete conversation history to remember details shared earlier in the active chat session.

## Features
- Minimal chat interface
- Remembers the user's name, interests, and preferences within the active session
- Sends full conversation history with every LLM request
- Clear conversation option
- Brief retry handling for temporary API overloads

## Technology
Python, Streamlit, Google Gen AI SDK, Gemini API, python-dotenv.

## Run locally
1. Install Python 3.10 or newer.
2. In this folder, run `python -m venv venv`.
3. Activate it with `venv\\Scripts\\activate` on Windows.
4. Install dependencies: `pip install -r requirements.txt`.
5. Copy `.env.example` to `.env` and add your real Gemini API key.
6. Run `streamlit run app.py`.

## Memory test
1. Tell Milo: "My name is Alex and I like Python."
2. Tell Milo: "I am studying computer science."
3. Ask: "What is my name and which programming language do I like?"

## Memory limitation
Memory is held in Streamlit session state. Clearing the chat or restarting the session resets it.

## API key safety
Keep your real key in `.env`. Never commit `.env` or share your API key.
