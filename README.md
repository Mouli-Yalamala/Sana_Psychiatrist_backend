# 🎧 Sana — Multimodal Mental Health Assistant (Text + Voice)

**Sana** is a compassionate, multimodal mental-health assistant powered by **Groq LLM**, **FastAPI**, **Speech Recognition**, and **Text-to-Speech**.  
It supports:

- 🗣️ **Voice input → Text** (Speech-to-Text)  
- 🔊 **Text → Voice output** (Text-to-Speech)  
- 💬 **Emotionally supportive conversations**  
- 🌍 **Multi-language support**  
- 🔒 **Local chat history storage**  
- ⚡ **Fast responses using Groq LLaMA 3.1 8B-Instant**

This project aims to create a warm, empathetic conversational experience for users who want emotional support or someone to talk to.

---

## 📁 Project Structure

```
Psychartist/
│
├── backend.py             # Core FastAPI backend with STT + TTS + Chat
├── requirements.txt       # Python dependencies
├── chat_history.json      # Local chat memory (auto-generated)
├── README.md              # Documentation
│
└── __pycache__/           # Python cache (ignored)
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/Psychartist.git
cd Psychartist
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Set up environment variables

Create a `.env` file:

```
GROQ_API_KEY=your_groq_api_key_here
```

---

## 🚀 Running the Backend Server

Start the FastAPI server:

```bash
python backend.py
```

This launches the API, which includes:

- `/chat` → Text-based conversation endpoint  
- `/transcribe_audio` → Speech-to-text endpoint  

You can connect this to a **frontend**, **mobile app**, or **desktop UI** easily.

---

## 🧠 AI Capabilities

### ✔ Empathetic Conversations  
The assistant follows a detailed **system prompt** that ensures:

- warm, compassionate responses  
- open-ended emotional questions  
- no medical diagnosis  
- supportive tone  
- multi-language replies  

### ✔ Speech-to-Text (Audio → Text)  
Powered by:

- **SpeechRecognition**
- **Google Speech API**
- **Pydub**

```bash
POST /transcribe_audio
```

### ✔ Text-to-Speech (Text → Audio Base64)  
Generated using:

- **pyttsx3**
- Temporary WAV files
- Base64 encoding for easy frontend playback

### ✔ Chat Completions (Groq API)  
Ultra-fast responses using:

- **LLaMA-3.1-8B-Instant**

---

## 🧪 Sample Chat Request

```python
from model import RAG

rag = RAG()
response = rag.ask("I've been feeling sad lately...")
print(response)
```

---

## 📡 API Endpoints

### 🔵 **POST /chat**
Send a message → get empathetic response + audio TTS

**Form Fields:**
- `message`: user text  
- `language`: response language (default: english)

**Response:**
```json
{
  "reply": "I'm really sorry you're feeling this way...",
  "audio_base64": "UklGRiQAAABXQVZFZm10IBAAAAABAAEA..."
}
```

---

### 🔵 **POST /transcribe_audio**
Upload an audio file → get transcript

**Form Fields:**
- `language`: (optional)
- `audio_file`: WAV/MP3/etc.

---

## 💾 Chat History

Conversations are stored locally in:

```
chat_history.json
```

This ensures:

- session memory  
- personalized replies  
- continuity between interactions  

---

## 🛡️ Error Handling

Global exception handler ensures:

- readable error logs  
- 500 Internal Server Error fallback  
- safe user experience  

---

## 🛠 Technologies Used

- **FastAPI**
- **Groq LLaMA-3.1-8B-Instant**
- **SpeechRecognition**
- **Pydub**
- **pyttsx3 TTS**
- **Python asyncio + ThreadPoolExecutor**
- **CORS Middleware for frontend integration**

---

## 📌 Future Improvements

- Add emotional sentiment detection  
- Add memory summarization  
- Add WebSockets for real-time chat  
- Add user-specific profiles  
- Deploy on Cloud (Railway / Render / HuggingFace Spaces)  
- Add proper UI (React / Flutter / Streamlit)

---

## ✨ Author

**Mouli Yalamala**  
AI/ML Developer | Speech + NLP | Agentic Systems  
GitHub: https://github.com/Mouli-Yalamala  

---

## ⭐ Support

If this project helped or inspired you, please consider **starring ⭐ the repository**!

