# Mavada Technologies Chat API — Powered by IMPERIAL ENTERPRISE
# This is a lightweight proxy that calls the CodeWords chat service

import os
import json
import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path

app = FastAPI(title="Mavada Technologies Chat - Powered by IMPERIAL ENTERPRISE")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

CODEWORDS_API_KEY = os.environ.get("CODEWORDS_API_KEY", "")
CODEWORDS_SERVICE_ID = "mavada_chat_api_b4abe1f3"
CODEWORDS_BASE_URL = "https://runtime.codewords.ai"

# Cache the HTML
_html_cache = None

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """Serve the chat UI."""
    global _html_cache
    if _html_cache is None:
        html_path = Path(__file__).parent / "chat.html"
        if html_path.exists():
            _html_cache = html_path.read_text()
        else:
            _html_cache = "<h1>Mavada Technologies Chat</h1><p>UI not found.</p>"
    return HTMLResponse(content=_html_cache)


@app.post("/")
async def chat(request: Request):
    """Proxy chat requests to the CodeWords service."""
    body = await request.json()

    if not CODEWORDS_API_KEY:
        return JSONResponse(
            content={"success": False, "response": "Chat service not configured. Please WhatsApp us at 0758 281922!", "blog_links": [], "session_id": "", "show_agent_option": False},
            status_code=200
        )

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{CODEWORDS_BASE_URL}/run/{CODEWORDS_SERVICE_ID}/",
                headers={
                    "Authorization": f"Bearer {CODEWORDS_API_KEY}",
                    "Content-Type": "application/json"
                },
                json=body
            )

            if response.status_code == 200:
                return JSONResponse(content=response.json())
            else:
                return JSONResponse(
                    content={"success": False, "response": "Our chat is temporarily busy. Please WhatsApp us at 0758 281922 for instant help! 💬", "blog_links": [], "session_id": "", "show_agent_option": True},
                    status_code=200
                )

    except Exception as e:
        return JSONResponse(
            content={"success": False, "response": "Connection issue. Please WhatsApp us at 0758 281922 for instant help! 💬", "blog_links": [], "session_id": "", "show_agent_option": True},
            status_code=200
        )


@app.post("/submit_lead")
async def submit_lead(request: Request):
    """Proxy lead submissions to CodeWords."""
    body = await request.json()

    if not CODEWORDS_API_KEY:
        return JSONResponse(content={"success": True, "message": "Thank you! Call us at 0758 281922."})

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{CODEWORDS_BASE_URL}/run/{CODEWORDS_SERVICE_ID}/submit_lead",
                headers={
                    "Authorization": f"Bearer {CODEWORDS_API_KEY}",
                    "Content-Type": "application/json"
                },
                json=body
            )
            if response.status_code == 200:
                return JSONResponse(content=response.json())
    except:
        pass

    return JSONResponse(content={"success": True, "message": "Thank you! Our team will contact you. Call 0758 281922."})


@app.get("/health")
async def health():
    return {"status": "ok", "service": "Mavada Chat Proxy", "powered_by": "IMPERIAL ENTERPRISE"}


# For local dev
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
