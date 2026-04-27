# 📈 TRADEBOT: An Automated Algorithmic Trading Framework utilizing Multi-Indicator Technical Filters

## 🔹 Project Overview
[cite_start]This project is an **intelligent Human-in-the-Loop (HITL) trading framework** built using **FastAPI** and the **Zerodha Kite API**[cite: 15, 64]. [cite_start]The system performs automated market analysis using multi-indicator technical filters to generate high-probability BUY signals[cite: 16, 37]. 

[cite_start]To ensure safety, transparency, and ethical compliance, trades are executed **only after explicit user approval**[cite: 17, 21]. [cite_start]The goal of this project is to explore the intersection of **Intelligent Computing and financial risk management**[cite: 15, 33].

---

## 🔹 Key Features
- [cite_start]🔍 **Intelligent Scanning**: Market analysis using Supertrend and SMA/EMA crossover strategies[cite: 16, 39, 112].
- [cite_start]🛡️ **Momentum Gatekeeper**: Integrated ADX filter ($>25$) to ensure entries only during strong trends[cite: 55, 113, 132].
- [cite_start]📊 **Real-time Telemetry**: A responsive CSS Grid dashboard providing live balance and trade updates[cite: 35, 125, 127].
- [cite_start]✅ **HITL Approval**: Manual verification for all orders to mitigate algorithmic risk[cite: 17, 19, 134].
- [cite_start]🔐 **Risk Protocols**: Automated 2% trailing stop-loss and 6-day time-exit conditions[cite: 28, 59, 109].
- [cite_start]💰 **Balance Validation**: Real-time margin checking through the Zerodha Kite Connect bridge[cite: 67, 128].

---

## 🔹 Why Human-in-the-Loop (HITL)?
- [cite_start]Fully automated systems can lead to significant capital erosion due to "black-box" failures[cite: 20, 23, 34].
- [cite_start]Human approval acts as a psychological safety net, preventing emotional or blind trading[cite: 24, 29].
- [cite_start]The "Glass Box" design allows users to monitor and intervene during anomalous market events[cite: 35, 134].

---

## 🔹 System Architecture
**User (Browser)**      ↓  
[cite_start]**Frontend (Vanilla JS + CSS Grid)** — *10s Telemetry Refresh* [cite: 125, 127]  
     ↓  
[cite_start]**FastAPI Backend** — *Asynchronous Middleware* [cite: 70, 71]  
     ↓  
[cite_start]**Strategy Engine** — *Supertrend + ADX Gatekeeper* [cite: 37, 56]  
     ↓  
[cite_start]**Zerodha Kite API** — *OAuth 2.0 Secure Bridge* [cite: 67, 68]  
     ↓  
**Live Market & Orders**

---

## 🔹 Technology Stack
| Layer | Technology |
|------|-----------|
| **Backend** | [cite_start]Python, FastAPI [cite: 16, 70] |
| **Broker API** | [cite_start]Zerodha KiteConnect [cite: 16, 67] |
| **Frontend** | [cite_start]HTML, CSS Grid, JavaScript [cite: 125, 127] |
| **Persistence** | [cite_start]JSON State Management [cite: 16, 75] |
| **Indicators** | [cite_start]Supertrend, ADX, ATR, SMA [cite: 16, 39, 53] |

---

## 🔹 Trading Strategies Used
- [cite_start]**Supertrend Breakout**: Primary trend-detection engine[cite: 39, 40].
- [cite_start]**ADX Filter**: Trend strength gatekeeper set at a threshold of $>25$[cite: 55, 56].
- [cite_start]**SMA/EMA Crossover**: Multi-period trend following[cite: 37, 112].
- [cite_start]**Trailing Stop-Loss**: Dynamic 2% safety net tracking peak prices ($P_{max}$)[cite: 28, 59, 60].

---

## 🔹 How the System Works
1. [cite_start]**Authentication**: User logs in via a secure Zerodha OAuth 2.0 handshake[cite: 68].
2. [cite_start]**Scan**: System fetches historical daily data and applies technical strategies[cite: 40, 112].
3. [cite_start]**Filter**: ADX momentum check ensures the market is not "choppy"[cite: 53, 55].
4. [cite_start]**Approval**: Signals are displayed on the dashboard for user verification[cite: 120, 131].
5. [cite_start]**Execution**: Upon approval, a Limit Order (CNC) is placed through the Zerodha bridge[cite: 120].
6. [cite_start]**Management**: Active trades are monitored for trailing stop-loss or 6-day time-exit triggers[cite: 78, 107, 109].

---

## 🔹 Safety Mechanisms
- [cite_start]**No Black-Box Trading**: Mandatory user confirmation for all buy orders[cite: 19, 34, 134].
- [cite_start]**Trailing SL**: Automatic capital protection if price drops 2% from its peak[cite: 28, 59, 107].
- [cite_start]**Time Limit**: Prevents capital stagnation by liquidating positions after 6 days[cite: 28, 79, 109].
- [cite_start]**Secure Persistence**: Credentials and trade states are stored in encrypted environments and JSON buffers[cite: 68, 75, 76].

---

## 🔹 Accuracy & Performance
- [cite_start]**Win Rate**: Expected strategy accuracy is approximately **64.2%**[cite: 138].
- [cite_start]**Benchmark**: Performance is measured against the **NIFTY 50** to ensure realistic risk-adjusted returns[cite: 137, 138].
- [cite_start]**Focus**: Prioritizes capital preservation and correct methodology over exaggerated profit claims[cite: 17, 30, 139].

---

## 🔹 Project Structure
```text
trade_bot/
├── backend/
│   ├── api.py           # FastAPI endpoints & HITL logic
│   ├── strategy.py      # Core signal generation
│   ├── indicators.py    # Math derivations (ADX, ATR)
│   ├── zerodha_session.py # OAuth & Session handlers
│   └── data/            # Persistence (active_trades.json)
├── frontend/
│   ├── index.html       # Telemetry Dashboard
│   ├── script.js        # Polling & UI Logic
│   └── style.css        # CSS Grid Layout
├── requirements.txt     # Dependencies
└── README.md
