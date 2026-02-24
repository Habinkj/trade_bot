# 📈 Semi-Automated Trading Bot using Zerodha API

## 🔹 Project Overview
This project is a **semi-automated stock trading application** built using **FastAPI** and **Zerodha Kite API**.  
The system scans selected stocks using **technical indicators** and generates BUY signals.  
Trades are executed **only after user approval**, ensuring safety and transparency.

The goal of this project is **academic learning and system design**, not guaranteed profits.

---

## 🔹 Key Features
- 🔍 Market scanning using SMA / EMA strategies
- 📊 Real-time balance fetching from Zerodha
- ✅ Manual trade approval (Human-in-the-loop)
- 🔐 Price range validation (Min & Max Buy Price)
- 💰 Balance validation before placing orders
- 🌐 Web-based frontend (HTML + JavaScript)
- 🔗 Real broker integration using Zerodha API

---

## 🔹 Why Semi-Automated?
- Fully automated bots are risky and unsafe
- Human approval prevents emotional and blind trading
- Academically ethical and review-safe design

---

## 🔹 System Architecture
User (Browser)
     ↓
Frontend (HTML + JS)
     ↓
FastAPI Backend
     ↓
Strategy Engine
     ↓
Zerodha Kite API
     ↓
Live Market & Orders

---

## 🔹 Technology Stack
| Layer | Technology |
|------|-----------|
| Backend | Python, FastAPI |
| Broker API | Zerodha KiteConnect |
| Frontend | HTML, CSS, JavaScript |
| Server | Uvicorn |
| Indicators | SMA, EMA |

---

## 🔹 Trading Strategies Used
- SMA 5–10 crossover
- SMA 9–21 crossover
- SMA 15–20 crossover
- EMA crossover

These strategies generate **BUY signals** based on trend direction.

---

## 🔹 How the System Works
1. User logs in using Zerodha
2. System fetches historical market data
3. Technical strategy is applied
4. BUY signals are generated
5. User enters:
   - Quantity
   - Minimum Buy Price
   - Maximum Buy Price
6. System validates:
   - Available balance
   - Price range
7. Order is placed through Zerodha API

---

## 🔹 Safety Mechanisms
- No automatic trades
- User approval required
- Balance check before trade
- Price range validation
- No leverage trading

---

## 🔹 Accuracy
- Expected accuracy: **50–60%**
- This is realistic for technical indicators
- Project focuses on **correct methodology**, not exaggerated accuracy

---

## 🔹 Project Structure

```text
trade_bot/
├── backend/
│   ├── main.py
│   ├── api.py
│   ├── strategy.py
│   ├── zerodha_session.py
│   ├── data_provider.py
│   └── config_loader.py
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── config/
│   └── watchlist.json
├── logs/
├── requirements.txt
└── README.md
```
---

## 🔹 How to Run the Project

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 2️⃣ Set Environment Variables
```
KITE_API_KEY=your_api_key
KITE_API_SECRET=your_api_secret
```

### 3️⃣ Start Backend Server
```
python -m uvicorn backend.main:app --reload
```

### 4️⃣ Open Frontend
```
Open frontend/index.html in your browser.
```
---
## 🔹 Limitations
	•	No auto-sell logic yet
	•	SMA/EMA do not work well in sideways markets
	•	Requires Zerodha login session
	•	Intraday only (no long-term strategies)
---
⸻

## 🔹 Future Enhancements
	•	Auto sell with stop-loss & target
	•	Trailing stop-loss
	•	Volatility filter (ATR)
	•	Trend strength filter (ADX)
	•	Multi-stock portfolio support
	•	Advanced charts and analytics
---
⸻

## 🔹 Academic Declaration

This project is developed for educational purposes only.
It does not guarantee profits and follows ethical trading practices.
---
⸻

## 🔹 References
	•	Zerodha Kite API Documentation
	•	FastAPI Documentation
	•	Technical Analysis of Financial Markets – John J. Murphy

---
