from fastapi import APIRouter,Body, Request, HTTPException
from fastapi.responses import JSONResponse
from planner.MetroPlanner import MetroPlanner
from config.llm_config import get_llm_config

router = APIRouter()
planner = MetroPlanner(llm_config=get_llm_config())

@router.post("/run/text", response_model=dict)
async def run_metro_task_text(text: str = Body(..., media_type="text/plain")):
    """
    POST /api/metro_task/run/text
    
    Processes a train disruption description as plain text and returns the response from all agents.
    
    Simply post the text description directly without JSON formatting.
    """
    try:
        if not text.strip():
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "Empty input text."}
            )
        
        # Run the workflow and get the structured response
        result = await planner.run(text)
        
        # Return the formatted result
        return result
        
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Internal error: {str(e)}"}
        )

@router.get("/debug")
async def debug_endpoint():
    """
    GET /api/metro_task/debug
    
    Simple endpoint to test if the API is working correctly.
    Returns a mock response in the same format as the real endpoint
    to help debug frontend issues.
    """
    # Return a mock response to test frontend rendering
    return {
        "status": "completed",
        "steps": [
            {
                "name": "TrainBreakdownAgent",
                "content": "🚨 Incident logged successfully at Redhill Station. Disruption response initiated."
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
                "content": "⚠️ Draft social media post: 'Service disruption on Red Line at Redhill Station. Shuttle buses are being arranged. We apologize for the inconvenience.'"
            },
            {
                "name": "IncidentResolutionAgent",
                "content": "✅ System check complete. No remaining disruptions detected. Ready to proceed with clearance notification."
            },
            {
                "name": "InternalNotificationAgent",
                "content": "📨 All internal teams notified of incident resolution. Acknowledged by: Control Room, Bus Ops, Maintenance."
            },
            {
                "name": "PublicUpdateAgent",
                "content": "📢 Public notice posted: 'Train services on the Red Line have resumed. Thank you for your patience.' Published on Twitter, Facebook, and IG."
            }
        ]
    }