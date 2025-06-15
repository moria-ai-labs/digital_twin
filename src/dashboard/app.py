import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import simpy
import sys
import os

# Adjust Python path to include the root directory for src.simulation imports
# This is often needed when running scripts from subdirectories that import from other subdirectories
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.simulation.procurement import ProcurementSimulation, COMPONENTS_DATA as ORIGINAL_COMPONENTS_DATA
from src.simulation.assembly import AssemblySimulation, ASSEMBLY_STEPS_DATA

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

# Define the callback to update simulation results
@app.callback(
    [Output('procurement-cost-a', 'children'),
     Output('procurement-time-a', 'children'),
     Output('procurement-cost-b', 'children'),
     Output('procurement-time-b', 'children'),
     Output('assembly-time', 'children')],
    [Input('run-button', 'n_clicks')]
)
def update_simulation_results(n_clicks):
    if n_clicks == 0:
        default_text = "Click 'Run Simulations' to see results."
        return default_text, "", default_text, "", default_text # Return for all five outputs

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

    # Assembly Simulation (remains the same for both scenarios in this example)
    asm_env = simpy.Environment()
    asm_sim = AssemblySimulation(asm_env, ASSEMBLY_STEPS_DATA)
    asm_main_process = asm_env.process(asm_sim.run_simulation())
    asm_env.run(until=asm_main_process)

    asm_time_text = f"**Total Assembly Time:** {asm_sim.total_assembly_time} minutes"

    return proc_cost_a_text, proc_time_a_text, proc_cost_b_text, proc_time_b_text, asm_time_text

# Standard Dash app execution line
if __name__ == '__main__':
    # Note: When running locally, Dash server will typically be on http://127.0.0.1:8050/
    # The server needs to be stopped manually (e.g., Ctrl+C in the terminal)
    app.run_server(debug=True)
