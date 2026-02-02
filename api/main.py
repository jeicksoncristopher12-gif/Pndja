from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

# URL de la API v2 que confirmamos antes
URL_GENERATE = "https://notegpt.io/api/v2/music/generate"
URL_STATUS = "https://notegpt.io/api/v2/music/status"

# Estos valores los saqué de tu lista de cookies
ZFSESSID = "i77j4ci4nhrhc4rqhuv8ja0kp3"
CSRF_TOKEN = "LnuMGh4ApcJCmlSPNRaOohkIBlUT24o85pqBwsvYq79MLuZKNJJdlWFSXefWjKkW"

@app.post("/api/generate")
async def generate_song(req: Request):
    try:
        user_input = await req.json()
        
        # Construimos la cookie combinando tus datos
        mi_cookie = f"ZFSESSID={ZFSESSID}; csrftoken={CSRF_TOKEN}; is_first_visit=true"

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Cookie": mi_cookie,
            "X-Csrftoken": CSRF_TOKEN, # Algunos sistemas Django lo piden por separado
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

        response = requests.post(URL_GENERATE, json=payload, headers=headers, timeout=25)
        
        # Si la respuesta es exitosa, devolvemos el JSON de NoteGPT
        return response.json()

    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

@app.get("/api/status")
async def get_status(conversation_id: str):
    headers = {
        "Cookie": f"ZFSESSID={ZFSESSID}",
        "User-Agent": "Mozilla/5.0"
    }
    try:
        r = requests.get(URL_STATUS, params={"conversation_id": conversation_id}, headers=headers, timeout=15)
        return r.json()
    except Exception as e:
        return {"success": False, "error": str(e)}
