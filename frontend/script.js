async function runScan() {
    const resultsBox = document.getElementById("scanResults");
    resultsBox.innerHTML = "Scanning...";

    try {
        const response = await fetch("/scan");
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
        resultsBox.innerHTML = "Scan failed";
        console.error(error);
    }
}


async function placeOrder() {
    const symbol = document.getElementById("symbol").value;
    const quantity = document.getElementById("quantity").value;
    const side = document.getElementById("side").value;
    const resultBox = document.getElementById("orderResult");

    resultBox.innerText = "Placing order...";

    try {
        const response = await fetch("/order", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ symbol, quantity, side })
        });

        const data = await response.json();
        resultBox.innerText = data.status;

    } catch (error) {
        resultBox.innerText = "Order failed";
        console.error(error);
    }
}