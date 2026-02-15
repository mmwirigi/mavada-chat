# Mavada Technologies Water ATM Chat
**Powered by IMPERIAL ENTERPRISE**

## Structure
```
api/
  index.py      ← FastAPI (serves HTML on GET /, chat on POST /)
  chat.html     ← Chat frontend (served by FastAPI)
vercel.json     ← Routes all requests to FastAPI
requirements.txt
```

## Deploy to Vercel
1. Push to GitHub → Connect to Vercel
2. Add `OPENAI_API_KEY` environment variable
3. Deploy — visit your URL!

## Powered by IMPERIAL ENTERPRISE
