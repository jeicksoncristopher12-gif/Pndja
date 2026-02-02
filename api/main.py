from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
import time

app = FastAPI()

# La nueva URL que encontraste en la consola
GENERATE_URL = "https://notegpt.io/api/v2/music/generate"
STATUS_URL = "https://notegpt.io/api/v2/music/status"

@app.post("/api/generate")
async def generate_song(req: Request):
    try:
        # Recibimos los datos de tu index.html
        user_data = await req.json()
        
        # Disfrazamos la petición para que NoteGPT crea que viene de su propia web
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Origin": "https://notegpt.io",
            "Referer": "https://notegpt.io/ai-music-generator",
            "Accept": "application/json, text/plain, */*"
        }

        # Estructura de datos que NoteGPT v2 espera
        payload = {
            "prompt": user_data.get("prompt", ""),
            "lyrics": user_data.get("lyrics", ""),
            "custom_mode": True,
            "instrumental": False,
            "model": "suno-v3.5" # O el modelo que viste en la consola
        }

        # Enviamos la petición a NoteGPT
        response = requests.post(GENERATE_URL, json=payload, headers=headers, timeout=20)
        
        # Si NoteGPT responde bien, devolvemos su respuesta (que contiene el id)
        if response.status_code == 200:
            return response.json()
        else:
            return JSONResponse(
                status_code=response.status_code, 
                content={"success": False, "error": f"Error de NoteGPT: {response.text}"}
            )

    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

@app.get("/api/status")
async def get_status(conversation_id: str):
    try:
        # El polling para revisar si la canción ya está lista
        params = {"conversation_id": conversation_id}
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://notegpt.io/ai-music-generator"
        }
        
        response = requests.get(STATUS_URL, params=params, headers=headers, timeout=10)
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}
