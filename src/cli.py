# Command-line entry point
import argparse
import tempfile

from .capture import record_mic
from .asr import transcribe
from .summarize import summarize, keywords


def main():
    p = argparse.ArgumentParser(description="LocalMind: offline notes MVP")
    p.add_argument("--input", required=True,
                   help="Path to a WAV/MP3 file, or 'mic' to record")
    p.add_argument("--seconds", type=int, default=30,
                   help="Mic recording length (default 30)")
    p.add_argument("--model", default="tiny",
                   help="Whisper model: tiny/base/small (default tiny)")
    args = p.parse_args()

    if args.input.lower() == "mic":
        audio = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
        record_mic(args.seconds, audio)
    else:
        audio = args.input

    print("Transcribing on-device...")
    transcript = transcribe(audio, args.model)

    print()
    print("TRANSCRIPT")
    print("-" * 50)
    print(transcript)

    print()
    print("SUMMARY")
    print("-" * 50)
    print(summarize(transcript))

    print()
    print("KEYWORDS: " + ", ".join(keywords(transcript)))
    print()
    print("Everything ran locally. Nothing was sent to the cloud.")