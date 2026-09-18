# Transcribe audio to text using faster-whisper (runs locally).
from faster_whisper import WhisperModel


def transcribe(audio_path, model_size="tiny"):
    # Return the full transcript of an audio file as a string.
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, _info = model.transcribe(audio_path)
    return " ".join(seg.text.strip() for seg in segments)