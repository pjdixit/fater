import cadquery as cq
import numpy as np
import os

# Parameters
grid_size = 10  # Distance between grid points
sphere_radius = 1  # Radius of the spheres
cylinder_radius = 0.5  # Radius of the connecting cylinders
levels = 3  # Number of levels
N_u = 7
N_v = 6

# Create the base grid structure
result = cq.Workplane("XY")


# Function to create a cylinder between two points in 3D space
def create_cylinder(p1, p2):
    p1 = cq.Vector(p1)
    p2 = cq.Vector(p2)
    vec = p2.sub(p1)
    length = vec.Length
    mid_point = p1.add(vec.multiply(0.5))

    # Calculate the rotation axis and angle
    z_axis = cq.Vector(0, 0, 1)
    rotation_axis = z_axis.cross(vec)
    rotation_angle = np.degrees(np.arccos(z_axis.dot(vec) / vec.Length))

    # Create the cylinder in the XY plane and rotate it into position
    cylinder = cq.Workplane("XY").cylinder(length, cylinder_radius)

    if rotation_axis.Length > 0:
        cylinder = cylinder.rotate((0, 0, 0), rotation_axis.toTuple(), rotation_angle)

    # Translate the cylinder to the midpoint
    cylinder = cylinder.translate(mid_point.toTuple())

    return cylinder


# Generate spheres and connect cylinders
for level in range(levels):
    z = level * grid_size
    for u in range(N_u):
        x = u * grid_size
        for v in range(N_v):
            y = v * grid_size

            sphere = cq.Workplane("XY").sphere(sphere_radius).translate((x, y, z))
            result.add(sphere)

            if v != N_v - 1:
                # vertical connection the y direction
                result.add(create_cylinder((x, y, z), (x, y + grid_size, z)))

            if u != N_u - 1:
                # horizontal connection in the x direction
                result.add(create_cylinder((x, y, z), (x + grid_size, y, z)))

            if level != levels - 1:
                # vertical connection the y direction
                result.add(create_cylinder((x, y, z), (x, y, z + grid_size)))

            if u != N_u - 1 and v != N_v - 1:
                # diagonal connection in the XY plane
                result.add(
                    create_cylinder((x, y, z), (x + grid_size, y + grid_size, z))
                )

            if u != N_u - 1 and level != levels - 1:
                # diagonal connection in the XZ plane
                result.add(
                    create_cylinder((x, y, z), (x + grid_size, y, z + grid_size))
                )

            if v != N_v - 1 and level != levels - 1:
                # diagonal connection in the YZ plane
                result.add(
                    create_cylinder((x, y, z), (x, y + grid_size, z + grid_size))
                )

            if u != N_u - 1 and v != N_v - 1 and level != levels - 1:
                # diagonal connection in the 1/2-XYZ plane
                result.add(
                    create_cylinder(
                        (x, y, z), (x + grid_size, y + grid_size, z + grid_size)
                    )
                )

# Export the final structure
output_filename = "space_truss"

extensions = [".stl", ".step", ".svg"]

# Export the final structure in different formats
for ext in extensions:
    output_filepath = os.path.join("results", output_filename + ext)
    cq.exporters.export(result, output_filepath)
