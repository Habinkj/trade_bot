const API_BASE = "http://127.0.0.1:8000";

let CURRENT_BALANCE = 0;

// ==========================
// BALANCE
// ==========================
async function loadBalance() {
    const el = document.getElementById("balanceAmount");
    el.innerText = "Loading...";

    try {
        const res = await fetch(`${API_BASE}/balance`);
        const data = await res.json();

        CURRENT_BALANCE = data.available_cash || 0;
        el.innerText = CURRENT_BALANCE.toFixed(2);

    } catch (err) {
        el.innerText = "Error";
        console.error("Balance error:", err);
    }
}


// ==========================
// MARKET SCAN (TABLE)
// ==========================
async function runScan() {
    const strategy = document.getElementById("strategy").value;
    const fast = document.getElementById("fast").value;
    const slow = document.getElementById("slow").value;

    const tbody = document.querySelector("#scanTable tbody");
    tbody.innerHTML = "<tr><td colspan='4'>Scanning...</td></tr>";

    try {
        const res = await fetch(
            `${API_BASE}/scan?strategy=${strategy}&fast=${fast}&slow=${slow}`
        );
        const data = await res.json();

        tbody.innerHTML = "";

        if (!data || data.length === 0) {
            tbody.innerHTML = "<tr><td colspan='4'>No signals found</td></tr>";
            return;
        }

        data.forEach(stock => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${stock.symbol}</td>
                <td>₹${stock.price}</td>
                <td>${stock.signal}</td>
                <td>${stock.adx}</td>
            `;

            // 🔥 CLICK → AUTO-FILL
            row.onclick = () => {
                document.getElementById("symbol").value = stock.symbol;

                const min = stock.price * 0.98;
                const max = stock.price * 1.02;

                document.getElementById("minPrice").value = min.toFixed(2);
                document.getElementById("maxPrice").value = max.toFixed(2);

                // 🔥 AUTO QUANTITY (10% capital)
                const qty = Math.floor((CURRENT_BALANCE * 0.1) / stock.price);
                document.getElementById("quantity").value = qty > 0 ? qty : 1;
            };

            tbody.appendChild(row);
        });

    } catch (err) {
        tbody.innerHTML = "<tr><td colspan='4'>Error loading data</td></tr>";
        console.error("Scan error:", err);
    }
}


// ==========================
// ACTIVE TRADES (TABLE)
// ==========================
async function loadTrades() {
    const tbody = document.querySelector("#tradeTable tbody");
    tbody.innerHTML = "<tr><td colspan='5'>Loading...</td></tr>";

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
                <td style="color:${trade.pnl >= 0 ? 'green' : 'red'}">
                    ${trade.pnl}%
                </td>
            `;

            tbody.appendChild(row);
        });

    } catch (err) {
        tbody.innerHTML = "<tr><td colspan='5'>Error loading trades</td></tr>";
        console.error("Trades error:", err);
    }
}


// ==========================
// PLACE ORDER (SAFE VERSION)
// ==========================
async function placeOrder() {
    const symbol = document.getElementById("symbol").value.trim();
    const quantity = parseInt(document.getElementById("quantity").value);
    const min = parseFloat(document.getElementById("minPrice").value);
    const max = parseFloat(document.getElementById("maxPrice").value);
    const resultBox = document.getElementById("orderResult");

    // 🔴 VALIDATION
    if (!symbol || !quantity || quantity <= 0) {
        resultBox.innerText = "❌ Enter valid symbol & quantity";
        return;
    }

    if (
        isNaN(min) ||
        isNaN(max) ||
        min <= 0 ||
        max <= min
    ) {
        resultBox.innerText = "❌ Invalid price range";
        return;
    }

    // 🔴 BALANCE CHECK
    const required = quantity * max;
    if (required > CURRENT_BALANCE) {
        resultBox.innerText = `❌ Not enough balance (Need ₹${required.toFixed(2)})`;
        return;
    }

    resultBox.innerText = "Placing order...";

    try {
        const res = await fetch(`${API_BASE}/order`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                symbol,
                quantity,
                min_price: min,
                max_price: max
            })
        });

        const data = await res.json();

        if (!res.ok) {
            resultBox.innerText = data.reason || "❌ Order failed";
            return;
        }

        resultBox.innerText = `✅ ${data.status}`;

        // refresh trades after buy
        loadTrades();

    } catch (err) {
        resultBox.innerText = "❌ Order error";
        console.error("Order error:", err);
    }
}


// ==========================
// AUTO SELL LOOP
// ==========================
setInterval(async () => {
    try {
        const res = await fetch(`${API_BASE}/auto-sell`);
        const data = await res.json();

        if (data.length > 0) {
            console.log("Auto Sell:", data);
            loadTrades();
        }

    } catch (err) {
        console.error("Auto sell error:", err);
    }
}, 10000);


// ==========================
// INIT
// ==========================
loadBalance();
loadTrades();

setInterval(loadTrades, 10000);