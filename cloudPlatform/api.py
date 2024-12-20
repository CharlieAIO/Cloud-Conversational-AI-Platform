import uuid

from fastapi import FastAPI, UploadFile, HTTPException, Form, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from typing import Optional
import os

load_dotenv()

from .gcp import speech_to_text, text_to_speech
from .chatgpt import query_gpt

tmp_file_dir = "/tmp/audio_files"
app = FastAPI()
os.makedirs(tmp_file_dir, exist_ok=True)

# Allow all origins, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/query")
async def query(query: Optional[str] = Form(None), audioFile: Optional[UploadFile] = File(None)):
    if query:
        response = query_gpt(query)
        if not response:
            raise HTTPException(status_code=400, detail="Error querying GPT")
        return {"response": response}
    elif audioFile:
        audio_file_path = os.path.join(tmp_file_dir, audioFile.filename)

        file_bytes = await audioFile.read()

        with open(audio_file_path, "wb") as file_out:
            file_out.write(file_bytes)

        transcript = speech_to_text(audio_file_path)
        if not transcript:
            raise HTTPException(status_code=400, detail="Error transcribing audio")
        response = query_gpt(transcript)
        if not response:
            raise HTTPException(status_code=400, detail="Error querying GPT")

        os.remove(audio_file_path)
        return {"response": response}
    else:
        raise HTTPException(status_code=400, detail="No input provided")



@app.post("/text-to-speech")
async def tts(textInput: str = Form(...)):
    if textInput:
        random_id = str(uuid.uuid4())
        output_file = os.path.join(tmp_file_dir, f"{random_id}.mp3")
        response = text_to_speech(textInput, output_file)
        if not response:
            raise HTTPException(status_code=400, detail="Error synthesizing speech")
    
        return FileResponse(output_file, media_type='audio/mpeg', filename=f"{random_id}.mp3")
    
    raise HTTPException(status_code=400, detail="No input provided")