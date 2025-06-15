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

        # Verify Gantt data
        self.assertTrue(len(asm_sim.gantt_data) > 0, "Gantt data should not be empty")
        self.assertEqual(len(asm_sim.gantt_data), len(ASSEMBLY_STEPS_DATA), "Gantt data should have one entry per assembly step")

        for item in asm_sim.gantt_data:
            self.assertIn('Task', item, "Gantt item should have 'Task' key")
            self.assertIn('Start', item, "Gantt item should have 'Start' key")
            self.assertIn('Finish', item, "Gantt item should have 'Finish' key")
            self.assertIsInstance(item['Task'], str, "'Task' should be a string")
            self.assertIsInstance(item['Start'], (int, float), "'Start' should be a number")
            self.assertIsInstance(item['Finish'], (int, float), "'Finish' should be a number")
            self.assertTrue(item['Finish'] >= item['Start'], f"Finish time should be >= Start time for task {item['Task']}")
        # print(f"Assembly Test: Time - {asm_sim.total_assembly_time}, Gantt entries - {len(asm_sim.gantt_data)}")

if __name__ == '__main__':
    unittest.main()
