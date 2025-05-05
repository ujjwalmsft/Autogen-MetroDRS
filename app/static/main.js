/**
 * main.js
 *
 * Handles form submission, communicates with the backend API,
 * and displays each agent's response in the result section.
 */

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("incident-form");
    const input = document.getElementById("incident-input");
    const resultSection = document.getElementById("result-section");
    const resultSteps = document.getElementById("result-steps");
  
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
  
      const incident = input.value.trim();
      if (!incident) {
        alert("Please enter a disruption description.");
        return;
      }
  
      // Reset UI and show loading
      resultSteps.innerHTML = "<p>🔄 Contacting agents...</p>";
      resultSection.style.display = "block";
  
      try {
        const response = await fetch("/api/metro_task/run", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ input: incident })
        });
  
        const data = await response.json();
  
        if (data.status !== "completed") {
          resultSteps.innerHTML = `<p class="error">❌ Error: ${data.message || "Unknown error."}</p>`;
          return;
        }
  
        // Display agent responses
        resultSteps.innerHTML = "";
        data.steps.forEach((step, index) => {
          const card = document.createElement("div");
          card.className = "result-card";
          card.innerHTML = `
            <h3>${index + 1}. ${step.name || step.role}</h3>
            <p>${step.content}</p>
          `;
          resultSteps.appendChild(card);
        });
  
      } catch (err) {
        resultSteps.innerHTML = `<p class="error">❌ Failed to reach backend: ${err.message}</p>`;
      }
    });
  });
  