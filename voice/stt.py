from faster_whisper import WhisperModel
import torch

class SpeechToText:
    def __init__(self):
        print("Loading Whisper large-v3 model... first time ???? 5-10 ????")
        self.model = WhisperModel(
            "large-v3",
            device="cuda" if torch.cuda.is_available() else "cpu",
            compute_type="float16" if torch.cuda.is_available() else "int8"
        )

    def transcribe(self, audio_path: str) -> str:
        segments, info = self.model.transcribe(
            audio_path,
            language="hi",
            beam_size=5,
            vad_filter=True
        )
        text = "".join(seg.text for seg in segments).strip()
        print(f"Language: {info.language} ({info.language_probability:.2f})")
        return text

stt = SpeechToText()
