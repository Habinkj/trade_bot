console.log("script.js loaded");
const API_BASE = "https://trade-bot-hvfi.onrender.com";
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
    console.error("Balance fetch failed:", err);
  }
}


// -------- MARKET SCAN --------
async function runScan() {
    const strategy = document.getElementById("strategy").value;
    const fast = document.getElementById("fast").value;
    const slow = document.getElementById("slow").value;

    const resultBox = document.getElementById("scanResults");

    // SMA validation
    if (strategy === "sma") {
        if (!fast || !slow || fast <= 0 || slow <= 0 || parseInt(fast) >= parseInt(slow)) {
            resultBox.innerHTML = "<li>Invalid SMA values</li>";
            return;
        }
    }

    resultBox.innerHTML = "Scanning market...";

    try {
        const response = await fetch(`${API_BASE}/scan?strategy=${strategy}&fast=${fast}&slow=${slow}`);
        const data = await response.json();

        resultBox.innerHTML = "";

        if (data.length === 0) {
            resultBox.innerHTML = "<li>No signals found</li>";
            return;
        }

        data.forEach(stock => {
            const li = document.createElement("li");

            // ✅ IMPROVED DISPLAY
            li.innerText = `${stock.symbol} | ₹${stock.price} | ${stock.signal} | ADX: ${stock.adx} (${stock.strength})`;

            if (stock.signal === "BUY") {
                li.style.color = "green";
            } else if (stock.signal === "SELL") {
                li.style.color = "red";
            }

            resultBox.appendChild(li);
        });

    } catch (error) {
        resultBox.innerHTML = "<li>Error connecting to server</li>";
        console.error(error);
    }
}


// -------- DOM READY --------
document.addEventListener("DOMContentLoaded", () => {

    loadBalance();   // ✅ load balance immediately
    loadTrades();    // ✅ load trades immediately

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
    const requiredAmount = quantity * maxPrice;

    if (requiredAmount > CURRENT_BALANCE) {
      resultBox.innerText =
        `❌ Insufficient balance. Need ₹${requiredAmount.toFixed(2)}, have ₹${CURRENT_BALANCE.toFixed(2)}`;
      return;
    }

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

    // ✅ refresh trades instantly
    loadTrades();

  } catch (error) {
    resultBox.innerText = "❌ Order failed";
    console.error(error);
  }
}


// -------- ACTIVE TRADES --------
async function loadTrades() {
    const list = document.getElementById("tradeList");
    list.innerHTML = "Loading...";

    try {
        const res = await fetch(`${API_BASE}/trades`);
        const data = await res.json();

        list.innerHTML = "";

        if (data.length === 0) {
            list.innerHTML = "<li>No active trades</li>";
            return;
        }

        data.forEach(trade => {
            const li = document.createElement("li");

            li.innerText = `${trade.symbol} | Entry: ₹${trade.entry_price} | Current: ₹${trade.current_price} | PnL: ${trade.pnl}%`;

            if (trade.pnl >= 0) {
                li.style.color = "green";
            } else {
                li.style.color = "red";
            }

            list.appendChild(li);
        });

    } catch (err) {
        list.innerHTML = "<li>Error loading trades</li>";
        console.error(err);
    }
}


// -------- AUTO SYSTEM (CLEAN VERSION) --------
setInterval(async () => {
    try {
        await loadTrades();

        const res = await fetch(`${API_BASE}/auto-sell`);
        const data = await res.json();

        if (data.length > 0) {
            console.log("Auto Sell Executed:", data);
        }

    } catch (err) {
        console.error("Auto system error", err);
    }
}, 10000);


// expose functions to HTML
window.loadBalance = loadBalance;
window.runScan = runScan;
window.placeOrder = placeOrder;