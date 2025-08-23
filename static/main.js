async function compareMeds() {
  const prescribed = document.getElementById("prescribed").value.trim();
  const available = document.getElementById("available").value.trim();
  const resultDiv = document.getElementById("result");

  resultDiv.innerHTML = "<p>Loading...</p>";

  const res = await fetch("/api/compare", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prescribed, available })
  });

  const data = await res.json();

  if (data.error) {
    resultDiv.innerHTML = `<p class="text-danger">${data.error}</p>`;
    console.log(data.raw);
    return;
  }

  resultDiv.innerHTML = `
    <h3>Comparison Result</h3>
    <p><strong>Prescribed Ingredients:</strong> ${data.prescribed_ingredients?.join(", ") || "N/A"}</p>
    <p><strong>Available Ingredients:</strong> ${data.available_ingredients?.join(", ") || "N/A"}</p>
    <p><strong>Therapeutic Use:</strong> ${data.therapeutic_use || "N/A"}</p>
    <p><strong>Side Effects (Prescribed):</strong> ${data.side_effects?.prescribed?.join(", ") || "N/A"}</p>
    <p><strong>Side Effects (Available):</strong> ${data.side_effects?.available?.join(", ") || "N/A"}</p>
    <h4>Confidence Score: ${data.confidence_score || "N/A"}%</h4>
    <p><em>${data.reasoning || ""}</em></p>
  `;
}
