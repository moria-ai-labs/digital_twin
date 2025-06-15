import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import simpy
import sys
import os

import base64
import time # For cache-busting image
import plotly.figure_factory as ff
import plotly.graph_objects as go

# Adjust Python path to include the root directory for src.simulation imports
# This is often needed when running scripts from subdirectories that import from other subdirectories
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.simulation.procurement import ProcurementSimulation, COMPONENTS_DATA as ORIGINAL_COMPONENTS_DATA
from src.simulation.assembly import AssemblySimulation, ASSEMBLY_STEPS_DATA
from src.cad_model.flashlight_model import get_full_flashlight_assembly, export_flashlight_image

# Define component data scenarios for impact reporting
COMPONENTS_DATA_SCENARIO_A = ORIGINAL_COMPONENTS_DATA

COMPONENTS_DATA_SCENARIO_B = {
    "handle": {"lead_time": 7, "cost": 5.0},
    "head": {"lead_time": 7, "cost": 3.0},
    "lens": {"lead_time": 5, "cost": 1.5},
    "battery": {"lead_time": 15, "cost": 3.0}, # More Expensive, Longer Lead Time Battery
    "led_bulb": {"lead_time": 5, "cost": 1.0},
    "switch": {"lead_time": 5, "cost": 0.5},
    "circuit": {"lead_time": 12, "cost": 4.0},
}


# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Flashlight Supply Chain Dashboard"

# Define the app layout
app.layout = html.Div(children=[
    html.H1(children="Flashlight Supply Chain & Assembly Dashboard"),
    dcc.Tabs(id="tabs-main", value='tab-sim-results', children=[
        dcc.Tab(label='Simulation Results', value='tab-sim-results', children=[
            html.Div([
                html.Button('Run Simulations', id='run-button', n_clicks=0),
                html.Hr(),

                html.H2(children="Procurement Simulation Results"),

                html.H3(children="Scenario A: Standard Components"),
                dcc.Markdown(id='procurement-cost-a', children="Click 'Run Simulations' to see results."),
                dcc.Markdown(id='procurement-time-a', children=""),
                html.Br(),

                html.H3(children="Scenario B: Modified Battery (Higher Cost & Lead Time)"),
                dcc.Markdown(id='procurement-cost-b', children="Click 'Run Simulations' to see results."),
                dcc.Markdown(id='procurement-time-b', children=""),
                html.Hr(),

                html.H2(children="Assembly Simulation Results"),
                dcc.Markdown(id='assembly-time', children="Click 'Run Simulations' to see results. (Assembly is independent of procurement changes shown above)"),
            ])
        ]),
        dcc.Tab(label='CAD Visualization', value='tab-cad-vis', children=[
            html.Div([
                html.H3("CAD Model Visualization"),
                html.Button("Generate/Refresh CAD View", id="btn-generate-cad-view", n_clicks=0),
                html.Img(id="img-cad-visualization", style={'maxWidth': '100%', 'height': 'auto', 'marginTop': '20px'})
            ])
        ]),
        dcc.Tab(label='Assembly Visualization', value='tab-asm-vis', children=[
            html.Div([
                html.H3("Assembly Process Gantt Chart"),
                dcc.Graph(id='gantt-assembly-visualization')
            ])
        ]),
    ])
])

