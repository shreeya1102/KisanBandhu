
from TTS.api import TTS
import torch

class HindiTTS:
    def __init__(self):
        print('Loading XTTS-v2 Hindi model... (2-4 min first time only)')
        self.tts = TTS(
            model_name='tts_models/multilingual/multi-dataset/xtts_v2',
            progress_bar=True,
            gpu=torch.cuda.is_available()
        )

    def speak(self, text: str, output_path: str):
        self.tts.tts_to_file(
            text=text,
            speaker_wav='reference_hindi.wav',   # your 5–10 sec Hindi voice sample in project root
            language='hi',
            file_path=output_path
        )

# Global instance
tts = HindiTTS()
