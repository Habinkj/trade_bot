# 📈 TRADEBOT: Intelligent HITL Trading Framework

## 🔹 Project Overview
This project is an **intelligent Human-in-the-Loop (HITL) trading framework** built using **FastAPI** and the **Zerodha Kite API**. The system performs automated market analysis using multi-indicator technical filters to generate high-probability BUY signals. 

To ensure safety, transparency, and ethical compliance, trades are executed **only after explicit user approval**. The goal of this project is to explore the intersection of **Intelligent Computing and financial risk management**.

---

## 🔹 Key Features
- 🔍 **Intelligent Scanning**: Automated analysis across a curated watchlist using Supertrend and SMA/EMA strategies.
- 🛡️ **Momentum Gatekeeper**: Integrated ADX filter ($>25$) to ensure entries only during strong trends.
- 📊 **Real-time Telemetry**: A responsive CSS Grid dashboard providing live balance and trade updates.
- ✅ **HITL Approval**: Manual verification for all orders to mitigate algorithmic risk.
- 🔐 **Risk Protocols**: Automated 2% trailing stop-loss and 6-day time-exit conditions.
- 💰 **Balance Validation**: Real-time margin checking through the Zerodha Kite Connect bridge.

---

## 🔹 Why Human-in-the-Loop (HITL)?
- Fully automated systems can lead to significant capital erosion due to "black-box" failures.
- Human approval acts as a psychological safety net, preventing emotional or blind trading.
- The "Glass Box" design allows users to monitor and intervene during anomalous market events.

---

## 🔹 System Architecture
**User (Browser)**      ↓  
**Frontend (Vanilla JS + CSS Grid)** — *10s Telemetry Refresh*  
     ↓  
**FastAPI Backend** — *Asynchronous Middleware*  
     ↓  
**Strategy Engine** — *Supertrend + ADX Gatekeeper*  
     ↓  
**Zerodha Kite API** — *OAuth 2.0 Secure Bridge*  
     ↓  
**Live Market & Orders**

---

## 🔹 Technology Stack
| Layer | Technology |
|------|-----------|
| **Backend** | Python, FastAPI |
| **Broker API** | Zerodha KiteConnect |
| **Frontend** | HTML, CSS Grid, JavaScript |
| **Persistence** | JSON State Management |
| **Indicators** | Supertrend, ADX, ATR, SMA |

---

## 🔹 Trading Strategies Used
- **Supertrend Breakout**: Primary trend-detection engine.
- **ADX Filter**: Trend strength gatekeeper set at a threshold of $>25$.
- **SMA/EMA Crossover**: Multi-period trend following.
- **Trailing Stop-Loss**: Dynamic 2% safety net tracking peak prices ($P_{max}$).

---

## 🔹 How the System Works
1. **Authentication**: User logs in via a secure Zerodha OAuth 2.0 handshake.
2. **Scan**: System fetches historical daily data and applies technical strategies.
3. **Filter**: ADX momentum check ensures the market is not "choppy".
4. **Approval**: Signals are displayed on the dashboard for user verification.
5. **Execution**: Upon approval, a Limit Order (CNC) is placed through the Zerodha bridge.
6. **Management**: Active trades are monitored for trailing stop-loss or 6-day time-exit triggers.

---

## 🔹 Safety Mechanisms
- **No Black-Box Trading**: Mandatory user confirmation for all buy orders.
- **Trailing SL**: Automatic capital protection if price drops 2% from its peak.
- **Time Limit**: Prevents capital stagnation by liquidating positions after 6 days.
- **Secure Persistence**: Credentials and trade states are stored in encrypted environments and JSON buffers.

---

## 🔹 Accuracy & Performance
- **Win Rate**: Expected strategy accuracy is approximately **64.2%**.
- **Benchmark**: Performance is measured against the **NIFTY 50** to ensure realistic risk-adjusted returns.
- **Focus**: Prioritizes capital preservation and correct methodology over exaggerated profit claims.

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
├── config/
│   └── watchlist.json   # Targeted equity symbols
├── requirements.txt     # Dependencies
└── README.md
