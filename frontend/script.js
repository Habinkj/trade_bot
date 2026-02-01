const API = "http://127.0.0.1:8000"; // change to Render URL when deployed

function loginZerodha() {
    window.open(API + "/login", "_blank");
}

async function scanMarket() {
    document.getElementById("resultBox").innerText = "Scanning market...";

    try {
        const res = await fetch(API + "/scan");
        const data = await res.json();

        const dropdown = document.getElementById("topStocks");
        dropdown.innerHTML = '<option value="">Select Recommended Stock</option>';

        data.forEach(stock => {
            const option = document.createElement("option");
            option.value = stock.symbol;
            option.text = `${stock.symbol} (${stock.signal}, ${stock.confidence}%)`;
            dropdown.appendChild(option);
        });

        document.getElementById("resultBox").innerText = "Top stocks loaded!";
    } catch (err) {
        document.getElementById("resultBox").innerText = "Error scanning market.";
    }
}

function getSelectedSymbol() {
    const dropdown = document.getElementById("topStocks").value;
    const manual = document.getElementById("symbolInput").value.trim();
    return dropdown || manual;
}

async function getPrediction() {
    const symbol = getSelectedSymbol();
    const sma = document.getElementById("smaSelect").value;

    if (!symbol) {
        alert("Select or enter a stock symbol");
        return;
    }

    document.getElementById("resultBox").innerText = "Getting prediction...";

    try {
        const res = await fetch(`${API}/predict?symbol=${symbol}&sma=${sma}`);
        const data = await res.json();

        document.getElementById("resultBox").innerHTML =
            `📊 Signal: ${data.signal}
📈 Confidence: ${data.confidence}%
🧠 Reason: ${data.reason}`;
    } catch (err) {
        document.getElementById("resultBox").innerText = "Prediction failed.";
    }
}

async function approveTrade() {
    const symbol = getSelectedSymbol();
    const qty = document.getElementById("qtyInput").value;

    if (!symbol) {
        alert("Select or enter a stock symbol");
        return;
    }

    if (!confirm(`⚠️ Place REAL order for ${symbol} qty ${qty}?`)) return;

    document.getElementById("resultBox").innerText = "Placing real order...";

    try {
        const res = await fetch(`${API}/order`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ symbol, qty, side: "buy" })
        });

        const data = await res.json();

        document.getElementById("resultBox").innerText =
            "Order Response:\n" + JSON.stringify(data, null, 2);

    } catch (err) {
        document.getElementById("resultBox").innerText = "Order failed.";
    }
}