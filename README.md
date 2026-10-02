# FocusFlow — Private, Offline AI Notes for `Snapdragon HP PCs`

> Record → Transcribe → Summarize — entirely on your laptop.</br> 
> **No cloud. No API keys. No data ever leaves your device.**

FocusFlow is an AI meeting & study companion designed, developed, and optimized for  **Snapdragon-powered HP PCs**. It runs Whisper speech-to-text and extractive summarization fully on-device — perfect for flights, dead zones, classrooms, and confidential meetings where cloud AI simply isn't an option.

---

## Features

- **Record or upload audio** — browser mic recording (Web UI) or local files (CLI)
- Process audio locally for privacy-focused, offline-first note creation.
- **On-device transcription** — Whisper via `faster-whisper` (int8, CPU; NPU-ready)
- Choose between Tiny, Base, and Small transcription models based on speed and accuracy requirements.
- **Instant summaries & keywords** — zero-LLM extractive summarizer, works offline out of the box
- Save processed notes in local history.
- Reopen previous notes to review transcripts, summaries, and keywords.
- Display note metadata including source, date, ID, and preview text.
- **Snapdragon NPU-ready** — the same code activates the 45 TOPS Hexagon NPU on Snapdragon X machines via ONNX Runtime + QNN
- **Battery-friendly** — int8 quantized inference keeps CPU load (and fan noise) low
- **Privacy by design** — no accounts, no telemetry, no network calls after first model download
- Show live recording, processing, success, and error status messages.

## Quick Start (Windows)
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    
    pip install -r requirements.txt

    # Web app (recommended demo)
    uvicorn app:app --reload       # → open http://127.0.0.1:8000

    # CLI version
    python -m src --input mic --seconds 30
    python -m src --input meeting.wav

    python -m focusflow --input history     # browse all saved notes in terminal

> **First run** downloads the Whisper `tiny` model (~75 MB) from Hugging Face. Everything works offline after that.

## Project Structure

    FocusFlow/
    ├── app.py                  # FastAPI backend (serves API + frontend)
    ├── static/
    │   └── index.html          # Browser UI (record / upload / results)
    ├── scripts/
    │   └── npu.py              # CPU vs Snapdragon NPU benchmark
    ├── src/                    # Core package
    │   ├── cli.py              # Command-line entry point
    │   ├── capture.py          # Microphone recording
    │   ├── asr.py              # Whisper transcription
    │   └── summarize.py        # Extractive summary + keywords
    ├── requirements.txt
    └── README.md

> The benchmark degrades gracefully: on non-Snapdragon machines it reports the CPU numbers and a clear "QNN EP not found" message instead of crashing — **the same script lights up the NPU on Snapdragon HP PCs with zero code changes.**

## Snapshot
<p float="left">
<img width="50%" alt="Screenshot 2026-09-30 233122" src="https://github.com/user-attachments/assets/054af5fd-1b56-4033-ac74-24b8765f9054" />

<img width="49%" alt="Screenshot 2026-09-30 233150" src="https://github.com/user-attachments/assets/0400e914-5de8-4413-a48a-b29538803fd3" />
</p>

## Roadmap

- [x] MVP: offline transcription + summarization (CLI + web UI)
- [x] CPU vs NPU benchmark harness
- [x] NPU-accelerated Whisper via ONNX Runtime + QNN (`onnxruntime-qnn`)
- [x] Notes stored locally in focusflow.db (Searchable history on the device)
- [ ] Battery-aware inference scheduling (batch when plugged in)
- [ ] Chat-with-your-notes using a local SLM (Phi-3-mini)
- [ ] WinUI 3 desktop app + MSIX packaging

## Contributing / Feedback

Built as a beginner-friendly submission for AI use-case development on Snapdragon HP PCs. Issues, forks, and demo videos welcome!
