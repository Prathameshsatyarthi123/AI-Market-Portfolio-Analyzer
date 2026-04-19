# 🇮🇳 Indian Stock Portfolio Analyzer

AI-powered portfolio analysis tool for Indian stock market investors.

## Features
- Upload broker holdings statement (.xlsx)
- Automatic P&L analysis
- Sector breakdown
- AI suggestions powered by Groq (LLaMA 3.3 70B)
- Built for NSE/BSE listed stocks

## Tech Stack
- **Frontend:** React, Recharts
- **Backend:** FastAPI, Python
- **AI:** Groq API (LLaMA 3.3 70B)
- **Infrastructure:** AWS EC2 (Amazon Linux)

## Setup

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run build
cd build && python3 -m http.server 3000
```

## Environment Variables
Create `backend/.env`:
