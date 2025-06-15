import cadquery as cq

import cadquery as cq

def get_full_flashlight_assembly():
    # Define parameters for the flashlight components
    handle_length = 50.0
    handle_diameter = 20.0
    head_length = 20.0
    head_diameter = 30.0
    lens_thickness = 5.0
    lens_diameter = 25.0

    # --- New component parameters ---
    battery_diameter = handle_diameter * 0.8
    battery_length = handle_length * 0.9
    led_diameter = lens_diameter * 0.5
    led_length = lens_thickness * 1.5 # Making it slightly longer than lens is thick
    switch_width = handle_diameter * 0.3
    switch_length = handle_diameter * 0.5 # Length along the handle
    switch_thickness = 5.0 # How much it sticks out
    circuit_diameter = head_diameter * 0.8
    circuit_thickness = 2.0

    # Create the handle
    handle = (
        cq.Workplane("XY")
        .cylinder(handle_length, handle_diameter / 2.0)
    )

    # Create the head
    head = (
        cq.Workplane("XY")
        .cylinder(head_length, head_diameter / 2.0)
        .translate((0, 0, handle_length))
    )

    # Create the lens
    lens = (
        cq.Workplane("XY")
        .cylinder(lens_thickness, lens_diameter / 2.0)
        .translate((0, 0, handle_length + head_length))
    )

    # --- Create new components ---
    # Battery: Centered inside the handle
    battery = (
        cq.Workplane("XY")
        .cylinder(battery_length, battery_diameter / 2.0)
        .translate((0, 0, (handle_length - battery_length) / 2.0 + battery_length / 2.0)) # Centered along Z in handle
    )

    # LED Bulb: Positioned at the front part of the head
    led_bulb = (
        cq.Workplane("XY")
        .cylinder(led_length, led_diameter / 2.0)
        .translate((0, 0, handle_length + head_length + (lens_thickness / 2.0) - (led_length / 2.0) )) # Centered in lens depth
    )

    # Switch: Positioned on the outer surface of the handle
    # Assuming Z is up, X is right, Y is forward for the handle. Switch on +Y side.
    switch = (
        cq.Workplane("XZ") # Workplane for switch body
        .box(switch_length, switch_thickness, switch_width) # length, thickness(height from handle), width
        .rotate((0,0,0),(0,0,1),90) # Rotate to align length along handle Z
        .translate((0, (handle_diameter / 2.0) + (switch_thickness / 2.0), handle_length * 0.75))
    )

    # Circuit: Thin disk inside the head, behind the LED
    circuit = (
        cq.Workplane("XY")
        .cylinder(circuit_thickness, circuit_diameter / 2.0)
        .translate((0, 0, handle_length + head_length - circuit_thickness / 2.0)) # Just behind the lens plane
    )

    # Combine the body components
    flashlight_body = handle.union(head).union(lens)

    # Combine all components for the full flashlight
    full_flashlight_solid = flashlight_body.union(battery).union(led_bulb).union(switch).union(circuit)

    # Return the combined solid directly
    return full_flashlight_solid

# --- SVG Export Function ---
def export_flashlight_image(assembly, output_path="flashlight_view.svg", img_width=800, img_height=600, projection_dir=(1,1,1)):
    """
    Exports a CadQuery assembly to an SVG image.
    """
    print(f"Exporting SVG image to {output_path}...")
    try:
        options = {
            'projectionDir': projection_dir,
            'showAxes': False,
            'showHidden': False, # Typically false for a clean SVG, unless hidden lines are desired
            'width': float(img_width),   # Viewport width
            'height': float(img_height),  # Viewport height
            'marginLeft': 20.0,
            'marginTop': 20.0,
            # 'strokeWidth': 0.1, # Thinner lines for detail. Default is usually fine.
            # 'strokeColor': (0,0,0), # Black lines, default
            # 'hiddenColor': (100,100,100), # Color for hidden lines if showHidden=True
            # 'showOutline': True, # Default
            # 'showHidden': False, # Default
        }
        cq.exporters.export(
            assembly,
            output_path,
            exportType='SVG',
            opt=options
        )
        print(f"SVG Image successfully exported to {output_path}")
    except Exception as e:
        print(f"Error exporting SVG image: {e}")

if __name__ == "__main__":
    # This block is executed when the script is run directly.
    # It will perform the STL export defined above and then the SVG export.

    flashlight_assembly = get_full_flashlight_assembly()

    # Export the STL model
    output_filename_stl = "full_flashlight.stl"
    cq.exporters.export(flashlight_assembly, output_filename_stl)
    print(f"Full flashlight exported to {output_filename_stl}")
    print(f"Full flashlight bounding box: {flashlight_assembly.val().BoundingBox()}")

    # Call the SVG export function for the full_flashlight assembly
    export_flashlight_image(flashlight_assembly, output_path="flashlight_view.svg")
