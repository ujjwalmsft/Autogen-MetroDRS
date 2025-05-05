"""
main.py

Main FastAPI application for the Metro Multi-Agent Response System.
- Registers the API route (/api/metro_task/run)
- Serves the frontend UI (index.html)
- Mounts static assets (JS/CSS)
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api.routers import metro_task_router

# Initialize FastAPI app
app = FastAPI(
    title="Metro Disruption Response System",
    description="Uses AutoGen v0.5.6 multi-agent coordination",
    version="1.0.0"
)

# Set up Jinja2 templates and static assets
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Register the API router
app.include_router(metro_task_router.router, prefix="/api/metro_task")

# Serve frontend at root URL
@app.get("/", response_class=HTMLResponse)
async def serve_frontend(request: Request):
    """
    GET /

    Returns the HTML frontend UI for metro response simulation.
    """
    return templates.TemplateResponse("index.html", {"request": request})
