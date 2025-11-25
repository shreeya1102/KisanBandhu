import os
from app.voice.stt import stt

audio = "sample_hindi.wav"

if not os.path.exists(audio):
    print("\nERROR: sample_hindi.wav not found in project folder!")
    print("Record 5–10 seconds Hindi voice on your phone and save as sample_hindi.wav here:")
    print(os.getcwd())
else:
    print("Transcribing your voice...")
    text = stt.transcribe(audio)
    print("\nYou said ?", text)
