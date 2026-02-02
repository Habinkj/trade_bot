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
    const resultsList = document.getElementById("scanResults");
    resultsList.innerHTML = "Scanning...";

    try {
        const res = await fetch(`${API_BASE}/scan`);
        const data = await res.json();

        resultsList.innerHTML = "";
        data.results.forEach(stock => {
            const li = document.createElement("li");
            li.textContent = stock;
            resultsList.appendChild(li);
        });

    } catch (err) {
        resultsList.innerHTML = "Scan failed";
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