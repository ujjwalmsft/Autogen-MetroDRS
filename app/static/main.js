/**
 * main.js
 *
 * Handles form submission, communicates with the backend API,
 * and displays each agent's response in the result section.
 */

// Simple console log to verify script is loaded
console.log("Metro system script loaded");

document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM Content Loaded event fired");

    // Get button element
    const submitBtn = document.getElementById("submit-btn");
    console.log("Submit button found:", submitBtn);

    // Add click event with basic handler first
    if (submitBtn) {
        submitBtn.addEventListener("click", function() {
            console.log("Process Incident button clicked");
            alert("Button clicked! Now attempting to process incident...");
            
            // After confirming the basic click works, try the full processing
            processIncident();
        });
    } else {
        console.error("Submit button not found in the DOM");
    }

    // Get other DOM elements
    const form = document.getElementById("incident-form");
    const input = document.getElementById("incident-input");
    const resultSection = document.getElementById("result-section");
    const resultSteps = document.getElementById("result-steps");
    
    console.log("Form elements found:", {
        form: form ? "Yes" : "No",
        input: input ? "Yes" : "No",
        resultSection: resultSection ? "Yes" : "No",
        resultSteps: resultSteps ? "Yes" : "No"
    });
  
    // Add form submit handler too
    if (form) {
        form.addEventListener("submit", function(event) {
            event.preventDefault();
            console.log("Form submitted");
            processIncident();
        });
    }
    
    // Function to process the incident
    async function processIncident() {
        console.log("processIncident function called");
        
        if (!input) {
            console.error("Input element not found!");
            return;
        }
        
        const incident = input.value.trim();
        if (!incident) {
            alert("Please enter a disruption description.");
            return;
        }
        
        console.log("Processing incident text:", incident);
  
        // Make sure results section is visible
        if (resultSection) {
            resultSection.style.display = "block";
        }
        
        // Show loading message
        if (resultSteps) {
            resultSteps.innerHTML = "<p>🔄 Contacting agents...</p>";
        }
  
        try {
            console.log("Sending API request to /api/metro_task/run");
            const response = await fetch("/api/metro_task/run", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ input: incident })
            });
            
            console.log("API response received, status:", response.status);
  
            const data = await response.json();
            console.log("API response data:", data);
  
            if (!resultSteps) {
                console.error("Result steps element not found for displaying results!");
                return;
            }
            
            if (data.status !== "completed") {
                resultSteps.innerHTML = `<p class="error">❌ Error: ${data.message || "Unknown error."}</p>`;
                return;
            }
  
            // Display agent responses with animation
            resultSteps.innerHTML = "";
            displayStepsSequentially(data.steps);
  
        } catch (err) {
            console.error("API request failed:", err);
            if (resultSteps) {
                resultSteps.innerHTML = `<p class="error">❌ Failed to reach backend: ${err.message}</p>`;
            }
        }
    }
    
    // Function to display steps with a sequential animation
    function displayStepsSequentially(steps) {
        if (!resultSteps) {
            console.error("Result steps element not found!");
            return;
        }
        
        console.log("Displaying steps sequentially:", steps.length, "steps");
        
        steps.forEach((step, index) => {
            setTimeout(() => {
                // Create the card with animation
                const card = document.createElement("div");
                card.className = "result-card";
                
                // Generate current time for the step
                const now = new Date();
                const timeString = now.toLocaleTimeString();
                
                // Format the agent name
                const formattedName = formatAgentName(step.name);
                
                card.innerHTML = `
                <div class="step-marker">${index + 1}</div>
                <div class="step-header">
                    <h3>${formattedName}</h3>
                    <span class="step-time">${timeString}</span>
                </div>
                <div class="step-content">
                    <p>${step.content}</p>
                </div>
                `;
                
                resultSteps.appendChild(card);
                
                // Scroll to the new card
                card.scrollIntoView({ behavior: 'smooth', block: 'end' });
                
                console.log(`Step ${index + 1} displayed: ${step.name}`);
            }, index * 800); // Add delay for sequential appearance
        });
    }
    
    // Function to format agent names for display
    function formatAgentName(name) {
        if (!name) return "Agent";
        
        return name
            .replace('Agent', '')
            .replace(/([A-Z])/g, ' $1') // Add spaces before capital letters
            .trim();
    }
    
    // Debug function - can be used to test the UI with sample data
    window.testUI = function() {
        console.log("Testing UI with debug endpoint");
        fetch('/api/metro_task/debug')
            .then(response => {
                console.log("Debug response status:", response.status);
                return response.json();
            })
            .then(data => {
                console.log("Debug data received:", data);
                if (resultSteps && resultSection) {
                    resultSteps.innerHTML = "";
                    resultSection.style.display = "block";
                    displayStepsSequentially(data.steps);
                } else {
                    console.error("Result elements not found for debug display");
                }
            })
            .catch(error => {
                console.error("Debug error:", error);
                if (resultSteps) {
                    resultSteps.innerHTML = `<p class="error">❌ Debug test failed: ${error.message}</p>`;
                }
            });
    };
    
    // Log initialization complete
    console.log("Metro response system initialized - event handlers should be attached");
});

// Add a global error handler to catch any JavaScript errors
window.onerror = function(message, source, lineno, colno, error) {
    console.error("JavaScript error:", message, "at", source, "line", lineno, "column", colno);
    console.error("Error details:", error);
    return false;
};