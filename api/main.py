from fastapi import FastAPI, Request
import requests

app = FastAPI()

# URL que viste en tu consola
BASE_URL = "https://notegpt.io/api/v1/ai-music"

@app.post("/api/generate")
async def generate_song(req: Request):
    body = await req.json()
    # Enviamos los datos a NoteGPT fingiendo ser un navegador real
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://notegpt.io/ai-music-generator",
        "Content-Type": "application/json"
    }
    r = requests.post(f"{BASE_URL}/generate", json=body, headers=headers)
    return r.json()

@app.get("/api/status")
async def get_status(conversation_id: str):
    # El polling que viste en tu consola
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(f"{BASE_URL}/status?conversation_id={conversation_id}", headers=headers)
    return r.json()