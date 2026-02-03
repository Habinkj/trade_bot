// -------- BALANCE --------
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

    const res = await fetch(`/scan?strategy=${strategy}`);
    const data = await res.json();

    const list = document.getElementById("signalsList");
    list.innerHTML = "";

    if (data.signals.length === 0) {
        list.innerHTML = "<li>No BUY signals found</li>";
        return;
    }

    data.signals.forEach(signal => {
        const li = document.createElement("li");
        li.textContent = signal;
        list.appendChild(li);
    });
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