"""
metro_task_router.py

API route for initiating the metro multi-agent response workflow.
Calls the updated MetroPlanner (AutoGen v0.5.6) and returns agent responses.
"""

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from planner.MetroPlanner import MetroPlanner
from config.llm_config import get_llm_config

# Create the router instance
router = APIRouter()

# Instantiate the planner (with config from .env)
planner = MetroPlanner(llm_config=get_llm_config())

@router.post("/run")
async def run_metro_task(request: Request):
    """
    POST /api/metro_task/run

    Request JSON:
    {
        "input": "Train breakdown at Redhill Station"
    }

    Response JSON:
    {
        "status": "completed",
        "steps": [
            {
                "role": "assistant",
                "name": "TrainBreakdownAgent",
                "content": "Incident logged..."
            },
            ...
        ]
    }
    """
    try:
        body = await request.json()
        input_text = body.get("input", "").strip()

        if not input_text:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "Missing or empty 'input' field."}
            )

        # Run the planner (GroupChatManager based)
        steps = await planner.run(input_text)

        return {
            "status": "completed",
            "steps": steps
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Internal error: {str(e)}"}
        )
