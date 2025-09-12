**Psychartist Chatbot**
This is a FastAPI backend server for the Psychartist chatbot application. It provides endpoints for speech-to-text transcription and AI chatbot text + speech dialogue generation with multilingual support.

**Features**
API to transcribe uploaded audio (supports multiple languages using Google Web Speech API)

AI chat completions via Groq LLM API ("llama-3.1-8b-instant" model)

Text-to-Speech (TTS) support using either Google Cloud Text-to-Speech or local offline pyttsx3

Maintains chat history with system prompts to customize AI personality and multilingual responses

Support for CORS and async handling for fast web integration

**Technology Stack**
Python 3.11+

FastAPI for API server

Groq API client for LLM chat completions

speech_recognition for transcribing audio uploads

pydub for audio format conversions

google-cloud-texttospeech and pyttsx3 for TTS

ThreadPoolExecutor for async background tasks

JSON for chat history persistence

**Environment Setup**
Clone the repository

Install dependencies via:

bash
pip install -r requirements.txt
Configure environment variables or secrets:

GROQ_API_KEY: Your Groq API key

Google Cloud credentials JSON if using Google TTS

Run the server:

bash
uvicorn main:app --reload
API Endpoints
POST /transcribe_audio
Upload audio file and get transcript text.

Form fields:

language: Language code (default: "english")

audio_file: Audio file (wav, mp3, etc.)

Response:

json
{
  "transcript": "Recognized text from audio",
  "message": "Optional message"
}
POST /chat
Send a chat message and get AI response in text and speech.
**Form fields:**

message: User message text

language: Language code (default: "english")

Response:

json
{
  "reply": "AI assistant reply text",
  "audio_base64": "Base64 encoded speech audio"
}
**Notes**
Supports multilingual chat by specifying the language in requests.

Uses system prompts to instruct AI assistant personality ("Sana", compassionate mental health assistant).

Stores chat history locally in chat_history.json.

Text-to-speech uses offline or cloud options configurable in code.
