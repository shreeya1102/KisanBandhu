
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
import uuid
import os
from app.voice.stt import stt
from app.voice.tts import tts
from app.llm.gemini import get_response

router = APIRouter()

# 1. Speech → Text (for mic recording)
@router.post("/stt")
async def speech_to_text(file: UploadFile = File(...)):
    path = f"temp_{uuid.uuid4()}.wav"
    with open(path, "wb") as f:
        f.write(await file.read())
    text = stt.transcribe(path)
    os.remove(path)
    return {"text": text}

# 2. Text → Speech (to speak reply)
@router.post("/tts")
async def text_to_speech(request: dict):
    text = request['text']
    path = f"reply_{uuid.uuid4()}.wav"
    tts.speak(text, path)
    return FileResponse(path, media_type="audio/wav", filename="reply.wav")

# 3. Full voice chat (old endpoint - keep for testing)
@router.post("/voice")
async def full_voice_chat(file: UploadFile = File(...)):
    input_path = f"in_{uuid.uuid4()}.wav"
    output_path = f"out_{uuid.uuid4()}.wav"
    try:
        with open(input_write_path, "wb") as f:
            f.write(await file.read())
        text = stt.transcribe(input_path)
        reply = get_response(text)
        tts.speak(reply, output_path)
        return FileResponse(output_path, media_type="audio/wav")
    finally:
        for p in [input_path, output_path]:
            if os.path.exists(p): os.remove(p)