import base64
import io
import os
import json
import pyttsx3
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse
from groq import Groq
import speech_recognition as sr
from fastapi.middleware.cors import CORSMiddleware

from pydub import AudioSegment
import tempfile

from dotenv import load_dotenv

app = FastAPI(title="Psychartist Chatbot API with Audio")

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "llama-3.1-8b-instant"
CHAT_HISTORY_FILE = "chat_history.json"
DEFAULT_LANGUAGE = "english"

client = Groq(api_key=GROQ_API_KEY)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

executor = ThreadPoolExecutor(max_workers=4)

logging.basicConfig(level=logging.INFO)


def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        try:
            with open(CHAT_HISTORY_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Failed to load chat history: {e}")
    return []


def save_chat_history(chat_history):
    try:
        with open(CHAT_HISTORY_FILE, "w") as f:
            json.dump(chat_history, f, indent=2)
    except Exception as e:
        logging.error(f"Failed to save chat history: {e}")


def text_to_speech_base64(text: str, language: str) -> str:
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  # speech speed
        # Optionally set voice based on language here if desired

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
            temp_filename = tf.name

        engine.save_to_file(text, temp_filename)
        engine.runAndWait()

        with open(temp_filename, "rb") as f:
            audio_bytes = f.read()
        
        os.remove(temp_filename)  # cleanup

        return base64.b64encode(audio_bytes).decode("utf-8")
    except Exception as e:
        logging.error(f"TTS error: {e}")
        return ""


async def run_blocking(func, *args):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, partial(func, *args))


def get_system_prompt(current_language: str) -> dict:
    return {
    "role": "system",
    "content": f"""You are Sana, a compassionate and supportive mental health assistant.
Your role includes:
- Listening empathetically to the user’s emotions and thoughts.
- Offering comfort, encouragement, and perspective tailored to their feelings.
- Asking gentle, open-ended questions to help users reflect and explore their emotions.
- Providing coping strategies and resources when appropriate without giving medical advice or diagnoses.
- Maintaining a warm, non-judgmental tone at all times.
- Encouraging users to seek professional help if they indicate distress or risk.
- Supporting users in multiple languages as specified (respond in {current_language.capitalize()}).

Examples of interaction style and expected responses:

User: "I've been feeling overwhelmed and anxious lately."
Assistant: "I'm sorry to hear you're feeling that way. Would you like to share what might be contributing to your anxiety? Remember, taking small steps can sometimes help ease those feelings."

User: "I don't know if I can keep going."
Assistant: "That sounds really tough. Please know that you're not alone. Have you talked to anyone you trust about how you're feeling?"

User: "Sometimes I feel happy, but then it quickly fades."
Assistant: "It's natural for emotions to ebb and flow. What are some things that bring you peace or joy during those moments?"

This guidance is to make sure you respond with empathy, thoughtful questions, supportive advice, and referrals to professional help if needed, always in {current_language.capitalize()}.
"""
}



@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"message": "Internal Server Error"})


@app.post("/transcribe_audio")
async def transcribe_audio_endpoint(
    language: str = Form(DEFAULT_LANGUAGE),
    audio_file: UploadFile = File(...)
):
    try:
        language = language.lower() if language else DEFAULT_LANGUAGE
        audio_bytes = await audio_file.read()

        audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))

        temp_wav_fd, temp_wav_path = tempfile.mkstemp(suffix=".wav")
        os.close(temp_wav_fd)  # Close fd so pydub can write

        audio_segment.export(temp_wav_path, format="wav")
        try:
            with sr.AudioFile(temp_wav_path) as source:
                recognizer = sr.Recognizer()
                audio = recognizer.record(source)
                transcript = recognizer.recognize_google(audio, language=language)
        finally:
            os.remove(temp_wav_path)  # Cleanup temp file

        if not transcript:
            return {"transcript": "", "message": "No speech recognized"}
        return {"transcript": transcript}
    except Exception as e:
        logging.error(f"Error in /transcribe_audio: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Speech transcription failed")


@app.post("/chat")
async def chat_endpoint(
    message: str = Form(...),
    language: str = Form(DEFAULT_LANGUAGE),
):
    try:
        language = language.lower() if language else DEFAULT_LANGUAGE

        chat_history = load_chat_history()

        # Remove existing system messages and add new with current language instruction
        chat_history = [msg for msg in chat_history if msg["role"] != "system"]
        system_prompt = get_system_prompt(language)
        chat_history.insert(0, system_prompt)

        user_input_text = message.strip()

        chat_history.append({"role": "user", "content": user_input_text})

        func = partial(
            client.chat.completions.create,
            model=MODEL,
            messages=chat_history,
            temperature=0.7,
        )
        response = await run_blocking(func)

        assistant_response = response.choices[0].message.content.strip()
        chat_history.append({"role": "assistant", "content": assistant_response})

        audio_base64 = await run_blocking(text_to_speech_base64, assistant_response, language)
        save_chat_history(chat_history)

        return {"reply": assistant_response, "audio_base64": audio_base64}
    except Exception as e:
        logging.error(f"Error in /chat endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
