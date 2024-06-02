import cadquery as cq

# Parameters from Grasshopper sliders and panel
radius = 12
length = 12
factor = 12
count = 10

# Create a cone
base_center = (0, 0, 0)
tip_center = (0, 0, length)
cone = cq.Solid.makeCone(radius, 0, length)

# Move the cone along the X-axis
unit_vector = (factor, 0, 0)
moved_cone = cone.translate(unit_vector)

# Create a polar array of the moved cone
polar_array = []
angle_step = 360 / count

for i in range(count):
    angle = angle_step * i
    rotation = cq.Location(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), angle)
    polar_array.append(moved_cone.moved(rotation))

# Combine all instances in the polar array into one object
result = cq.Workplane("XY")
for instance in polar_array:
    result = result.union(instance)

# Display the result
show_object(result)
