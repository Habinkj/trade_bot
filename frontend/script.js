// -------- STRATEGY OPTIONS --------
const strategies = {
    "Fast SMA (5/9)": "sma_fast",
    "Medium SMA (9/21)": "sma_medium",
    "Triple SMA (5/13/34)": "sma_triple",

    // NEW EMA STRATEGIES
    "EMA Crossover (9/21)": "ema_cross",
    "Fast EMA (5/9)": "ema_fast"
};

// Load strategies into dropdown when page loads
window.addEventListener("DOMContentLoaded", () => {
    const strategySelect = document.getElementById("strategy");

    // Prevent duplicates if already present
    strategySelect.innerHTML = "";

    for (let label in strategies) {
        const option = document.createElement("option");
        option.text = label;
        option.value = strategies[label];
        strategySelect.add(option);
    }
});/


/ -------- BALANCE --------
async function refreshBalance() {
    const balanceEl = document.getElementById("balanceAmount");
    balanceEl.innerText = "Loading...";

    try {
        const res = await fetch("/balance"); // optional backend endpoint
        if (!res.ok) throw new Error();

        const data = await res.json();
        balanceEl.innerText = "₹" + data.balance;
    } catch {
        balanceEl.innerText = "₹0";
    }
}


// -------- MARKET SCAN --------
async function runScan() {
    const strategy = document.getElementById("strategy").value;
    const resultBox = document.getElementById("scanResults");

    resultBox.innerHTML = "Scanning market...";

    try {
        const response = await fetch(`/scan?strategy=${strategy}`);
        const data = await response.json();

        resultBox.innerHTML = "";

        if (data.length === 0) {
            resultBox.innerHTML = "<li>No BUY signals found</li>";
            return;
        }

        data.forEach(stock => {
            resultBox.innerHTML += `<li>${stock.symbol} - ₹${stock.price} - ${stock.signal}</li>`;
        });

    } catch (error) {
        resultBox.innerHTML = "<li>Error connecting to server</li>";
        console.error(error);
    }
}

// -------- PLACE ORDER --------
async function placeOrder() {
    const symbol = document.getElementById("symbol").value;
    const quantity = document.getElementById("quantity").value;
    const side = document.getElementById("side").value;
    const resultBox = document.getElementById("orderResult");

    if (!symbol || !quantity) {
        resultBox.innerText = "Enter symbol and quantity";
        return;
    }

    resultBox.innerText = "Placing order...";

    try {
        const response = await fetch("/order", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                symbol: symbol,
                quantity: quantity,
                side: side
            })
        });

        if (!response.ok) throw new Error("Order failed");

        const data = await response.json();
        resultBox.innerText = data.status || "Order placed successfully";

    } catch (error) {
        resultBox.innerText = "Order failed";
        console.error("Order error:", error);
    }
}


async function refreshBalance() {
    const res = await fetch("/balance");
    const data = await res.json();

    document.getElementById("balanceAmount").textContent = data.balance || 0;
}