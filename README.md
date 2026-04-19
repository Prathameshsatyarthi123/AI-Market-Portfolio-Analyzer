# 🇮🇳 AI-Powered Indian Stock Portfolio Analyzer

> Upload your broker's holdings statement and get instant AI-powered analysis, sector breakdown, and actionable buy/hold/exit suggestions — tailored specifically for the Indian stock market.

![Stack](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi)
![Stack](https://img.shields.io/badge/AI-Groq%20LLaMA%203.3%2070B-FF6B35?style=flat-square)
![Stack](https://img.shields.io/badge/Frontend-React-61DAFB?style=flat-square&logo=react)
![Stack](https://img.shields.io/badge/Cloud-AWS%20EC2-FF9900?style=flat-square&logo=amazonaws)

---

## 📸 What It Does

1. **Upload** your broker's `.xlsx` holdings statement
2. **View** your P&L chart — green/red per stock at a glance
3. **Get AI analysis** — sector concentration, risk flags, stock-wise recommendations
4. **Act** — concrete buy/hold/exit suggestions based on Indian market context

---

## 📥 How to Download Your Holdings Statement (.xlsx)

### From Groww
1. Open the **Groww app** on your phone
2. Tap your **Profile icon** (bottom right)
3. Go to **Holdings**
4. Scroll down and tap **Holdings Statement**
5. Select date range and tap **Download**
6. A `.xlsx` file will be saved to your phone/downloads

### From Zerodha (Kite)
1. Login to **console.zerodha.com**
2. Go to **Portfolio → Holdings**
3. Click the **download icon** (top right)
4. Download as `.xlsx`

### From Upstox
1. Login to **upstox.com**
2. Go to **Portfolio → Holdings**
3. Click **Download** → select Excel format

### From Angel One
1. Login to **angelone.in**
2. Go to **Portfolio → My Holdings**
3. Click **Export** → Excel

> ✅ The app supports the standard holdings export format from all major Indian brokers.

---

## ✨ Features

- 📂 Upload `.xlsx` holdings statement directly in the browser
- 📊 Visual P&L bar chart per stock (green = profit, red = loss)
- 🤖 AI analysis powered by **Groq LLaMA 3.3 70B**
- 🏷️ Stock-wise **Hold / Accumulate / Exit** recommendations
- 🏦 Sector concentration analysis (PSU, Banking, IT, Pharma etc.)
- ⚠️ Risk flags specific to NSE/BSE listed stocks
- 💡 Suggestions for stocks to complement your portfolio
- 🇮🇳 All advice tailored to **Indian market, SEBI regulations, NSE/BSE**

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React + Recharts | UI, file upload, P&L charts |
| Backend | FastAPI (Python) | REST API, file parsing |
| AI Model | Groq API — LLaMA 3.3 70B | Portfolio analysis & suggestions |
| File Parsing | pandas + openpyxl | Read `.xlsx` holdings file |
| Server | AWS EC2 (Amazon Linux) | Hosting |
| Process Manager | systemd + uvicorn | Keep backend running 24/7 |

---

## 🚀 Setup & Deployment

### Prerequisites
- AWS EC2 instance (Amazon Linux, t2.micro free tier works)
- Python 3.9+
- Node.js 20+
- Groq API key — get one free at [console.groq.com](https://console.groq.com)

---

### Step 1 — Clone the repo

```bash
git clone https://github.com/Prathameshsatyarthi123/AI-Market-Portfolio-Analyzer.git
cd AI-Market-Portfolio-Analyzer
```

### Step 2 — Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cat > .env << 'EOF'
GROQ_API_KEY=your_groq_api_key_here
EOF
```

### Step 3 — Run the Backend

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Verify it's running:
```bash
curl http://localhost:8000/health
# Expected: {"status":"ok"}
```

### Step 4 — Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Update API URL in src/App.js
# Change YOUR_EC2_PUBLIC_IP to your actual EC2 public IP
nano src/App.js

# Build
npm run build
```

### Step 5 — Serve the Frontend

```bash
cd build
python3 -m http.server 3000
```

### Step 6 — Access the App

Open your browser and go to:
```
http://YOUR_EC2_PUBLIC_IP:3000
```

---

## ⚙️ Running as a Background Service (systemd)

So the backend keeps running after you close the terminal:

```bash
sudo cat > /etc/systemd/system/portfolio-api.service << 'EOF'
[Unit]
Description=Portfolio Analyzer API
After=network.target

[Service]
User=root
WorkingDirectory=/root/AI-Market-Portfolio-Analyzer/backend
Environment="PATH=/root/AI-Market-Portfolio-Analyzer/backend/venv/bin"
EnvironmentFile=/root/AI-Market-Portfolio-Analyzer/backend/.env
ExecStart=/root/AI-Market-Portfolio-Analyzer/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable portfolio-api
sudo systemctl start portfolio-api
```

---

## 🔒 AWS EC2 Security Group — Required Ports

| Port | Purpose |
|------|---------|
| 22 | SSH |
| 3000 | React Frontend |
| 8000 | FastAPI Backend |

---

## 📁 Project Structure

```
AI-Market-Portfolio-Analyzer/
├── backend/
│   ├── main.py              # FastAPI app, Groq integration, xlsx parsing
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # GROQ_API_KEY (never commit this)
├── frontend/
│   ├── src/
│   │   └── App.js           # React UI, charts, file upload
│   └── package.json
├── .gitignore
└── README.md
```

---

## 🔑 Environment Variables

Create `backend/.env` with:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key at [console.groq.com](https://console.groq.com) → API Keys → Create API Key

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

---

## 🐛 Common Issues & Fixes

| Problem | Fix |
|---------|-----|
| `Failed to load environment files` | Check `.env` exists at `backend/.env` |
| `500 Internal Server Error` on frontend | Copy build to `/var/www/` or skip Nginx, use `python3 -m http.server` |
| Service keeps restarting | Run `uvicorn` manually to see actual error |
| `error: src refspec main does not match` | You haven't committed yet — run `git add . && git commit` first |
| Groq API error | Verify API key in `.env` has no extra spaces |

---

## 📝 Blog Post

Read the full build story on Medium:
[I Built an AI-Powered Indian Stock Portfolio Analyzer Using Groq, FastAPI & AWS EC2](#)

---

## 🙌 Author

**Prathamesh Rajiv Satyarthi**
- GitHub: [@Prathameshsatyarthi123](https://github.com/Prathameshsatyarthi123)

---

## ⭐ If this helped you, give it a star on GitHub!
