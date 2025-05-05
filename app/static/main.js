// Wait for DOM to load
document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM loaded, initializing incident form handlers");
    
    const incidentForm = document.getElementById('incident-form');
    const incidentInput = document.getElementById('incident-input');
    // Look for the correct button ID that exists in the HTML
    const processButton = document.getElementById('submit-btn');
    const resultSteps = document.getElementById('result-steps');
    const resultSection = document.getElementById('result-section');
    const loadingIndicator = document.getElementById('loading-indicator');
    
    // Log elements to make sure they're found
    console.log("Form elements found:", {
        form: !!incidentForm,
        input: !!incidentInput,
        button: !!processButton,
        results: !!resultSteps,
        loading: !!loadingIndicator,
        resultSection: !!resultSection
    });
    
    // Initialize with sample incident text
    if (incidentInput) {
        incidentInput.value = "Train breakdown on green line near Tampines station";
    }
    
    // Add direct click handler to button in addition to form submit
    if (processButton) {
        console.log("Adding click handler to process button");
        processButton.addEventListener('click', async (e) => {
            console.log("Process button clicked!");
            e.preventDefault();
            await processIncident();
        });
    } else {
        console.error("CRITICAL ERROR: Process button not found! Check HTML IDs.");
    }
    
    if (incidentForm) {
        console.log("Adding submit handler to form");
        incidentForm.addEventListener('submit', async (e) => {
            console.log("Form submitted");
            e.preventDefault();
            await processIncident();
        });
    }
    
    // Create a global test function for direct debugging
    window.testUI = function() {
        console.log("Manual test function called");
        alert("Testing UI interactions");
        // Make the results section visible for testing
        if (resultSection) resultSection.style.display = "block";
        if (resultSteps) {
            resultSteps.innerHTML = "<p>Test message added to results</p>";
        }
    };
    
    // Function to directly use the hardcoded mock data if API fails completely
    function getMockSteps() {
        return [
            {
                "name": "TrainBreakdownAgent",
                "content": "🚨 Incident logged successfully at Tampines. Disruption response initiated."
            },
            {
                "name": "DriverCoordinationAgent",
                "content": "📣 Notification sent to 10 drivers. 8/10 confirmed. Still waiting on 2 responses..."
            },
            {
                "name": "DepotMaintenanceAgent",
                "content": "🚍 Maintenance team notified to prepare 10 buses. Depot confirmed all buses are ready for deployment."
            },
            {
                "name": "PublicCommunicationAgent",
                "content": "⚠️ Draft social media post: 'Service disruption on Green Line near Tampines. Shuttle buses are being arranged. We apologize for the inconvenience.'"
            },
            {
                "name": "IncidentResolutionAgent",
                "content": "✅ System check complete. No remaining disruptions detected at Tampines. Ready to proceed with clearance notification."
            },
            {
                "name": "InternalNotificationAgent",
                "content": "📨 All internal teams notified of incident resolution. Acknowledged by: Control Room, Bus Ops, Maintenance."
            },
            {
                "name": "PublicUpdateAgent",
                "content": "📢 Public notice posted: 'Train services on Green Line have resumed. Thank you for your patience.' Published on Twitter, Facebook, and IG."
            }
        ];
    }
    
    async function processIncident() {
        console.log("processIncident function started");
        // Make sure the results section is visible
        if (resultSection) {
            console.log("Making results section visible");
            resultSection.style.display = "block";
        }
        
        const incident = incidentInput ? incidentInput.value.trim() : "";
        console.log("Incident text:", incident);
        
        if (!incident) {
            alert("Please enter an incident description");
            return;
        }
        
        // Show loading indicator
        if (loadingIndicator) {
            console.log("Showing loading indicator");
            loadingIndicator.style.display = 'block';
        }
        if (processButton) {
            processButton.disabled = true;
        }
        
        // Define the main API URL - the one that really works
        const apiUrl = "/api/metro_task/run/text";
        
        try {
            console.log(`Sending API request to ${apiUrl} with input:`, incident);
            
            // Directly call the API that we know works in Swagger
            const response = await fetch(apiUrl, {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: JSON.stringify({ text: incident })
            });
            
            console.log("API response status:", response.status);
            
            let data;
            
            // Even with status 404, try to parse the JSON response
            // This is because your API actually returns a valid JSON with fallback steps
            // even when it encounters a 404 error from Azure OpenAI
            try {
                data = await response.json();
                console.log("Response data:", data);
            } catch (parseError) {
                console.error("Error parsing JSON response:", parseError);
                // If we can't parse the response, use the hardcoded mock data
                data = {
                    status: "error",
                    message: "Invalid response from server: " + parseError.message,
                    steps: getMockSteps()
                };
            }

            if (!resultSteps) {
                console.error("Result steps element not found for displaying results!");
                return;
            }
            
            // Always use the steps if they exist, regardless of status
            if (data.steps && data.steps.length > 0) {
                console.log(`Found ${data.steps.length} steps in response - displaying them`);
                
                if (data.status !== "completed") {
                    // Show notice about fallback response
                    resultSteps.innerHTML = `<p class="notice">⚠️ Note: Using automated response (API status: ${data.status})</p>`;
                } else {
                    resultSteps.innerHTML = "";
                }
                
                displayStepsSequentially(data.steps);
            } else {
                console.log("No steps found in response - using mock data");
                resultSteps.innerHTML = `<p class="notice">⚠️ Note: No steps returned from API - using fallback</p>`;
                displayStepsSequentially(getMockSteps());
            }
            
        } catch (err) {
            console.error("Error processing incident:", err);
            
            // Use mock data as final fallback
            resultSteps.innerHTML = `<p class="notice">⚠️ Network error - using fallback response</p>`;
            displayStepsSequentially(getMockSteps());
            
        } finally {
            // Hide loading indicator
            if (loadingIndicator) {
                console.log("Hiding loading indicator");
                loadingIndicator.style.display = 'none';
            }
            if (processButton) {
                processButton.disabled = false;
            }
        }
    }
    
    function displayStepsSequentially(steps) {
        console.log("displayStepsSequentially called with", steps ? steps.length : 0, "steps");
        if (!steps || !steps.length) {
            console.log("No steps to display");
            return;
        }
        
        // Clear previous content if needed
        if (!resultSteps.querySelector('.steps-container')) {
            resultSteps.innerHTML = resultSteps.innerHTML + '<div class="steps-container"></div>';
        }
        
        const stepsContainer = resultSteps.querySelector('.steps-container');
        
        const stepDisplayDelay = 1000; // ms between steps
        
        steps.forEach((step, index) => {
            console.log(`Scheduling step ${index+1} to display in ${index * stepDisplayDelay}ms`);
            setTimeout(() => {
                console.log(`Displaying step ${index+1}: ${step.name}`);
                const stepEl = document.createElement('div');
                stepEl.className = 'step-item animated fadeIn';
                
                // Determine agent icon based on agent name
                let agentIcon = '🤖';
                if (step.name.includes('TrainBreakdown')) agentIcon = '🚨';
                else if (step.name.includes('DriverCoordination')) agentIcon = '📣';
                else if (step.name.includes('DepotMaintenance')) agentIcon = '🚍';
                else if (step.name.includes('PublicCommunication')) agentIcon = '⚠️';
                else if (step.name.includes('IncidentResolution')) agentIcon = '✅';
                else if (step.name.includes('InternalNotification')) agentIcon = '📨';
                else if (step.name.includes('PublicUpdate')) agentIcon = '📢';
                
                stepEl.innerHTML = `
                    <div class="step-header">
                        <span class="step-icon">${agentIcon}</span>
                        <span class="step-name">${step.name}</span>
                        <span class="step-number">${index + 1}</span>
                    </div>
                    <div class="step-content">${step.content}</div>
                `;
                
                stepsContainer.appendChild(stepEl);
                console.log(`Step ${index+1} added to DOM`);
                
                // Scroll to the bottom to show the latest step
                stepsContainer.scrollTop = stepsContainer.scrollHeight;
            }, index * stepDisplayDelay);
        });
    }
    
    // Log that we've reached the end of initialization
    console.log("Metro disruption UI initialized successfully");
});