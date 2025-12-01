from fastapi import HTTPException, UploadFile
from dotenv import load_dotenv
from ollama import Client
import os

load_dotenv()
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "50"))

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_TEXT_MODEL = os.getenv("OLLAMA_TEXT_MODEL", "llama3")
ollama_client = Client(host=OLLAMA_HOST)


async def save_upload(file: UploadFile, dest_folder: str) -> str:
    os.makedirs(dest_folder, exist_ok=True)
    fname = file.filename
    contents = await file.read()
    size_mb = len(contents) / (1024*1024)
    if size_mb > MAX_UPLOAD_MB:
        raise HTTPException(status_code=413, detail="File too large")
    path = os.path.join(dest_folder, fname)
    with open(path, "wb") as f:
        f.write(contents)
    return path


async def call_ollama(prompt: str) -> dict:
    """
    Calls Ollama via the Python client.
    Requires the Ollama daemon to be running locally.
    """
    try:
        response = ollama_client.chat(
            model=OLLAMA_TEXT_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.get("message", {}).get("content", "").strip()
        return {"text": text or prompt, "image_url": ""}
    except Exception as e:
        print("Ollama call failed:", e)
        return {"text": prompt, "image_url": ""}