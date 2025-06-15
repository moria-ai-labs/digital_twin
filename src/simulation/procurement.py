import simpy

# Define component data (name, lead_time_days, cost_usd)
# For now, these are hardcoded. Later, they could come from the CAD model or a database.
COMPONENTS_DATA = {
    "handle": {"lead_time": 7, "cost": 5.0},
    "head": {"lead_time": 7, "cost": 3.0},
    "lens": {"lead_time": 5, "cost": 1.5},
    "battery": {"lead_time": 10, "cost": 2.0},
    "led_bulb": {"lead_time": 5, "cost": 1.0},
    "switch": {"lead_time": 5, "cost": 0.5},
    "circuit": {"lead_time": 12, "cost": 4.0},
}

class ProcurementSimulation:
    def __init__(self, env, components_data):
        self.env = env
        self.components_data = components_data
        self.total_cost = 0
        self.max_lead_time = 0
        self.procurement_log = [] # To store events

    def procure_component(self, component_name, data):
        '''Simulates the procurement of a single component.'''
        print(f"{self.env.now:.2f}: Ordering {component_name}")
        self.procurement_log.append(f"{self.env.now:.2f}: Ordering {component_name}")

        yield self.env.timeout(data["lead_time"])

        print(f"{self.env.now:.2f}: Received {component_name} (Cost: ${data['cost']:.2f})")
        self.procurement_log.append(f"{self.env.now:.2f}: Received {component_name} (Cost: ${data['cost']:.2f})")
        self.total_cost += data["cost"]
        # Note: self.max_lead_time is set in run_simulation before processes start
        # to reflect the planned duration. If we wanted actual longest process time,
        # we could update it here as well, but the current logic is for overall expected time.

    def run_simulation(self):
        '''Runs the procurement simulation for all components.'''
        # This is a generator function.

        self.total_cost = 0
        self.max_lead_time = 0 # Reset for the run
        self.procurement_log = [f"{self.env.now:.2f}: --- Starting Procurement Simulation ---"]
        print(f"{self.env.now:.2f}: --- Starting Procurement Simulation ---")

        procurement_events = []
        for name, data in self.components_data.items():
            procurement_events.append(self.env.process(self.procure_component(name, data)))
            if data["lead_time"] > self.max_lead_time:
                 self.max_lead_time = data["lead_time"]

        yield self.env.all_of(procurement_events) # Wait for all procurement events to complete

        print(f"{self.env.now:.2f}: --- Procurement Simulation Finished ---")
        print(f"{self.env.now:.2f}: Total Procurement Cost: ${self.total_cost:.2f}")
        print(f"{self.env.now:.2f}: Overall Lead Time (longest component lead time): {self.max_lead_time} days")
        self.procurement_log.append(f"{self.env.now:.2f}: --- Procurement Simulation Finished ---")
        self.procurement_log.append(f"{self.env.now:.2f}: Total Procurement Cost: ${self.total_cost:.2f}")
        self.procurement_log.append(f"{self.env.now:.2f}: Overall Lead Time: {self.max_lead_time} days")

# Example of how to run the simulation
if __name__ == "__main__":
    env = simpy.Environment()
    proc_sim = ProcurementSimulation(env, COMPONENTS_DATA)

    main_process = env.process(proc_sim.run_simulation())
    env.run(until=main_process) # Run until the main simulation process is done

    print("\nFinal Log (from procurement_log list):")
    for entry in proc_sim.procurement_log:
        print(entry)

    # These print statements are for verification against the log and internal state
    print(f"\nFinal Calculated Cost (from instance variable): ${proc_sim.total_cost:.2f}")
    print(f"Final Max Lead Time (from instance variable): {proc_sim.max_lead_time} days")
