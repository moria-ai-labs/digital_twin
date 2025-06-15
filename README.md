# Flashlight CAD, Supply Chain, and Assembly Simulation

This project aims to estimate the impact of changes in the physical configuration of a product (a flashlight) on its supply chain and assembly methodology.

## Technology Stack

*   Python
*   CadQuery (for CAD as code)
*   SimPy (for discrete-event simulation: procurement and assembly)
*   Plotly Dash (for dashboarding)

## Project Structure

*   `src/cad_model/flashlight_model.py`: Defines the flashlight's 3D model using CadQuery. Can be run to export an STL file and an SVG image.
*   `src/simulation/procurement.py`: Simulates the procurement of flashlight components.
*   `src/simulation/assembly.py`: Simulates the assembly process of the flashlight and collects data for Gantt chart visualization.
*   `src/dashboard/app.py`: A Plotly Dash application to visualize simulation results, CAD models, and assembly processes.
*   `tests/`: Contains unit tests for the project.
*   `assets/`: Stores static assets like the exported SVG image for the dashboard.
*   `requirements.txt`: Lists Python dependencies.

## Setup

1.  **Clone the repository.**
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    For CAD model image export, additional system dependencies might be required by CadQuery's underlying OCP backend, such as Xvfb for headless environments if direct export fails (e.g., `sudo apt-get install xvfb`).

## How to Run

### Generate CAD Model Files

To generate the `full_flashlight.stl` and `flashlight_view.svg` files from the CAD model script directly:
```bash
# May require Xvfb for SVG export in headless environments:
# xvfb-run -a python3 src/cad_model/flashlight_model.py
python3 src/cad_model/flashlight_model.py
```
This will create/update the STL and SVG files in the project root.

### Run Simulations (via Dashboard)

To run the simulations and view the dashboard:
```bash
python3 src/dashboard/app.py
```
Navigate to the URL provided (usually `http://127.0.0.1:8050/`) in your web browser.

The dashboard now features multiple tabs:
*   **Simulation Results**: Shows the main procurement (including scenario comparison) and assembly simulation summary outcomes. Click the "Run Simulations" button here to populate all simulation-dependent views.
*   **CAD Visualization**: Allows you to generate and view an SVG image of the flashlight model. Click the 'Generate/Refresh CAD View' button within this tab. The image is saved to the `assets/` folder.
*   **Assembly Visualization**: Displays a Gantt chart representing the steps and durations of the assembly process. This chart is populated after running simulations from the 'Simulation Results' tab.

### Run Unit Tests

To run the unit tests:
```bash
# May require Xvfb for CAD export tests in headless environments:
# xvfb-run -a python3 -m unittest discover tests/
python3 -m unittest discover tests/
```
Or run individual test files:
```bash
python3 -m unittest tests/test_simulation.py
python3 -m unittest tests/test_cad_model.py # This might require Xvfb
```
