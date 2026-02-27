import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path
import toml
from dtw_lab.lab1 import (
    read_csv_from_google_drive,
    visualize_data,
    calculate_statistic,
    clean_data,
)

# Initialize FastAPI application instance
# This creates our main application object that will handle all routing and middleware
app = FastAPI()

# Server deployment configuration function. We specify on what port we serve, and what IPs we listen to.
def run_server(port: int = 80, reload: bool = False, host: str = "127.0.0.1"):
    uvicorn.run("dtw_lab.lab2:app", port=port, reload=reload, host=host)

# Wrapper functions for script entry points
def run_server_dev():
    """Development server with hot reload on port 8000"""
    run_server(port=8000, reload=True)

def run_server_prod():
    """Production server on all interfaces"""
    run_server(reload=False, host='0.0.0.0')

# Define an entry point to our application.
@app.get("/")
def main_route():
    return {"message": "Hello world"}