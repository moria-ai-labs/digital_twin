import simpy

# Define assembly steps and their durations (in minutes for this example)
ASSEMBLY_STEPS_DATA = [
    {"name": "Attach head to handle", "duration": 5},
    {"name": "Insert battery into handle", "duration": 2},
    {"name": "Place LED bulb into head", "duration": 3},
    {"name": "Fix switch onto handle", "duration": 4},
    {"name": "Install circuit into head", "duration": 5},
    {"name": "Attach lens to head", "duration": 3},
]

# For simplicity, assume a single assembly worker/station for now.
# Later, this could be expanded with resources (e.g., simpy.Resource).

class AssemblySimulation:
    def __init__(self, env, assembly_steps):
        self.env = env
        self.assembly_steps = assembly_steps
        self.total_assembly_time = 0
        self.assembly_log = []
        self.gantt_data = [] # For Gantt chart data collection

    def perform_step(self, step_name, duration):
        '''Simulates a single assembly step.'''
        start_time = self.env.now
        print(f"{self.env.now:.2f}: Starting: {step_name}")
        self.assembly_log.append(f"{self.env.now:.2f}: Starting: {step_name}")

        yield self.env.timeout(duration)

        finish_time = self.env.now
        print(f"{self.env.now:.2f}: Finished: {step_name} (Took: {duration} mins)")
        self.assembly_log.append(f"{self.env.now:.2f}: Finished: {step_name} (Took: {duration} mins)")
        self.total_assembly_time += duration
        self.gantt_data.append(dict(
            Task=step_name,
            Start=start_time,
            Finish=finish_time,
            # Optional: Resource='Worker 1' # Placeholder if resources are added
        ))

    def run_simulation(self):
        '''Runs the assembly simulation for all steps sequentially.'''
        print(f"--- Starting Assembly Simulation ---")
        self.assembly_log = [f"{self.env.now:.2f}: --- Starting Assembly Simulation ---"] # Reset log
        self.gantt_data = [] # Reset Gantt data for the run
        self.total_assembly_time = 0 # Reset for the run

        for step in self.assembly_steps:
            # In a sequential process, each step must complete before the next.
            # So, we 'yield' the process directly.
            yield self.env.process(self.perform_step(step["name"], step["duration"]))

        print(f"--- Assembly Simulation Finished ---")
        print(f"Total Assembly Time: {self.total_assembly_time} minutes")
        self.assembly_log.append(f"--- Assembly Simulation Finished ---")
        self.assembly_log.append(f"Total Assembly Time: {self.total_assembly_time} minutes")

# Example of how to run the simulation
if __name__ == "__main__":
    env = simpy.Environment()
    assembly_sim = AssemblySimulation(env, ASSEMBLY_STEPS_DATA)

    # Run the main simulation process
    main_process = env.process(assembly_sim.run_simulation())
    env.run(until=main_process) # Run until the assembly simulation process is done

    print("\nFinal Log:")
    for entry in assembly_sim.assembly_log:
        print(entry)
    print(f"Final Calculated Total Assembly Time: {assembly_sim.total_assembly_time} minutes")

    print("\nCollected Gantt Data:")
    for item in assembly_sim.gantt_data:
        print(item)
