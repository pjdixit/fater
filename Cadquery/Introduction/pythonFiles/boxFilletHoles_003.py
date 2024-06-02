import cadquery as cq

# Define parameters
base_height = 60.0
base_width = 100.0
base_thickness = 10.0
hole_diameter = 15.0
fillet_radius = 5.0
extrusion_height = 30.0

# Create base box
base = cq.Workplane("XY").box(base_width, base_height, base_thickness)

# Create hole
hole = cq.Workplane("XY").circle(hole_diameter / 2).extrude(base_thickness)

# Subtract hole from base
bracket = base.cut(hole)

# Fillet edges
bracket = bracket.edges("|Z").fillet(fillet_radius)

# Create extrusion
extrusion = cq.Workplane("XY").box(base_width, base_height / 2, extrusion_height).translate((0, 0, base_thickness + extrusion_height / 2))

# Combine base and extrusion
result = bracket.union(extrusion)

# Render the solid
show_object(result)
