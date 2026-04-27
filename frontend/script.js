const API_BASE = "http://127.0.0.1:8000";

let CURRENT_BALANCE = 0;

// ==========================
// BALANCE
// ==========================
async function loadBalance() {
    const el = document.getElementById("balanceAmount");
    try {
        const res = await fetch(`${API_BASE}/balance`);
        const data = await res.json();

        // Using total_balance to match your Kite App (400.26)
        CURRENT_BALANCE = data.total_balance || 0;
        el.innerText = CURRENT_BALANCE.toFixed(2);

    } catch (err) {
        el.innerText = "Error";
        console.error("Balance error:", err);
    }
}


// ==========================
// MARKET SCAN (SORTED)
// ==========================
async function runScan() {
    const strategy = document.getElementById("strategy").value;
    const fast = document.getElementById("fast").value;
    const slow = document.getElementById("slow").value;

    const tbody = document.querySelector("#scanTable tbody");
    tbody.innerHTML = "<tr><td colspan='4'>Scanning...</td></tr>";

    try {
        const res = await fetch(
            `${API_BASE}/scan?strategy=${strategy}&fast=${parseInt(fast)}&slow=${parseInt(slow)}`
        );
        let data = await res.json();

        tbody.innerHTML = "";

        if (!data || data.length === 0) {
            tbody.innerHTML = "<tr><td colspan='4'>No signals found</td></tr>";
            return;
        }

        // 🔥 SORTING: Actionable signals (BUY/SELL) and high ADX first
        data.sort((a, b) => {
            const isActionA = a.signal === "BUY" || a.signal === "SELL";
            const isActionB = b.signal === "BUY" || b.signal === "SELL";
            if (isActionA && !isActionB) return -1;
            if (!isActionA && isActionB) return 1;
            return b.adx - a.adx;
        });

        data.forEach(stock => {
            const row = document.createElement("tr");
            const sClass = stock.signal.includes("BUY") ? "green" : stock.signal.includes("SELL") ? "red" : "";

            row.innerHTML = `
                <td>${stock.symbol}</td>
                <td>₹${stock.price}</td>
                <td class="${sClass}">${stock.signal}</td>
                <td>${stock.adx}</td>
            `;

            row.onclick = () => {
                document.getElementById("symbol").value = stock.symbol;
                document.getElementById("minPrice").value = (stock.price * 0.98).toFixed(2);
                document.getElementById("maxPrice").value = (stock.price * 1.02).toFixed(2);
                const qty = Math.floor((CURRENT_BALANCE * 0.1) / stock.price);
                document.getElementById("quantity").value = qty > 0 ? qty : 1;
            };

            tbody.appendChild(row);
        });

    } catch (err) {
        tbody.innerHTML = "<tr><td colspan='4'>Error loading data</td></tr>";
    }
}


// ==========================
// ACTIVE TRADES (AUTO-RELOAD)
// ==========================
async function loadTrades() {
    const tbody = document.querySelector("#tradeTable tbody");
    try {
        const res = await fetch(`${API_BASE}/trades`);
        const data = await res.json();

        tbody.innerHTML = "";

        if (!data || data.length === 0) {
            tbody.innerHTML = "<tr><td colspan='5'>No active trades</td></tr>";
            return;
        }

        data.forEach(trade => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${trade.symbol}</td>
                <td>₹${trade.entry_price}</td>
                <td>₹${trade.current_price}</td>
                <td>${trade.quantity}</td>
                <td class="${trade.pnl >= 0 ? 'green' : 'red'}">${trade.pnl}%</td>
            `;
            tbody.appendChild(row);
        });

    } catch (err) {
        console.error("Trades error:", err);
    }
}


// ==========================
// TRADE HISTORY
// ==========================
async function loadHistory() {
    const tbody = document.querySelector("#historyTable tbody");
    try {
        const res = await fetch(`${API_BASE}/history`);
        const data = await res.json();
        tbody.innerHTML = "";

        if (!data || data.length === 0) {
            tbody.innerHTML = "<tr><td colspan='5'>No history available</td></tr>";
            return;
        }

        data.reverse().forEach(trade => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${trade.symbol}</td>
                <td>₹${trade.entry_price}</td>
                <td>₹${trade.exit_price}</td>
                <td class="${trade.pnl >= 0 ? 'green' : 'red'}">${trade.pnl}%</td>
                <td>${trade.reason}</td>
            `;
            tbody.appendChild(row);
        });
    } catch (err) {
        console.error("History error:", err);
    }
}


// ==========================
// PLACE ORDER
// ==========================
async function placeOrder() {
    const symbol = document.getElementById("symbol").value.trim();
    const quantity = parseInt(document.getElementById("quantity").value);
    const min = parseFloat(document.getElementById("minPrice").value);
    const max = parseFloat(document.getElementById("maxPrice").value);
    const resultBox = document.getElementById("orderResult");

    if (!symbol || !quantity || quantity <= 0) {
        resultBox.innerText = "❌ Invalid Inputs";
        return;
    }

    resultBox.innerText = "Placing order...";

    try {
        const res = await fetch(`${API_BASE}/order`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ symbol, quantity, min_price: min, max_price: max })
        });

        const data = await res.json();
        if (!res.ok) {
            resultBox.innerText = data.reason || "❌ Failed";
            return;
        }

        resultBox.innerText = `✅ SUCCESS`;
        loadTrades();
        loadBalance();

    } catch (err) {
        resultBox.innerText = "❌ Error";
    }
}


// ==========================
// INIT & AUTOMATION
// ==========================

// Initial Load
loadBalance();
loadTrades();
loadHistory();

// Refresh Active Trades & Balance every 5 seconds
setInterval(() => {
    loadTrades();
    loadBalance();
}, 5000);

// Auto-Sell Monitoring loop (every 10 seconds)
setInterval(async () => {
    try {
        const res = await fetch(`${API_BASE}/auto-sell`);
        const data = await res.json();

        // If a sale happened, refresh everything
        if (data && data.length > 0) {
            loadTrades();
            loadHistory();
            loadBalance();
        }
    } catch (err) {
        console.error("Auto sell loop error:", err);
    }
}, 10000);