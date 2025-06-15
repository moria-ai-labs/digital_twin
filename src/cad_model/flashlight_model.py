import cadquery as cq

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
full_flashlight = flashlight_body.union(battery).union(led_bulb).union(switch).union(circuit)

# Export the model
output_filename = "full_flashlight.stl"
cq.exporters.export(full_flashlight, output_filename)

print(f"Full flashlight exported to {output_filename}")
print(f"Full flashlight bounding box: {full_flashlight.val().BoundingBox()}")
