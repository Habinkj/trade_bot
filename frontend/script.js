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

    try {
        const token = localStorage.getItem("token");   // 🔑 get saved token

        if (!token) {
            resultsBox.innerHTML = "Please login first";
            return;
        }

        const response = await fetch("/scan", {
            headers: {
                "Authorization": "Bearer " + token   // 🔥 send token
            }
        });

        if (!response.ok) {
            resultsBox.innerHTML = "Scan failed (Unauthorized)";
            return;
        }

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
        resultsBox.innerHTML = "Scan error";
        console.error(error);
    }
}

async function placeOrder() {
    const symbol = document.getElementById("symbol").value;
    const quantity = document.getElementById("quantity").value;
    const side = document.getElementById("side").value;
    const statusBox = document.getElementById("orderStatus");

    try {
        const token = localStorage.getItem("token");

        if (!token) {
            statusBox.innerText = "Please login first";
            return;
        }

        const response = await fetch("/order", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify({
                symbol: symbol,
                quantity: Number(quantity),
                side: side
            })
        });

        if (!response.ok) {
            statusBox.innerText = "Order failed";
            return;
        }

        const data = await response.json();
        statusBox.innerText = "✅ " + data.status;

    } catch (error) {
        statusBox.innerText = "Order error";
        console.error(error);
    }
}
async function loginUser() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            throw new Error("Invalid credentials");
        }

        const data = await response.json();

        // 🔥 THIS IS STEP 1 — SAVE TOKEN
        localStorage.setItem("token", data.token);

        alert("Login successful!");
    } catch (error) {
        alert("Login failed");
        console.error(error);
    }
}