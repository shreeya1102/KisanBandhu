# main.py
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import base64
import tempfile
import os
from faster_whisper import WhisperModel
import edge_tts
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models (takes 1–3 minutes first time only)
print("Loading Whisper model... (first time takes 2–3 minutes)")
whisper_model = WhisperModel("medium", device="cpu", compute_type="int8")

async def llm_generate(text: str) -> str:
    # Simple free fallback — replace later with Grok/HF if you want
    prompts = {
        "फसल कब बोनी चाहिए": "गेहूं की बुवाई अक्टूबर-नवंबर में करें।",
        "कीटनाशक कौन सा": "नीम का तेल या देसी तरीके आजमाएं।",
        "बारिश कम है": "मल्चिंग करें और ड्रिप सिंचाई लगवाएं।"
    }
    for key in prompts:
        if key in text.lower():
            return prompts[key]
    return f"आपने कहा: {text}\nमैं आपकी मदद कर रहा हूँ। अभी यह डेमो है।"

async def text_to_speech(text: str):
    communicate = edge_tts.Communicate(text, voice="hi-IN-MadhurNeural")
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    await communicate.save(tmp.name)
    with open(tmp.name, "rb") as f:
        audio = f.read()
    os.unlink(tmp.name)
    return base64.b64encode(audio).decode()

@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client connected locally!")
    try:
        while True:
            data = await websocket.receive_text()
            audio_bytes = base64.b64decode(data)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                f.write(audio_bytes)
                path = f.name

            # Speech → Text
            segments, _ = whisper_model.transcribe(path, language="hi")
            user_text = " ".join(seg.text for seg in segments).strip()
            os.unlink(path)

            if not user_text:
                continue

            print("किसान ने कहा:", user_text)
            await websocket.send_text(f"TEXT:{user_text}")

            # Generate reply
            reply = await llm_generate(user_text)
            print("जवाब:", reply)
            await websocket.send_text(f"BOT:{reply}")

            # Text → Speech
            audio_b64 = await text_to_speech(reply)
            await websocket.send_text(f"AUDIO:{audio_b64}")

    except Exception as e:
        print("Disconnected", e)