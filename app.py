# FocusFlow backend - serves the API + frontend.

import tempfile
import os

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.asr import transcribe
from src.summarize import summarize, keywords
from src.memory import save_session, list_sessions, get_session

app = FastAPI(title="FocusFlow")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.post("/api/process")
async def process(file: UploadFile = File(...), model: str = Form("tiny")):
    # Save the uploaded audio, transcribe + summarize, store in memory return JSON.
    suffix = os.path.splitext(file.filename or "audio.webm")[1] or ".wav"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(await file.read())
        path = tmp.name
    transcript = transcribe(path, model)
    s= summarize(transcript)
    k= keywords(transcript)
    save_session(file.filename or "mic", transcript, s, k)
    return {
        "transcript": transcript,
        "summary": s,
        "keywords": k,
    }

@app.get("/api/history")
def history():
    # Recent saved notes.
    return {"sessions": list_sessions()}


@app.get("/api/history/{session_id}")
def history_item(session_id: int):
    # One full note.
    item = get_session(session_id)
    if item is None:
        return {"error": "not found"}
    return item