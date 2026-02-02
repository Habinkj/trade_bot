const API = "https://tradebot-iuqd.onrender.com";

// Auto-refresh every 10 seconds
setInterval(() => {
    getBalance();
    runScan();
    checkStrategy();
}, 10000);

window.onload = () => {
    getBalance();
    runScan();
    checkStrategy();
};

// -------- BALANCE --------
async function getBalance() {
    try {
        const res = await fetch(`${API}/balance`);
        const data = await res.json();
        document.getElementById("balance").innerText = data.available_cash;
    } catch (err) {
        console.log("Balance fetch failed");
    }
}

// -------- MARKET SCAN --------
async function runScan() {
    try {
        const res = await fetch(`${API}/scan`);
        const data = await res.json();

        const list = document.getElementById("scanResults");
        list.innerHTML = "";

        if (data.signals.length === 0) {
            list.innerHTML = "<li>No signals found</li>";
            return;
        }

        data.signals.forEach(item => {
            const li = document.createElement("li");
            li.innerHTML = `
                <strong>${item.symbol}</strong> 
                <span style="color:#2c3e50;">₹${item.price}</span>
            `;
            list.appendChild(li);
        });

    } catch (err) {
        console.log("Scan failed");
    }
}

// -------- PLACE ORDER --------
async function placeOrder() {
    const symbol = document.getElementById("symbol").value;
    const qty = parseInt(document.getElementById("qty").value);
    const side = document.getElementById("side").value;

    try {
        await fetch(`${API}/order`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ symbol, qty, side })
        });

        alert("Order Sent 🚀");
    } catch (err) {
        alert("Order failed ❌");
    }
}

// -------- STRATEGY STATUS --------
async function checkStrategy() {
    try {
        const res = await fetch(`${API}/status`);
        const data = await res.json();

        const dot = document.querySelector(".dot");

        if (data.running) {
            dot.style.backgroundColor = "#2ecc71"; // green
        } else {
            dot.style.backgroundColor = "#e74c3c"; // red
        }

    } catch (err) {
        console.log("Status check failed");
    }
}