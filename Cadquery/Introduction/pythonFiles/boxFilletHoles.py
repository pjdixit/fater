# Import necessary module
from cadquery import Workplane

# Define parameters
length = 5.0
width = 3.0
height = 2.0
hole_diameter = 0.5
fillet_radius = 0.2
large_hole_diameter = 1.0

# Create a rectangular prism (box) with the given dimensions
result = Workplane("front").box(length, width, height)

# Add fillets to all edges
result = result.edges().fillet(fillet_radius)

# Select the top face and create a circular hole at the center
result = result.faces(">Z").workplane().hole(hole_diameter)

# Create a larger hole offset from the center
result = result.faces(">Z").workplane(offset=(length / 4, 0)).hole(large_hole_diameter)

# Output the final result
show_object(result)
