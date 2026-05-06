📈 TRADEBOT: Intelligent HITL Algorithmic Trading Framework🔹 Project OverviewTRADEBOT is a Human-in-the-Loop (HITL) algorithmic trading framework designed to bridge the gap between complex quantitative logic and retail investor discipline. Developed at SRMIST (Dept. of CINTEL), this system prioritizes capital preservation and transparency over high-frequency "black-box" execution.Unlike fully autonomous bots that are prone to emotional or systemic risks, TRADEBOT requires human verification before trade execution, ensuring an ethical and controlled approach to market participation.🔹 Key FeaturesIntelligent Scanning: Multi-indicator signal generation using Supertrend and SMA/EMA crossovers.Momentum Gatekeeper: A strict ADX > 25 filter to ensure trades only occur in high-probability, trending markets.Dynamic Risk Management: An automated 2% Trailing Stop-Loss that tracks peak price $(P_{max})$ to lock in gains.Time-Based Exit: Automatic liquidation after 6 days to prevent capital stagnation in sideways moves.Real-time Telemetry: A responsive CSS Grid dashboard providing a 10-second "Glass Box" view into backend logic.🔹 System ArchitectureThe framework follows a decoupled, asynchronous design pattern:Frontend: Vanilla JavaScript + CSS Grid polling every 10,000ms.Backend: FastAPI utilizing non-blocking $I/O$ for simultaneous market analysis.Broker Bridge: Secure integration via Zerodha Kite Connect API with OAuth 2.0 handshake.Persistence Layer: JSON-based state management to track active trades and peak prices across session restarts.🔹 Project StructurePlaintexttrade_bot/
├── backend/
│   ├── api.py           # FastAPI router & HITL endpoints
│   ├── strategy.py      # Signal generation logic (Supertrend/SMA)
│   ├── indicators.py    # Math derivations (ATR, ADX, SMA)
│   ├── zerodha_session.py # OAuth & Session management
│   └── data/            # Persistence (active_trades.json)
├── frontend/
│   ├── index.html       # Telemetry Dashboard
│   ├── script.js        # Polling & UI logic
│   └── style.css        # CSS Grid Layout
└── README.md
🔹 Strategy LogicSignal Generation: Supertrend bands stay flat unless price forces a breakout, filtering minor noise.Execution Logic: if stock.signal == "BUY" and stock.adx > 25 $\rightarrow$ Place Order.Safety Net: Exit Price = P_max * (1 - 0.02).🔹 Getting Started1. InstallationBashpip install -r requirements.txt
2. ConfigurationCreate a .env file in the root directory:PlaintextKITE_API_KEY=your_api_key
KITE_API_SECRET=your_api_secret
3. Run the FrameworkBashpython -m uvicorn backend.main:app --reload
