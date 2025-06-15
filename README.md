# Flashlight CAD, Supply Chain, and Assembly Simulation

This project aims to estimate the impact of changes in the physical configuration of a product (a flashlight) on its supply chain and assembly methodology.

## Technology Stack

*   Python
*   CadQuery (for CAD as code)
*   SimPy (for discrete-event simulation: procurement and assembly)
*   Plotly Dash (for dashboarding)

## Project Structure

*   `src/cad_model/flashlight_model.py`: Defines the flashlight's 3D model using CadQuery. Can be run to export an STL file.
*   `src/simulation/procurement.py`: Simulates the procurement of flashlight components.
*   `src/simulation/assembly.py`: Simulates the assembly process of the flashlight.
*   `src/dashboard/app.py`: A Plotly Dash application to visualize simulation results and impact of changes.
*   `tests/`: Contains unit tests for the project.
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

## How to Run

### Generate CAD Model

To generate the `full_flashlight.stl` file from the CAD model:
```bash
python src/cad_model/flashlight_model.py
```
This will create/update the STL file in the project root.

### Run Simulations (via Dashboard)

To run the simulations and view the dashboard:
```bash
python src/dashboard/app.py
```
Navigate to the URL provided (usually `http://127.0.0.1:8050/`) in your web browser. Click the "Run Simulations" button to see the results.

### Run Unit Tests

To run the unit tests:
```bash
python -m unittest discover tests/
```
Or run individual test files:
```bash
python -m unittest tests/test_simulation.py
python -m unittest tests/test_cad_model.py
```
