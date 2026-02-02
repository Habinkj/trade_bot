const API_BASE = "https://https://tradebot-iuqd.onrender.com"; // Same domain

async function refreshBalance() {
    try {
        const res = await fetch(`${API_BASE}/balance`);
        const data = await res.json();
        document.getElementById("balanceAmount").innerText = data.available_cash || 0;
    } catch (err) {
        alert("Failed to fetch balance");
    }
}

async function runScan() {
    const resultsBox = document.getElementById("scanResults");
    resultsBox.innerHTML = "Scanning market...";

    try {
        const response = await fetch("/scan");
        const data = await response.json();

        resultsBox.innerHTML = "";

        if (data.signals && data.signals.length > 0) {
            data.signals.forEach(signal => {
                const li = document.createElement("li");
                li.textContent = signal;
                resultsBox.appendChild(li);
            });
        } else {
            resultsBox.innerHTML = "No signals found";
        }

    } catch (error) {
        resultsBox.innerHTML = "Scan failed";
        console.error("Scan error:", error);
    }
}

async function placeOrder() {
    const symbol = document.getElementById("symbol").value;
    const quantity = document.getElementById("quantity").value;
    const side = document.getElementById("side").value;
    const status = document.getElementById("orderStatus");

    try {
        const res = await fetch(`${API_BASE}/order`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ symbol, quantity, side })
        });

        const data = await res.json();
        status.innerText = data.message || "Order placed!";
    } catch (err) {
        status.innerText = "Order failed";
    }
}