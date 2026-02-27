import uvicorn
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import FileResponse, HTMLResponse
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
DATA_FILE_ID = "1eKiAZKbWTnrcGs3bqdhINo1E4rBBpglo"

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
@app.get("/", response_class=HTMLResponse)
def main_route():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>DTW Lab API</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; }
            h1 { margin-bottom: 0.5rem; }
            .section { margin-top: 1.5rem; padding: 1rem; border: 1px solid #ddd; border-radius: 8px; }
            .buttons { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.75rem; }
            a.button {
                display: inline-block;
                padding: 0.6rem 1rem;
                border-radius: 6px;
                border: 1px solid #bbb;
                text-decoration: none;
                color: #111;
                background: #f5f5f5;
            }
            a.button:hover { background: #ececec; }
            .hint { color: #555; font-size: 0.95rem; }
        </style>
    </head>
    <body>
        <h1>DTW Lab API</h1>
        <p class="hint">Accesos rápidos a los endpoints principales.</p>

        <div class="section">
            <h2>Version</h2>
            <div class="buttons">
                <a class="button" href="/version">GET /version</a>
            </div>
        </div>

        <div class="section">
            <h2>Statistic</h2>
            <p class="hint">Columna de ejemplo: Charge_Left_Percentage</p>
            <div class="buttons">
                <a class="button" href="/statistic/mean/Charge_Left_Percentage">GET mean</a>
                <a class="button" href="/statistic/median/Charge_Left_Percentage">GET median</a>
                <a class="button" href="/statistic/mode/Charge_Left_Percentage">GET mode</a>
            </div>
        </div>

        <div class="section">
            <h2>Visualization</h2>
            <div class="buttons">
                <a class="button" href="/visualization/scatter">GET scatter</a>
                <a class="button" href="/visualization/box">GET box</a>
                <a class="button" href="/visualization/hist">GET hist</a>
            </div>
        </div>

        <div class="section">
            <h2>Documentación</h2>
            <div class="buttons">
                <a class="button" href="/docs">Swagger UI</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/statistic/{measure}/{column}")
def get_statistic(measure: str, column: str):
    # Read the CSV data, clean the data, and calculate the statistic.
    df = read_csv_from_google_drive(DATA_FILE_ID)
    df = clean_data(df)

    allowed_measures = {"mean", "median", "mode"}
    if measure not in allowed_measures:
        raise HTTPException(status_code=400, detail="Invalid measure. Use mean, median, or mode.")

    if column not in df.columns:
        raise HTTPException(status_code=404, detail=f"Column '{column}' not found")

    statistic = calculate_statistic(measure, df[column])
    if measure == "mode" and statistic is None:
        statistic = df[column].mode()[0]

    return {
        "measure": measure,
        "column": column,
        "value": statistic,
    }

@app.get("/visualize/{graph_type}")
@app.get("/visualization/{graph_type}")
def get_visualization(graph_type: str):
    # Read the CSV data, clean the data, and visualize it.
    # This should create 3 files in the graphs folder.
    # Based on the graph_type input, return the corresponding image
    # HINT: Use FileResponse
    df = read_csv_from_google_drive(DATA_FILE_ID)
    df = clean_data(df)

    graphs_folder = Path("graphs")
    graphs_folder.mkdir(parents=True, exist_ok=True)
    visualize_data(df)

    graph_files = {
        "scatter": graphs_folder / "scatter_plots.png",
        "scatter_plots": graphs_folder / "scatter_plots.png",
        "box": graphs_folder / "boxplots.png",
        "boxplots": graphs_folder / "boxplots.png",
        "hist": graphs_folder / "histograms.png",
        "histograms": graphs_folder / "histograms.png",
    }

    selected_file = graph_files.get(graph_type)
    if selected_file is None:
        raise HTTPException(status_code=400, detail="Invalid graph type. Use scatter, box, or hist.")

    if not selected_file.exists():
        raise HTTPException(status_code=500, detail="Graph file was not generated")

    return FileResponse(path=selected_file)

@app.get("/version")
def get_visualization_version():
    # Using the toml library, get the version field from the "pyproject.toml" file and return it.
    pyproject_path = Path(__file__).resolve().parents[2] / "pyproject.toml"
    if not pyproject_path.exists():
        raise HTTPException(status_code=500, detail="pyproject.toml not found")

    project_data = toml.load(pyproject_path)
    version = project_data.get("project", {}).get("version")
    if version is None:
        raise HTTPException(status_code=500, detail="Version not found in pyproject.toml")

    return {"version": version}