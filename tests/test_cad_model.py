# tests/test_cad_model.py
import unittest
import sys
import os
import cadquery as cq

# Adjust Python path to include the root directory for src. module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.cad_model.flashlight_model import get_full_flashlight_assembly, export_flashlight_image

class TestCadModel(unittest.TestCase):
    def test_import_model_module(self): # Renamed for clarity
        try:
            from src.cad_model import flashlight_model # Keep this to ensure module itself is importable
            self.assertTrue(True, "Successfully imported flashlight_model module")
        except ImportError as e:
            self.fail(f"Failed to import flashlight_model module: {e}")

    def test_get_full_flashlight_assembly(self):
        assembly = get_full_flashlight_assembly()
        self.assertIsNotNone(assembly, "Assembly should not be None")
        # A Workplane object containing a Solid is a common return type after chained operations
        self.assertIsInstance(assembly, (cq.Workplane, cq.Shape), "Should return a CadQuery Workplane or Shape")

    def test_export_flashlight_image(self):
        assembly = get_full_flashlight_assembly()
        test_svg_path = "test_flashlight_view.svg"

        # Ensure file does not exist before test if cleanup failed previously
        if os.path.exists(test_svg_path):
            os.remove(test_svg_path)

        export_flashlight_image(assembly, output_path=test_svg_path)

        self.assertTrue(os.path.exists(test_svg_path), f"SVG file should be created at {test_svg_path}")

        with open(test_svg_path, 'r') as f:
            content = f.read()

        self.assertTrue(len(content) > 0, "SVG file content should not be empty")

        stripped_content = content.strip()
        # Check if it starts with <?xml ...> <svg ...> or just <svg ...>
        starts_correctly = stripped_content.startswith("<svg") or \
                           (stripped_content.startswith("<?xml") and "<svg" in stripped_content[:100]) # Check <svg in first 100 chars
        ends_correctly = "</svg>" in stripped_content # Check if closing tag is present anywhere

        is_valid_svg = starts_correctly and ends_correctly

        if not is_valid_svg:
            print(f"SVG content unexpected. Starts correctly: {starts_correctly}, Ends correctly: {ends_correctly}. First 100 chars: '{stripped_content[:100]}'. Last 100 chars: '{stripped_content[-100:]}'")
        self.assertTrue(is_valid_svg, "Content should be valid SVG")

        # Clean up the created file
        if os.path.exists(test_svg_path):
            os.remove(test_svg_path)

    # Add a placeholder for more complex tests later (can be kept or removed if other tests are sufficient)
    def test_placeholder_for_geometry(self):
        self.assertTrue(True, "Placeholder for future geometry verification")


if __name__ == '__main__':
    unittest.main()
