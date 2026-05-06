const API_BASE = "http://127.0.0.1:8000";
let CURRENT_BALANCE = 0;

// ==========================
// ⚙️ TOGGLE SETTINGS DRAWER
// ==========================
function toggleSettings() {
    const panel = document.getElementById("scanSettingsPanel");
    if (panel.style.display === "none" || panel.style.display === "") {
        panel.style.display = "block";
    } else {
        panel.style.display = "none";
    }
}

// ==========================
// 🎨 UI VISUAL FEEDBACK HELPER
// ==========================
function setButtonLoading(btnSelector, isLoading, defaultText) {
    const btn = document.querySelector(btnSelector);
    if (!btn) return;
    
    if (isLoading) {
        btn.innerText = "⏳ Processing...";
        btn.style.opacity = "0.7";
        btn.style.cursor = "not-allowed";
        btn.disabled = true;
    } else {
        btn.innerText = defaultText;
        btn.style.opacity = "1";
        btn.style.cursor = "pointer";
        btn.disabled = false;
    }
}

// ==========================
// 1. BALANCE
// ==========================
async function loadBalance(isBackground = false) {
    const el = document.getElementById("balanceAmount");
    if (!isBackground) setButtonLoading('.card.balance button', true, 'Refresh');

    try {
        const res = await fetch(`${API_BASE}/balance`);
        const data = await res.json();
        CURRENT_BALANCE = data.total_balance || 0;
        el.innerText = CURRENT_BALANCE.toFixed(2);
    } catch (err) {
        el.innerText = "Error";
    } finally {
        if (!isBackground) setButtonLoading('.card.balance button', false, 'Refresh');
    }
}

// ==========================
// 2. MARKET SCAN
// ==========================
async function runScan() {
    setButtonLoading('#runScanBtn', true, 'Run Full Scan');
    
    // Grab all 6 parameters from the new settings panel
    const st_p = parseInt(document.getElementById("st_p").value) || 10;
    const st_m = parseFloat(document.getElementById("st_m").value) || 3.0;
    const ema_f = parseInt(document.getElementById("ema_f").value) || 9;
    const ema_s = parseInt(document.getElementById("ema_s").value) || 21;
    const adx = parseFloat(document.getElementById("adx").value) || 25.0;
    const rsi = parseFloat(document.getElementById("rsi").value) || 40.0;

    const tbody = document.querySelector("#scanTable tbody");
    tbody.innerHTML = "<tr><td colspan='5' style='text-align: center; color: #64748b; padding: 20px;'>Scanning Live Markets... 🚀</td></tr>";

    try {
        const res = await fetch(`${API_BASE}/scan?st_p=${st_p}&st_m=${st_m}&ema_f=${ema_f}&ema_s=${ema_s}&adx=${adx}&rsi=${rsi}`);
        let data = await res.json();
        tbody.innerHTML = "";

        if (!data || data.length === 0) {
            tbody.innerHTML = "<tr><td colspan='5' style='text-align: center; color: #64748b; padding: 15px;'>No stocks met the strict Confluence criteria.</td></tr>";
            return;
        }

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
                <td style="font-weight: bold;">${stock.symbol}</td>
                <td>₹${stock.price.toFixed(2)}</td>
                <td class="${sClass}">${stock.signal}</td>
                <td>${stock.adx.toFixed(2)}</td>
                <td><strong>94%</strong></td>
            `;

            row.style.cursor = "pointer";
            row.onclick = () => {
                document.getElementById("symbol").value = stock.symbol;
                document.getElementById("minPrice").value = (stock.price * 0.98).toFixed(2);
                document.getElementById("maxPrice").value = (stock.price * 1.02).toFixed(2);
                const qty = Math.floor((CURRENT_BALANCE * 0.1) / stock.price);
                document.getElementById("quantity").value = qty > 0 ? qty : 1;
                
                const orderBox = document.querySelector(".card.order");
                orderBox.style.transition = "box-shadow 0.3s ease";
                orderBox.style.boxShadow = "0 0 15px rgba(22, 163, 74, 0.5)";
                setTimeout(() => { orderBox.style.boxShadow = "none"; }, 600);
            };

            tbody.appendChild(row);
        });

    } catch (err) {
        tbody.innerHTML = "<tr><td colspan='5' style='color: red; text-align: center;'>Scan failed. Check connection.</td></tr>";
    } finally {
        setButtonLoading('#runScanBtn', false, 'Run Full Scan');
    }
}

// ==========================
// 3. ACTIVE TRADES
// ==========================
async function loadTrades(isBackground = false) {
    if (!isBackground) setButtonLoading('.card.trades button', true, 'Refresh');
    const tbody = document.querySelector("#tradeTable tbody");
    
    try {
        const res = await fetch(`${API_BASE}/trades`);
        const data = await res.json();
        tbody.innerHTML = "";

        if (!data || data.length === 0) {
            tbody.innerHTML = "<tr><td colspan='5' style='text-align: center;'>No active trades</td></tr>";
        } else {
            data.forEach(trade => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td style="font-weight: bold;">${trade.symbol}</td>
                    <td>₹${trade.entry_price}</td>
                    <td>₹${trade.current_price}</td>
                    <td>${trade.quantity}</td>
                    <td class="${trade.pnl >= 0 ? 'green' : 'red'}">${trade.pnl}%</td>
                `;
                tbody.appendChild(row);
            });
        }
    } catch (err) {
        console.error("Trades error:", err);
    } finally {
        if (!isBackground) setButtonLoading('.card.trades button', false, 'Refresh');
    }
}

