# 🩵 Milo – Multi Turn Memory Chatbot

*A little space to think out loud.*

Milo is an AI-powered conversational chatbot built using Python, Streamlit and Google's Gemini API. Unlike a basic question-answering chatbot, Milo is designed to maintain conversational context and remember information shared by users throughout an active conversation.

From remembering your name and educational background to recalling your hobbies and interests, Milo makes conversations feel more natural, personal and interactive.

---

## ✨ Features

- **Multi-Turn Memory:** Retains conversational context to recall information shared in earlier messages.
- **Personalised Conversations:** Uses previously shared details to generate relevant responses.
- **Contextual Understanding:** Understands follow-up questions based on earlier interactions.
- **Interactive Chat Interface:** Clean, user-friendly interface developed using Streamlit.
- **Conversation History:** Displays recent conversations through a sidebar.
- **Custom UI Design:** Features a soft powder-blue aesthetic, a custom Milo character and an interactive chat experience.
- **Gemini Integration:** Uses Google's Gemini API to generate intelligent conversational responses.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | User interface |
| Google Gemini API | LLM integration and response generation |
| Google GenAI SDK | Connecting Python with Gemini |
| Git & GitHub | Version control and project hosting |

## 📂 Project Structure

```text
Milo_Memory_Chatbot/
│
├── app.py              # Main application
├── requirements.txt    # Project dependencies
├── README.md           # Project documentation
├── .gitignore          # Excluded files
└── .env.example        # API key configuration template
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/suveshak/llm-ps20-20.git
```

### 2. Navigate to the project directory

```bash
cd llm-ps20-20
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Gemini API key

- Obtain an API key from [Google AI Studio](https://aistudio.google.com/).
- Create a `.env` file in the project directory.
- Add your API key using the same variable name specified in `.env.example`.
- Never upload your actual API key to GitHub.

### 6. Run the application

```bash
streamlit run app.py
```

Milo will open in your browser!

## 🧪 Testing

The chatbot was tested using multiple conversational scenarios:

1. **Personal Information:** Sharing and recalling the user's name and field of study.
2. **Interest Recognition:** Identifying hobbies, music preferences and activities.
3. **Basic Memory Recall:** Asking questions about previously shared information.
4. **Multiple Detail Recall:** Retrieving multiple personal details from earlier messages.
5. **Contextual Understanding:** Generating a description of the user based on the conversation.

The tests demonstrated Milo's ability to use previously shared information within an active conversation.

## 🔮 Future Improvements

- Implement persistent memory across separate chat sessions.
- Integrate a database such as SQLite for storing conversation history.
- Add user-controlled memory management.
- Improve contextual retrieval and personalisation.


