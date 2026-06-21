# 📈 TRADEBOT: Intelligent HITL Trading Framework

> **⚠️ Note on Collaboration & Development Methodology**
> This framework was built entirely from scratch as a final-year academic project at SRMIST. My partner ([@fardu6288](https://github.com/fardu6288)) and I utilized strict **Pair Programming** for the entire lifecycle of this project. 
>
> Because we learned the stack, debugged, and architected the system side-by-side on a single machine to optimize our learning curve, the Git commit history is logged under his local configuration. However, every module—from the FastAPI asynchronous backend and Zerodha Kite API bridge to the Vanilla JS telemetry frontend—was equally co-engineered.

## 🔹 Project Overview

TRADEBOT is an intelligent Human-in-the-Loop (HITL) algorithmic trading framework designed to bridge the gap between complex quantitative logic and retail investor discipline. Built using FastAPI and the Zerodha Kite API, the system prioritizes capital preservation and transparency over high-frequency "black-box" execution. 

Unlike fully autonomous bots prone to systemic risks, TRADEBOT requires human verification before trade execution, ensuring an ethical and controlled approach to market participation.

## 🔹 Key Features

* **Intelligent Scanning:** Multi-indicator signal generation using Supertrend and SMA/EMA crossovers across a curated watchlist.
* **Momentum Gatekeeper:** A strict $ADX > 25$ filter to ensure trades only occur in high-probability, trending markets.
* **Dynamic Risk Management:** An automated 2% Trailing Stop-Loss that tracks peak price ($P_{max}$) to lock in gains and protect capital.
* **Time-Based Exit:** Automatic liquidation after 6 days to prevent capital stagnation in sideways moves.
* **Real-time Telemetry:** A responsive CSS Grid dashboard providing a 10-second "Glass Box" view into backend logic, allowing users to monitor anomalies.
* **HITL Approval:** Mandatory manual verification for all orders to mitigate algorithmic and emotional risk.

## 🔹 System Architecture

The framework follows a decoupled, asynchronous design pattern to maintain real-time responsiveness:

**User (Browser) $\rightarrow$ Frontend (Vanilla JS + CSS Grid)**
* 10,000ms telemetry polling for live balance and trade updates.

**$\downarrow$**

**FastAPI Backend**
* Asynchronous middleware managing state and concurrent execution.

**$\downarrow$**

**Strategy Engine**
* Supertrend + ADX Gatekeeper applying mathematical derivations (ATR, ADX, SMA).

**$\downarrow$**

**Zerodha Kite API**
* Secure OAuth 2.0 bridge for live market scanning and CNC Limit Order execution.

## 🔹 Project Structure

```text
trade_bot/
├── backend/
│   ├── api.py               # FastAPI router & HITL endpoints
│   ├── strategy.py          # Signal generation logic (Supertrend/SMA)
│   ├── indicators.py        # Math derivations (ATR, ADX, SMA)
│   ├── zerodha_session.py   # OAuth & Session management
│   └── data/                # Persistence (active_trades.json)
├── frontend/
│   ├── index.html           # Telemetry Dashboard
│   ├── script.js            # Polling & UI logic
│   └── style.css            # CSS Grid Layout
└── README.md