// ==========================
// 4. TRADE HISTORY
// ==========================
async function loadHistory(isBackground = false) {
    if (!isBackground) setButtonLoading('.card.history button', true, 'Refresh History');
    const tbody = document.querySelector("#historyTable tbody");
    
    try {
        const res = await fetch(`${API_BASE}/history`);
        const data = await res.json();
        tbody.innerHTML = "";

        if (!data || data.length === 0) {
            tbody.innerHTML = "<tr><td colspan='5' style='text-align: center;'>No history available</td></tr>";
        } else {
            data.reverse().forEach(trade => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td style="font-weight: bold;">${trade.symbol}</td>
                    <td>₹${trade.entry_price}</td>
                    <td>₹${trade.exit_price}</td>
                    <td class="${trade.pnl >= 0 ? 'green' : 'red'}">${trade.pnl}%</td>
                    <td>${trade.reason}</td>
                `;
                tbody.appendChild(row);
            });
        }
    } catch (err) {
        console.error("History error:", err);
    } finally {
        if (!isBackground) setButtonLoading('.card.history button', false, 'Refresh History');
    }
}

// ==========================
// 5. PLACE ORDER
// ==========================
async function placeOrder() {
    const symbol = document.getElementById("symbol").value.trim();
    const quantity = parseInt(document.getElementById("quantity").value);
    const min = parseFloat(document.getElementById("minPrice").value);
    const max = parseFloat(document.getElementById("maxPrice").value);
    const resultBox = document.getElementById("orderResult");

    if (!symbol || !quantity || quantity <= 0) {
        resultBox.innerText = "❌ Invalid Inputs";
        resultBox.style.color = "red";
        return;
    }

    setButtonLoading('.card.order button', true, 'Place Order');
    resultBox.innerText = "Routing to Zerodha...";
    resultBox.style.color = "#475569";

    try {
        const res = await fetch(`${API_BASE}/order`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ symbol, quantity, min_price: min, max_price: max })
        });

        const data = await res.json();
        if (!res.ok) {
            resultBox.innerText = data.reason || "❌ Order Failed";
            resultBox.style.color = "red";
        } else {
            resultBox.innerText = `✅ SUCCESS: Order Placed`;
            resultBox.style.color = "#16a34a";
            document.getElementById("symbol").value = "";
            document.getElementById("quantity").value = "";
            
            loadTrades();
            loadBalance();
        }
    } catch (err) {
        resultBox.innerText = "❌ Connection Error";
        resultBox.style.color = "red";
    } finally {
        setButtonLoading('.card.order button', false, 'Place Order');
    }
}

// ==========================
// INIT & AUTOMATION
// ==========================

loadBalance();
loadTrades();
loadHistory();

setInterval(() => {
    loadTrades(true);
    loadBalance(true);
}, 5000);

setInterval(async () => {
    try {
        const res = await fetch(`${API_BASE}/auto-sell`);
        const data = await res.json();
        if (data && data.length > 0) {
            loadTrades(true);
            loadHistory(true);
            loadBalance(true);
        }
    } catch (err) {}
}, 10000);