# Define the main callback for simulation results and assembly Gantt chart
@app.callback(
    [Output('procurement-cost-a', 'children'),
     Output('procurement-time-a', 'children'),
     Output('procurement-cost-b', 'children'),
     Output('procurement-time-b', 'children'),
     Output('assembly-time', 'children'),
     Output('gantt-assembly-visualization', 'figure')], # New output for Gantt chart
    [Input('run-button', 'n_clicks')]
)
def update_simulation_results(n_clicks):
    if n_clicks == 0:
        default_text = "Click 'Run Simulations' to see results."
        # Empty figure for Gantt chart initially
        empty_gantt = go.Figure().update_layout(title_text='Run simulation to see Gantt chart', xaxis_visible=False, yaxis_visible=False)
        return default_text, "", default_text, "", default_text, empty_gantt

    # Procurement Simulation - Scenario A
    proc_env_a = simpy.Environment()
    proc_sim_a = ProcurementSimulation(proc_env_a, COMPONENTS_DATA_SCENARIO_A)
    proc_main_process_a = proc_env_a.process(proc_sim_a.run_simulation())
    proc_env_a.run(until=proc_main_process_a)

    proc_cost_a_text = f"**Total Procurement Cost (Scenario A):** ${proc_sim_a.total_cost:.2f}"
    proc_time_a_text = f"**Overall Lead Time (Scenario A):** {proc_sim_a.max_lead_time} days"

    # Procurement Simulation - Scenario B
    proc_env_b = simpy.Environment()
    proc_sim_b = ProcurementSimulation(proc_env_b, COMPONENTS_DATA_SCENARIO_B)
    proc_main_process_b = proc_env_b.process(proc_sim_b.run_simulation())
    proc_env_b.run(until=proc_main_process_b)

    proc_cost_b_text = f"**Total Procurement Cost (Scenario B):** ${proc_sim_b.total_cost:.2f}"
    proc_time_b_text = f"**Overall Lead Time (Scenario B):** {proc_sim_b.max_lead_time} days"

    # Assembly Simulation
    asm_env = simpy.Environment()
    asm_sim = AssemblySimulation(asm_env, ASSEMBLY_STEPS_DATA)
    asm_main_process = asm_env.process(asm_sim.run_simulation())
    asm_env.run(until=asm_main_process)

    asm_time_text = f"**Total Assembly Time:** {asm_sim.total_assembly_time} minutes"

    # Create Gantt Chart for Assembly
    if asm_sim.gantt_data:
        # Convert SimPy simulation time (float) to datetime for ff.create_gantt if needed,
        # but ff.create_gantt can handle numeric Start/Finish if they represent time units.
        # For this project, SimPy time is in minutes or days, which are direct numerical values.
        # ff.create_gantt requires 'Start' and 'Finish' to be date strings or datetime objects
        # if using default time formatting. If they are simple numbers (like SimPy time),
        # it might work directly or require specific formatting.
        # Let's assume direct numerical values work or ff handles them appropriately for non-datetime axes.
        # For actual dates, conversion would be:
        # from datetime import datetime, timedelta
        # df['Start'] = df['Start'].apply(lambda x: (datetime.now() + timedelta(minutes=x)).strftime("%Y-%m-%d %H:%M:%S"))
        # df['Finish'] = df['Finish'].apply(lambda x: (datetime.now() + timedelta(minutes=x)).strftime("%Y-%m-%d %H:%M:%S"))
        # However, since our simulation times are relative (0 to N minutes/days), we can use them as is.
        # Plotly might treat them as milliseconds if not specified, so it's good to be mindful.
        # For ff.create_gantt, if Start/Finish are numbers, it plots them on a numerical axis.

        fig_gantt = ff.create_gantt(
            asm_sim.gantt_data,
            # colors='Viridis', # Example color scale
            index_col='Task', # Groups tasks by this column if group_tasks is True
            show_colorbar=True,
            group_tasks=False, # Set to False if 'Task' is unique per bar as in this sequential case
            title='Assembly Process Steps'
        )
        fig_gantt.update_layout(xaxis_title='Time (minutes)') # Assuming time unit is minutes from simulation
    else:
        fig_gantt = go.Figure().update_layout(title_text='No assembly data to display Gantt chart', xaxis_visible=False, yaxis_visible=False)

    return proc_cost_a_text, proc_time_a_text, proc_cost_b_text, proc_time_b_text, asm_time_text, fig_gantt

# Define the callback for CAD visualization
@app.callback(
    Output('img-cad-visualization', 'src'),
    [Input('btn-generate-cad-view', 'n_clicks')]
)
def update_cad_visualization(n_clicks):
    if n_clicks == 0:
        return "" # No image initially, or a placeholder path

    # Define path within assets folder
    # Ensure the assets folder exists (it should have been created by a previous step or manually)
    assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir) # Should not be strictly necessary if created before

    output_svg_path = os.path.join(assets_dir, "flashlight_view.svg")

    # Generate the CAD model assembly
    flashlight_assembly = get_full_flashlight_assembly()

    # Export the SVG image
    # The export_flashlight_image function prints to console, which is fine for now.
    export_flashlight_image(flashlight_assembly, output_path=output_svg_path)

    # Return the path to the image in the assets folder with a cache-busting query string
    # Dash serves files from the 'assets' folder automatically at '/assets/filename'
    return f"/assets/flashlight_view.svg?t={time.time()}"


# Standard Dash app execution line
if __name__ == '__main__':
    # Note: When running locally, Dash server will typically be on http://127.0.0.1:8050/
    # The server needs to be stopped manually (e.g., Ctrl+C in the terminal)
    app.run(debug=True)
