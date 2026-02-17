// -------- BALANCE --------
async function loadBalance() {
  try {
    const res = await fetch("http://127.0.0.1:8000/balance");
    const data = await res.json();

    document.getElementById("balance").innerText =
      `₹${data.available_cash.toFixed(2)}`;
  } catch (err) {
    document.getElementById("balance").innerText = "Error";
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
    const resultBox = document.getElementById("orderResult");
    const payload = {
  symbol: document.getElementById("symbol").value,
  quantity: document.getElementById("quantity").value,
  min_price: document.getElementById("minPrice").value,
  max_price: document.getElementById("maxPrice").value
};

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
            body: JSON.stringify({ symbol, quantity })
        });

        if (!response.ok) throw new Error("Order failed");

        const data = await response.json();
        resultBox.innerText = data.status || "Order placed successfully";

    } catch (error) {
        resultBox.innerText = "Order failed";
        console.error("Order error:", error);
    }
}