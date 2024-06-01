import cadquery as cq
import numpy as np
import os

# Parameters
length = 100
width = 60
height = 40
num_u = 20
num_v = 20


# Create the parametric surface function
def saddle_surface(u, v):
    x = length * (u - 0.5)
    y = width * (v - 0.5)
    z = (x**2 / length**2 - y**2 / width**2) * height
    return (x, y, z)


# Generate grid points
u_values = np.linspace(0, 1, num_u)
v_values = np.linspace(0, 1, num_v)

# Create the frame structure
frame = cq.Workplane("XY")

# Add horizontal and vertical grid lines
for i in range(num_u):
    for j in range(num_v):
        p1 = saddle_surface(u_values[i], v_values[j])
        if i < num_u - 1:
            p2 = saddle_surface(u_values[i + 1], v_values[j])
            frame = frame.add(cq.Edge.makeLine(cq.Vector(*p1), cq.Vector(*p2)))
        if j < num_v - 1:
            p3 = saddle_surface(u_values[i], v_values[j + 1])
            frame = frame.add(cq.Edge.makeLine(cq.Vector(*p1), cq.Vector(*p3)))

# Create surface panels by creating wires and lofting them
for i in range(num_u - 1):
    for j in range(num_v - 1):
        p1 = saddle_surface(u_values[i], v_values[j])
        p2 = saddle_surface(u_values[i + 1], v_values[j])
        p3 = saddle_surface(u_values[i + 1], v_values[j + 1])
        p4 = saddle_surface(u_values[i], v_values[j + 1])
        wire = cq.Wire.assembleEdges(
            [
                cq.Edge.makeLine(cq.Vector(*p1), cq.Vector(*p2)),
                cq.Edge.makeLine(cq.Vector(*p2), cq.Vector(*p3)),
                cq.Edge.makeLine(cq.Vector(*p3), cq.Vector(*p4)),
                cq.Edge.makeLine(cq.Vector(*p4), cq.Vector(*p1)),
            ]
        )
        face = cq.Face.makeFromWires(wire)
        frame = frame.add(face)

# Export the final structure
output_filename = "saddle"

extensions = [".stl", ".step", ".svg"]

# Export the final structure in different formats
for ext in extensions:
    output_filepath = os.path.join("results", output_filename + ext)
    cq.exporters.export(frame, output_filepath)
