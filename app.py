# FocusFlow backend - serves the API + frontend.

import tempfile
import os

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.asr import transcribe
from src.summarize import summarize, keywords

app = FastAPI(title="FocusFlow")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.post("/api/process")
async def process(file: UploadFile = File(...), model: str = Form("tiny")):
    # Save the uploaded audio, transcribe + summarize, return JSON.
    suffix = os.path.splitext(file.filename or "audio.webm")[1] or ".wav"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(await file.read())
        path = tmp.name
    transcript = transcribe(path, model)
    return {
        "transcript": transcript,
        "summary": summarize(transcript),
        "keywords": keywords(transcript),
    }