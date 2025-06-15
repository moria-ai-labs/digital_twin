# tests/test_simulation.py
import unittest
import simpy
import sys
import os

# Adjust Python path to include the root directory for src. module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.simulation.procurement import ProcurementSimulation, COMPONENTS_DATA
from src.simulation.assembly import AssemblySimulation, ASSEMBLY_STEPS_DATA

class TestSimulationModules(unittest.TestCase):

    def test_procurement_simulation(self):
        env = simpy.Environment()
        # Use the actual COMPONENTS_DATA imported from the module
        proc_sim = ProcurementSimulation(env, COMPONENTS_DATA)
        main_proc = env.process(proc_sim.run_simulation())
        env.run(until=main_proc)

        expected_total_cost = sum(d['cost'] for d in COMPONENTS_DATA.values())
        expected_max_lead_time = max(d['lead_time'] for d in COMPONENTS_DATA.values())

        self.assertEqual(proc_sim.total_cost, expected_total_cost)
        self.assertEqual(proc_sim.max_lead_time, expected_max_lead_time)
        # print(f"Procurement Test: Cost - {proc_sim.total_cost}, Time - {proc_sim.max_lead_time}")


    def test_assembly_simulation(self):
        env = simpy.Environment()
        # Use the actual ASSEMBLY_STEPS_DATA imported
        asm_sim = AssemblySimulation(env, ASSEMBLY_STEPS_DATA)
        main_proc = env.process(asm_sim.run_simulation())
        env.run(until=main_proc)

        expected_total_assembly_time = sum(s['duration'] for s in ASSEMBLY_STEPS_DATA)
        self.assertEqual(asm_sim.total_assembly_time, expected_total_assembly_time)
        # print(f"Assembly Test: Time - {asm_sim.total_assembly_time}")

if __name__ == '__main__':
    unittest.main()
