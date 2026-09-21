# FocusFlow — Private, Offline AI Notes for `Snapdragon HP PCs`

> Record → Transcribe → Summarize — entirely on your laptop.</br> 
> **No cloud. No API keys. No data ever leaves your device.**

FocusFlow is an AI meeting & study companion designed, developed, and optimized for  **Snapdragon-powered HP PCs**. It runs Whisper speech-to-text and extractive summarization fully on-device — perfect for flights, dead zones, classrooms, and confidential meetings where cloud AI simply isn't an option.

---

## Features

- **Record or upload audio** — browser mic recording (Web UI) or local files (CLI)
- **On-device transcription** — Whisper via `faster-whisper` (int8, CPU; NPU-ready)
- **Instant summaries & keywords** — zero-LLM extractive summarizer, works offline out of the box
- **Snapdragon NPU-ready** — the same code activates the 45 TOPS Hexagon NPU on Snapdragon X machines via ONNX Runtime + QNN
- **Battery-friendly** — int8 quantized inference keeps CPU load (and fan noise) low
- **Privacy by design** — no accounts, no telemetry, no network calls after first model download

## Quick Start (Windows)
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    
    pip install -r requirements.txt

    # Web app (recommended demo)
    uvicorn app:app --reload       # → open http://127.0.0.1:8000

    # CLI version
    python -m src --input mic --seconds 30
    python -m src --input meeting.wav

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

## Roadmap

- [x] MVP: offline transcription + summarization (CLI + web UI)
- [x] CPU vs NPU benchmark harness
- [x] NPU-accelerated Whisper via ONNX Runtime + QNN (`onnxruntime-qnn`)
- [ ] Battery-aware inference scheduling (batch when plugged in)
- [ ] Chat-with-your-notes using a local SLM (Phi-3-mini)
- [ ] WinUI 3 desktop app + MSIX packaging

## Contributing / Feedback

Built as a beginner-friendly submission for AI use-case development on Snapdragon HP PCs. Issues, forks, and demo videos welcome!
