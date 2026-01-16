async function predict() {
  const symbol = document.getElementById("symbol").value;
  const resultBox = document.getElementById("result");

  try {
    const res = await fetch(`http://127.0.0.1:8000/signal/${symbol}`);
    const data = await res.json();

    window.lastSignal = data;
    resultBox.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    resultBox.textContent = "Error fetching prediction. Check backend.";
  }
}

async function execute() {
  if (!window.lastSignal || window.lastSignal.signal !== "BUY") {
    alert("No BUY signal available");
    return;
  }

  alert("Trade execution will be added after API integration");
}
