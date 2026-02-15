# Mavada Technologies Water ATM Chat
**Powered by IMPERIAL ENTERPRISE**

## Vercel Deployment Structure
```
├── api/
│   └── index.py          ← FastAPI backend (serverless function)
├── public/
│   └── index.html         ← Chat frontend (static)
├── vercel.json            ← Routing config
├── requirements.txt       ← Python dependencies
└── .env.example           ← Environment variables template
```

## Deploy to Vercel
1. Push this folder to GitHub
2. Connect repo to [Vercel](https://vercel.com)  
3. Add environment variable: `OPENAI_API_KEY`
4. Deploy — your chat will be at the root URL `/`

## Local Development
```bash
pip install -r requirements.txt uvicorn
cd api && python index.py
# Then open public/index.html in browser
```

## Powered by IMPERIAL ENTERPRISE
