from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def parse_portfolio_xlsx(file_bytes):
    df = pd.read_excel(io.BytesIO(file_bytes), header=None)
    
    # Extract summary (rows 6-8 based on your sample format)
    invested = float(df.iloc[6, 1])
    closing = float(df.iloc[7, 1])
    unrealised_pnl = float(df.iloc[8, 1])
    
    # Extract holdings (row 10 is header, data from row 11)
    holdings_df = df.iloc[10:].copy()
    holdings_df.columns = df.iloc[10].tolist()
    holdings_df = holdings_df.iloc[1:].dropna(subset=["Stock Name"])
    holdings_df = holdings_df.reset_index(drop=True)
    
    holdings = []
    for _, row in holdings_df.iterrows():
        holdings.append({
            "stock_name": str(row["Stock Name"]),
            "isin": str(row["ISIN"]),
            "quantity": int(row["Quantity"]),
            "avg_buy_price": float(row["Average buy price"]),
            "buy_value": float(row["Buy value"]),
            "closing_price": float(row["Closing price"]),
            "closing_value": float(row["Closing value"]),
            "unrealised_pnl": float(row["Unrealised P&L"]),
            "pnl_percent": round((float(row["Unrealised P&L"]) / float(row["Buy value"])) * 100, 2)
        })
    
    return {
        "summary": {
            "invested_value": invested,
            "closing_value": closing,
            "unrealised_pnl": unrealised_pnl,
            "total_pnl_percent": round((unrealised_pnl / invested) * 100, 2)
        },
        "holdings": holdings
    }

def build_prompt(portfolio_data):
    holdings_text = "\n".join([
        f"- {h['stock_name']}: Qty {h['quantity']}, Avg Buy ₹{h['avg_buy_price']}, "
        f"Current ₹{h['closing_price']}, P&L ₹{h['unrealised_pnl']} ({h['pnl_percent']}%)"
        for h in portfolio_data["holdings"]
    ])
    
    summary = portfolio_data["summary"]
    
    return f"""You are an expert Indian stock market portfolio advisor with deep knowledge of NSE/BSE listed companies, Indian sectors, SEBI regulations, and current market trends.

Analyze this Indian investor's portfolio and provide detailed, actionable suggestions:

PORTFOLIO SUMMARY:
- Total Invested: ₹{summary['invested_value']:,.2f}
- Current Value: ₹{summary['closing_value']:,.2f}  
- Unrealised P&L: ₹{summary['unrealised_pnl']:,.2f} ({summary['total_pnl_percent']}%)

HOLDINGS:
{holdings_text}

Please provide a comprehensive analysis covering:
1. **Portfolio Health Assessment** - Overall portfolio quality and risk level
2. **Top Performers & Laggards** - Which stocks are doing well vs poorly
3. **Sector Analysis** - Sector concentration and diversification gaps
4. **Stock-wise Recommendations** - Hold / Accumulate / Exit suggestions with reasoning
5. **Risk Factors** - Key risks specific to these holdings in Indian market context
6. **Actionable Steps** - 3-5 concrete next steps the investor should take
7. **Stocks to Watch** - 2-3 Indian stocks that could complement this portfolio

Keep suggestions practical and specific to Indian market conditions, SEBI regulations, and NSE/BSE listed companies."""

@app.post("/analyze")
async def analyze_portfolio(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        portfolio_data = parse_portfolio_xlsx(contents)
        
        prompt = build_prompt(portfolio_data)
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            max_tokens=2000,
            temperature=0.7
        )
        
        analysis = chat_completion.choices[0].message.content
        
        return {
            "portfolio": portfolio_data,
            "analysis": analysis,
            "status": "success"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/health")
def health():
    return {"status": "ok"}
