# Command-line entry point
import argparse
import tempfile

from .capture import record_mic
from .asr import transcribe
from .summarize import summarize, keywords
from .memory import save_session, list_sessions

def main():
    p = argparse.ArgumentParser(description="FocusFlow: offline notes")
    p.add_argument("--input", required=True,
                   help="Path to a WAV/MP3 file, or 'mic' to record")
    p.add_argument("--seconds", type=int, default=30,
                   help="Mic recording length (default 30)")
    p.add_argument("--model", default="tiny",
                   help="Whisper model: tiny/base/small (default tiny)")
    args = p.parse_args()

#to BROWSE MEMORY from the terminal
    if args.input.lower() == "history":
        print("SAVED NOTES (focusflow.db)")
        print("-" * 50)
        for item in list_sessions():
            print("#%s  %s  [%s]  %s" % (item["id"], item["date"],
                                           item["source"], item["preview"]))
        return
    
    if args.input.lower() == "mic":
        audio = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
        record_mic(args.seconds, audio)
        source = "mic (%ds)" % args.seconds
    else:
        audio = args.input
        source= args.input

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

    #saved to memory
    save_session(source, transcript, summarize(transcript), kws)
    print("Saved to memory (focusflow.db). View with: python -m focusflow --input history")
    print("Everything ran locally. Nothing was sent to the cloud.")