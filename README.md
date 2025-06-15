# Flashlight CAD, Supply Chain, and Assembly Simulation

This project aims to estimate the impact of changes in the physical configuration of a product (a flashlight) on its supply chain and assembly methodology.

## Technology Stack

*   Python
*   CadQuery (for CAD as code)
*   SimPy (for discrete-event simulation: procurement and assembly)
*   Plotly Dash (for dashboarding)
*   CairoSVG (for converting SVG to PNG)

## Project Structure

*   `src/cad_model/flashlight_model.py`: Defines the flashlight's 3D model using CadQuery. Can be run to export an STL file, an SVG image, and a PNG image (via SVG conversion).
*   `src/simulation/procurement.py`: Simulates the procurement of flashlight components.
*   `src/simulation/assembly.py`: Simulates the assembly process of the flashlight and collects data for Gantt chart visualization.
*   `src/dashboard/app.py`: A Plotly Dash application to visualize simulation results, CAD models (SVG with PNG download), and assembly processes.
*   `tests/`: Contains unit tests for the project.
*   `assets/`: Stores static assets like the exported SVG and PNG images for the dashboard.
*   `requirements.txt`: Lists Python dependencies.

## Setup

1.  **Clone the repository.**
2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    **System Dependencies Note:**
    *   For **CadQuery SVG export** in headless environments, `Xvfb` might be needed (e.g., `sudo apt-get install -y xvfb`).
    *   The **CairoSVG** library, used for converting SVG to PNG, requires system libraries for Cairo. On Debian/Ubuntu, install them with: `sudo apt-get install -y libcairo2-dev`. Other systems will have different package names (e.g., `cairo` on macOS via Homebrew).

## How to Run

### Generate CAD Model Files

To generate the `full_flashlight.stl`, `flashlight_view.svg`, and `flashlight_view.png` files from the CAD model script directly:
```bash
# May require Xvfb for SVG export in headless environments:
# xvfb-run -a python3 src/cad_model/flashlight_model.py
python3 src/cad_model/flashlight_model.py
```
This will create/update the STL, SVG, and PNG files in the project root.

### Run Simulations (via Dashboard)

To run the simulations and view the dashboard:
```bash
python3 src/dashboard/app.py
```
Navigate to the URL provided (usually `http://127.0.0.1:8050/`) in your web browser.

The dashboard now features multiple tabs:
*   **Simulation Results**: Shows the main procurement (including scenario comparison) and assembly simulation summary outcomes. Click the "Run Simulations" button here to populate all simulation-dependent views.
*   **CAD Visualization**: Allows you to generate and view an SVG image of the flashlight model. Click the 'Generate/Refresh CAD View' button within this tab. The image is saved to the `assets/` folder, and a download link for a PNG version (converted from the SVG) will also appear.
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
