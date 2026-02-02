from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
import time # Necesario para el timestamp

app = FastAPI()

URL_GENERATE = "https://notegpt.io/api/v2/music/generate"

@app.post("/api/generate")
async def generate_song(req: Request):
    try:
        user_input = await req.json()
        
        # Generamos el timestamp que NoteGPT espera (en milisegundos)
        ts = int(time.time() * 1000)

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Cookie": "ZFSESSID=i77j4ci4nhrhc4rqhuv8ja0kp3; csrftoken=LnuMGh4ApcJCmlSPNRaOohkIBlUT24o85pqBwsvYq79MLuZKNJJdlWFSXefWjKkW",
            "X-Csrftoken": "LnuMGh4ApcJCmlSPNRaOohkIBlUT24o85pqBwsvYq79MLuZKNJJdlWFSXefWjKkW",
            "Origin": "https://notegpt.io",
            "Referer": "https://notegpt.io/ai-music-generator"
        }

        # Intentamos enviar con los datos de tiempo
        payload = {
            "prompt": user_input.get("prompt"),
            "lyrics": user_input.get("lyrics"),
            "custom_mode": True,
            "instrumental": False,
            "model": "suno-v3.5",
            "timestamp": ts # Añadimos el tiempo actual
        }

        response = requests.post(URL_GENERATE, json=payload, headers=headers, timeout=25)
        
        # Si NoteGPT responde con error, queremos ver EXACTAMENTE qué dice
        if response.status_code != 200:
            return JSONResponse(status_code=response.status_code, content=response.json())
            
        return response.json()

    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})
