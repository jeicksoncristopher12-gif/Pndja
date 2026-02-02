from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

# Las rutas exactas que encontraste en el Django REST Framework
URL_GENERATE = "https://notegpt.io/api/v2/music/generate"
URL_STATUS = "https://notegpt.io/api/v2/music/status"

@app.post("/api/generate")
async def generate_song(req: Request):
    try:
        data = await req.json()
        
        # Copiamos el comportamiento del botón POST que viste en pantalla
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Origin": "https://notegpt.io",
            "Referer": "https://notegpt.io/ai-music-generator"
        }

        # Estructura para la v2
        payload = {
            "prompt": data.get("prompt"),
            "lyrics": data.get("lyrics"),
            "custom_mode": True,
            "instrumental": False,
            "model": "suno-v3.5"
        }

        # Disparamos el POST
        response = requests.post(URL_GENERATE, json=payload, headers=headers, timeout=20)
        
        # Si la respuesta es 201 o 200, NoteGPT aceptó la creación
        return response.json()

    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

@app.get("/api/status")
async def get_status(conversation_id: str):
    try:
        # El polling para la v2
        headers = {"User-Agent": "Mozilla/5.0"}
        params = {"conversation_id": conversation_id}
        
        r = requests.get(URL_STATUS, params=params, headers=headers, timeout=10)
        return r.json()
    except Exception as e:
        return {"success": False, "error": str(e)}
