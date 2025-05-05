from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from planner.MetroPlanner import MetroPlanner
import asyncio
import traceback

router = APIRouter(prefix="/api/metro_task", tags=["metro_task"])

# Input model for text-based tasks
class MetroTaskTextInput(BaseModel):
    text: str

# Output model for task results  
class Step(BaseModel):
    name: str
    content: str

class MetroTaskResult(BaseModel):
    status: str
    message: Optional[str] = None
    steps: List[Step]

# Dependency to get a MetroPlanner instance
def get_planner():
    return MetroPlanner()

@router.post("/run/text", response_model=MetroTaskResult)
async def run_task_text(task: MetroTaskTextInput, planner: MetroPlanner = Depends(get_planner)):
    """Run the metro task planner with a text input"""
    try:
        print(f"Running metro task with input: {task.text}")
        result = await planner.run(task.text)
        print(f"Task completed with status: {result['status']}")
        return result
    except Exception as e:
        print(f"Error in task: {str(e)}")
        traceback.print_exc()
        return {
            "status": "error",
            "message": f"Server error: {str(e)}",
            "steps": []
        }

# New route that just returns fallback steps without running the full workflow
@router.post("/fallback/text", response_model=MetroTaskResult)
async def get_fallback_steps(task: MetroTaskTextInput, planner: MetroPlanner = Depends(get_planner)):
    """
    Get the fallback steps for a metro task input without running the full LLM workflow.
    This is useful for testing or when the LLM service is unavailable.
    """
    try:
        print(f"Generating fallback steps for: {task.text}")
        # Generate fallback steps directly using the planner's method
        fallback_steps = planner._generate_fallback_steps(task.text)
        
        return {
            "status": "completed",
            "message": "Using fallback response",
            "steps": fallback_steps
        }
    except Exception as e:
        print(f"Error generating fallback steps: {str(e)}")
        traceback.print_exc()
        return {
            "status": "error",
            "message": f"Server error generating fallback: {str(e)}",
            "steps": []
        }