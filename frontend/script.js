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

    const response = await fetch(`/scan?strategy=${strategy}`);
    const data = await response.json();

    const box = document.getElementById("scanResults");
    box.innerHTML = "";

    if (data.signals.length > 0) {
        data.signals.forEach(sig => {
            const li = document.createElement("li");
            li.textContent = sig;
            box.appendChild(li);
        });
    } else {
        box.innerHTML = "No BUY signals found";
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
