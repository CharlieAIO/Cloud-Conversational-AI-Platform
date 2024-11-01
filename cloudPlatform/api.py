from fastapi import FastAPI, UploadFile, HTTPException, Form, File
from dotenv import load_dotenv
from typing import Optional
import os

load_dotenv()

from .gcp import speech_to_text
from .chatgpt import query_gpt

tmp_file_dir = "/tmp/audio_files"
app = FastAPI()
os.makedirs(tmp_file_dir, exist_ok=True)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/query")
async def query(query: Optional[str] = Form(None), audioFile: Optional[UploadFile] = File(None)):
    if query:
        response = query_gpt(query)
        return {"response": response}
    elif audioFile:
        audio_file_path = os.path.join(tmp_file_dir, audioFile.filename)

        file_bytes = await audioFile.read()

        with open(audio_file_path, "wb") as file_out:
            file_out.write(file_bytes)

        transcript = speech_to_text(audio_file_path)

        os.remove(audio_file_path)
        return {"transcript": transcript}
    else:
        raise HTTPException(status_code=400, detail="No query or audio file provided")
