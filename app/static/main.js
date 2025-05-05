// Modern transit disruption response system
document.addEventListener('DOMContentLoaded', () => {
    console.log("Initializing Metro Disruption Response System...");
    
    // Elements
    const incidentForm = document.getElementById('incident-form');
    const incidentInput = document.getElementById('incident-input');
    const submitButton = document.getElementById('submit-btn');
    const resultSection = document.getElementById('result-section');
    const resultSteps = document.getElementById('result-steps');
    const loadingIndicator = document.getElementById('loading-indicator');
    
    // Initialize with a professional example
    if (incidentInput) {
        incidentInput.value = "Train breakdown on green line near Tampines station";
        
        // Add focus effect
        incidentInput.addEventListener('focus', () => {
            incidentInput.parentElement.classList.add('focused');
        });
        
        incidentInput.addEventListener('blur', () => {
            incidentInput.parentElement.classList.remove('focused');
        });
    }
    
    // Form submit handlers
    if (submitButton) {
        submitButton.addEventListener('click', async (e) => {
            e.preventDefault();
            await processIncident();
        });
    }
    
    if (incidentForm) {
        incidentForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            await processIncident();
        });
    }
    
    // Create global test function for debugging
    window.testUI = function() {
        if (resultSection) resultSection.style.display = "block";
        if (resultSteps) {
            displayStepsSequentially(getMockSteps());
        }
    };
    
    // Mock data for fallback and testing
    function getMockSteps() {
        return [
            {
                "name": "TrainBreakdownAgent",
                "content": "🚨 Incident logged successfully at Tampines. Disruption response protocol initiated. Initial assessment indicates power supply failure affecting track circuits."
            },
            {
                "name": "DriverCoordinationAgent",
                "content": "📣 Emergency notification dispatched to 10 shuttle drivers. 8/10 confirmed availability. ETA to station: 12 minutes. Still awaiting confirmation from 2 drivers..."
            },
            {
                "name": "DepotMaintenanceAgent",
                "content": "🚍 Maintenance team notified to prepare 10 replacement buses. Depot confirmed all vehicles are fueled, inspected and ready for immediate deployment. Maintenance crew dispatched to incident location."
            },
            {
                "name": "PublicCommunicationAgent",
                "content": "⚠️ Draft social media announcement: 'SERVICE ALERT: Green Line experiencing disruption near Tampines. Shuttle buses are being arranged. Expect delays of 15-20 minutes. We apologize for the inconvenience and are working to restore service quickly.'"
            },
            {
                "name": "IncidentResolutionAgent",
                "content": "✅ System diagnostic complete. Power supply restored and track circuits recalibrated. Safety checks passed. No remaining disruptions detected at Tampines Station. Ready to proceed with service restoration."
            },
            {
                "name": "InternalNotificationAgent",
                "content": "📨 All stakeholders notified of incident resolution. Acknowledgments received from: Control Room, Bus Operations, Maintenance Division, Station Masters, and Customer Service teams."
            },
            {
                "name": "PublicUpdateAgent",
                "content": "📢 SERVICE RESTORED: 'Green Line services have resumed normal operation. Thank you for your patience during this disruption.' Published across Twitter, Facebook, Instagram, and the Metro Mobile App."
            }
        ];
    }
    
    // Process the incident report
    async function processIncident() {
        const incident = incidentInput ? incidentInput.value.trim() : "";
        
        if (!incident) {
            showNotification("Please enter an incident description", "warning");
            return;
        }
        
        // Show loading state
        if (loadingIndicator) loadingIndicator.classList.remove('hidden');
        if (submitButton) submitButton.disabled = true;
        
        // Define the API URL
        const apiUrl = "/api/metro_task/fallback/text";
        
        try {
            console.log(`Processing incident: ${incident}`);
            
            const response = await fetch(apiUrl, {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: JSON.stringify({ text: incident })
            });
            
            let data;
            
            try {
                data = await response.json();
            } catch (parseError) {
                console.error("Error parsing response:", parseError);
                data = {
                    status: "error",
                    message: "Invalid response format",
                    steps: getMockSteps()
                };
            }
            
            // Show result section
            if (resultSection) resultSection.style.display = "block";
            
            // Smooth scroll to results
            resultSection.scrollIntoView({ behavior: 'smooth' });
            
            if (data.steps && data.steps.length > 0) {
                if (data.status !== "completed") {
                    // Show notice about fallback
                    resultSteps.innerHTML = `
                        <div class="notice">
                            <strong>⚠️ Note:</strong> Using automated response system.
                            <span class="notice-details">(${data.status})</span>
                        </div>
                    `;
                } else {
                    resultSteps.innerHTML = "";
                }
                
                displayStepsSequentially(data.steps);
            } else {
                resultSteps.innerHTML = `
                    <div class="notice">
                        <strong>⚠️ System Notice:</strong> Using fallback response protocol.
                    </div>
                `;
                displayStepsSequentially(getMockSteps());
            }
            
        } catch (err) {
            console.error("Error:", err);
            
            if (resultSection) resultSection.style.display = "block";
            resultSteps.innerHTML = `
                <div class="notice">
                    <strong>⚠️ Connection Error:</strong> Using emergency response protocol.
                </div>
            `;
            displayStepsSequentially(getMockSteps());
            
        } finally {
            // Hide loading indicator
            if (loadingIndicator) loadingIndicator.classList.add('hidden');
            if (submitButton) submitButton.disabled = false;
        }
    }
    
    // Display steps with professional animation and consistent 1.5s delay between steps
    function displayStepsSequentially(steps) {
        if (!steps || !steps.length) return;
        
        // Clear previous content if needed
        if (!resultSteps.querySelector('.steps-container')) {
            resultSteps.innerHTML = resultSteps.innerHTML + '<div class="steps-container"></div>';
        }
        
        const stepsContainer = resultSteps.querySelector('.steps-container');
        stepsContainer.innerHTML = ''; // Clear any existing steps
        
        // Fixed 1.5 second delay between steps (1000ms) as requested
        const stepDelay = 1000; 
        
        // Add a "typing" indicator that moves between agents
        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'typing-indicator';
        typingIndicator.innerHTML = '<span></span><span></span><span></span>';
        stepsContainer.appendChild(typingIndicator);
        
        // Process each step with the exact 1.5 second delay
        steps.forEach((step, index) => {
            setTimeout(() => {
                // Remove typing indicator from previous position
                if (typingIndicator.parentNode) {
                    typingIndicator.parentNode.removeChild(typingIndicator);
                }
                
                // Create the step element
                const stepEl = document.createElement('div');
                stepEl.className = 'step-item';
                stepEl.style.opacity = '0';
                stepEl.style.transform = 'translateY(20px)';
                
                // Determine agent icon
                let agentIcon = '🤖';
                if (step.name.includes('TrainBreakdown')) agentIcon = '🚨';
                else if (step.name.includes('DriverCoordination')) agentIcon = '📣';
                else if (step.name.includes('DepotMaintenance')) agentIcon = '🚍';
                else if (step.name.includes('PublicCommunication')) agentIcon = '⚠️';
                else if (step.name.includes('IncidentResolution')) agentIcon = '✅';
                else if (step.name.includes('InternalNotification')) agentIcon = '📨';
                else if (step.name.includes('PublicUpdate')) agentIcon = '📢';
                
                // Format the agent name to be more readable
                const formattedName = step.name
                    .replace(/([A-Z])/g, ' $1')
                    .replace(/^./, str => str.toUpperCase())
                    .trim();
                
                stepEl.innerHTML = `
                    <div class="step-header">
                        <span class="step-icon">${agentIcon}</span>
                        <span class="step-name">${formattedName}</span>
                        <span class="step-number">${index + 1}</span>
                    </div>
                    <div class="step-content">${step.content}</div>
                `;
                
                stepsContainer.appendChild(stepEl);
                
                // Add appearing animation with subtle bounce
                setTimeout(() => {
                    stepEl.style.transition = 'all 0.6s cubic-bezier(0.2, 0.8, 0.2, 1.0)';
                    stepEl.style.opacity = '1';
                    stepEl.style.transform = 'translateY(0)';
                }, 50);
                
                // Scroll the new step into view with smooth animation
                stepEl.scrollIntoView({ behavior: 'smooth', block: 'end' });
                
                // Add the typing indicator for the next step (if not the last step)
                if (index < steps.length - 1) {
                    stepsContainer.appendChild(typingIndicator);
                }
            }, index * stepDelay); // Exactly 1.5 seconds (1000) between each step
        });
    }
    
    // Optional: Sound effects for steps (can be implemented later)
    function playStepSound(stepIndex) {
        // This could be implemented with subtle UI sounds
        // Left as a placeholder for potential future enhancement
    }
    
    // Notification system
    function showNotification(message, type = "info") {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        // Animate out and remove
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 5000);
    }
    
    console.log("Metro Disruption Response System initialized ✓");
});