let historyCount = 0;

//
function createSnowflake() {
  const snowflake = document.createElement("div");
  snowflake.classList.add("snowflake");
  snowflake.textContent = "❄"; 
  snowflake.style.left = Math.random() * window.innerWidth + "px";
  snowflake.style.fontSize = 8 + Math.random() * 12 + "px";
  snowflake.style.animationDuration = 5 + Math.random() * 10 + "s";
  document.body.appendChild(snowflake);

  
  setTimeout(() => {
    snowflake.remove();
  }, parseFloat(snowflake.style.animationDuration) * 1000);
}


setInterval(createSnowflake, 200);


// 
async function extractTopic(text) {
  try {
    const response = await fetch("/process/topic", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: text }),
    });
    if (!response.ok) throw new Error("Server error: " + response.status);
    const data = await response.json();
    return data.result || "Unknown";
  } catch (error) {
    console.error("Topic extraction error:", error);
    return "Unknown";
  }
}


// 
async function addToHistory(action, inputText) {
  historyCount++;
  const table = document.getElementById("historyTable").querySelector("tbody");
  const topic = await extractTopic(inputText);
  const row = document.createElement("tr");
  row.innerHTML = `
    <td>${historyCount}</td>
    <td>${action}</td>
    <td>${topic}</td>
  `;
  table.prepend(row);
}


// 
function formatOutput(action, text) {
  if (action === "summarize" || action === "explain") {
    return text.replace(/\*\*(.*?)\*\*/g, `<strong>$1</strong>`);
  }

  if (action === "questions") {
    let formatted = text
      .replace(/(Q\d*:.*)/g, `<strong>$1</strong>`)
      .replace(/\(Correct:\s*([A-D])\)/g, `<strong>(Correct: $1)</strong>`);
    return formatted;
  }

  return text;
}


// 
async function callAction(action) {
  const inputText = document.getElementById("inputText").value;

  if (!inputText.trim()) {
    alert("Please enter some text first!");
    return;
  }

  try {
    const response = await fetch(`/process/${action}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: inputText }),
    });

    if (!response.ok) {
      throw new Error("Server error: " + response.status);
    }

    const data = await response.json();

    // 
    document.getElementById("output").innerHTML = formatOutput(action, data.result);

    // 
    await addToHistory(action, inputText);
  } catch (error) {
    document.getElementById("output").textContent = "Error: " + error.message;
  }
}
