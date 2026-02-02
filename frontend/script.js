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
    resultsList.innerHTML = "Scanning market...";

    try {
        const response = await fetch("/scan");   // calls FastAPI backend
        const data = await response.json();

        resultsList.innerHTML = "";

        if (data.signals && data.signals.length > 0) {
            data.signals.forEach(signal => {
                const li = document.createElement("li");
                li.textContent = signal;
                resultsList.appendChild(li);
            });
        } else {
            resultsList.innerHTML = "<li>No signals found</li>";
        }

    } catch (error) {
        resultsList.innerHTML = "<li>Error scanning market</li>";
        console.error(error);
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