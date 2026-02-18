console.log("script.js loaded");
const API_BASE = "https://tradebot-iuqd.onrender.com";
let CURRENT_BALANCE = 0;

// -------- BALANCE --------
async function loadBalance() {
  const balanceEl = document.getElementById("balanceAmount");
  balanceEl.innerText = "Loading...";

  try {
    const res = await fetch(`${API_BASE}/balance`);
    const data = await res.json();

    CURRENT_BALANCE = data.available_cash;
    balanceEl.innerText = `₹${CURRENT_BALANCE.toFixed(2)}`;

  } catch (err) {
    balanceEl.innerText = "Error";
    console.error(err);
  }
}


// -------- MARKET SCAN --------
async function runScan() {
    const strategy = document.getElementById("strategy").value;
    const resultBox = document.getElementById("scanResults");

    resultBox.innerHTML = "Scanning market...";

    try {
        const response = await fetch(`${API_BASE}/scan?strategy=${strategy}`);
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


// -------- DOM READY --------
document.addEventListener("DOMContentLoaded", () => {

    const minPriceInput = document.getElementById("minPrice");
    const maxPriceInput = document.getElementById("maxPrice");
    const placeOrderBtn = document.getElementById("placeOrderBtn");

    function validatePrices() {
        const minPrice = parseFloat(minPriceInput.value);
        const maxPrice = parseFloat(maxPriceInput.value);

        if (
            !isNaN(minPrice) &&
            !isNaN(maxPrice) &&
            minPrice > 0 &&
            maxPrice > minPrice
        ) {
            placeOrderBtn.disabled = false;
        } else {
            placeOrderBtn.disabled = true;
        }
    }

    minPriceInput.addEventListener("input", validatePrices);
    maxPriceInput.addEventListener("input", validatePrices);
});


// -------- PLACE ORDER --------
async function placeOrder() {
  const symbol = document.getElementById("symbol").value.trim();
  const quantity = parseInt(document.getElementById("quantity").value);
  const minPrice = parseFloat(document.getElementById("minPrice").value);
  const maxPrice = parseFloat(document.getElementById("maxPrice").value);
  const resultBox = document.getElementById("orderResult");

  if (!symbol || !quantity) {
    resultBox.innerText = "Enter symbol and quantity";
    return;
  }

  if (
    isNaN(minPrice) ||
    isNaN(maxPrice) ||
    minPrice <= 0 ||
    maxPrice <= minPrice
  ) {
    resultBox.innerText = "Invalid price range";
    return;
  }

  resultBox.innerText = "Placing order...";

  try {
    const response = await fetch(`${API_BASE}/order`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        symbol,
        quantity,
        min_price: minPrice,
        max_price: maxPrice
      })
    });

    const data = await response.json();

    if (!response.ok) {
      resultBox.innerText = data.reason || "Order failed";
      return;
    }

    resultBox.innerText = `✅ ${data.status}`;

  } catch (error) {
    resultBox.innerText = "❌ Order failed";
    console.error(error);
  }
}
// expose functions to HTML
window.loadBalance = loadBalance;
window.runScan = runScan;
window.placeOrder = placeOrder;