from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
import time

app = FastAPI()

# Usamos la URL v2 que confirmaste en tus pruebas anteriores
URL_GENERATE = "https://notegpt.io/api/v2/music/generate"

@app.post("/api/generate")
async def generate_song(req: Request):
    try:
        user_input = await req.json()
        
        # Estas son las cookies que extrajimos de tu lista
        # Asegúrate de que estos valores coincidan con los que copiaste
        zfsessid = "i77j4ci4nhrhc4rqhuv8ja0kp3"
        csrf = "LnuMGh4ApcJCmlSPNRaOohkIBlUT24o85pqBwsvYq79MLuZKNJJdlWFSXefWjKkW"

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Cookie": f"ZFSESSID={zfsessid}; csrftoken={csrf}",
            "X-Csrftoken": csrf,
            "Origin": "https://notegpt.io",
            "Referer": "https://notegpt.io/ai-music-generator"
        }

        payload = {
            "prompt": user_input.get("prompt"),
            "lyrics": user_input.get("lyrics"),
            "custom_mode": True,
            "instrumental": False,
            "model": "suno-v3.5"
        }

        # Realizamos la petición y capturamos la respuesta real
        response = requests.post(URL_GENERATE, json=payload, headers=headers, timeout=25)
        
        # Si NoteGPT nos da error, lo enviamos al frontend para saber qué pasó
        if response.status_code != 200:
            return JSONResponse(
                status_code=response.status_code, 
                content={"success": False, "error": f"NoteGPT Error: {response.text}"}
            )
            
        return response.json()

    except Exception as e:
        # Esto evita el error de "Unexpected token 'I'" al devolver un JSON real
        return JSONResponse(
            status_code=500, 
            content={"success": False, "error": str(e)}
        )
