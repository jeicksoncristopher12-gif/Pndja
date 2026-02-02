from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

# La URL real que usa el motor de NoteGPT (Suno)
TARGET_URL = "https://notegpt.io/api/v1/ai-music"

@app.post("/api/generate")
async def generate_song(req: Request):
    try:
        body = await req.json()
        
        # DISFRAZ MEJORADO
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Origin": "https://notegpt.io",
            "Referer": "https://notegpt.io/ai-music-generator"
        }

        # Intentamos conectar con NoteGPT
        r = requests.post(f"{TARGET_URL}/generate", json=body, headers=headers, timeout=15)
        
        # Si NoteGPT nos rechaza (401 o 403), devolvemos un mensaje claro
        if r.status_code != 200:
            return JSONResponse(status_code=r.status_code, content={"success": False, "error": f"NoteGPT rechazó la petición: {r.status_code}"})
            
        return r.json()
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

@app.get("/api/status")
async def get_status(conversation_id: str):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://notegpt.io/ai-music-generator"
        }
        r = requests.get(f"{TARGET_URL}/status?conversation_id={conversation_id}", headers=headers, timeout=10)
        return r.json()
    except Exception as e:
        return {"success": False, "error": str(e)}
