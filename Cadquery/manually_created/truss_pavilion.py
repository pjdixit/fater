import cadquery as cq
import numpy as np
from scipy.interpolate import make_interp_spline
import os

# Parameters for arcs
arc_lengths = [5000, 3000, 5000]
arc_heights = [6000, 3000, 6000]
arc_y_positions = [-2000, 0, 2000]
arc_resolution = 20
cylinder_radius = 10  # Radius of the connecting cylinders
sphere_radius = 10  # Radius of the spheres
offset = (0, 0, 1000)
levels = 2


# Create points for arcs with rotations
def create_vertical_arc_points(length, height, y_position, num_points, rotation_angle):
    angles = np.linspace(0, np.pi, num_points)
    points = [(length * np.cos(angle), 0, height * np.sin(angle)) for angle in angles]
    rotation_matrix = np.array(
        [
            [1, 0, 0],
            [
                0,
                np.cos(np.radians(rotation_angle)),
                -np.sin(np.radians(rotation_angle)),
            ],
            [0, np.sin(np.radians(rotation_angle)), np.cos(np.radians(rotation_angle))],
        ]
    )
    rotated_points = [
        (np.dot(rotation_matrix, np.array([x, y, z]))).tolist() for x, y, z in points
    ]

    # Translate the points to the correct y-position
    translated_points = [(x, y + y_position, z) for x, y, z in rotated_points]

    return translated_points


# Define the arcs with respective rotations
arc_1 = create_vertical_arc_points(
    arc_lengths[0], arc_heights[0], arc_y_positions[0], arc_resolution, 30
)
arc_2 = create_vertical_arc_points(
    arc_lengths[1], arc_heights[1], arc_y_positions[1], arc_resolution, 0
)
arc_3 = create_vertical_arc_points(
    arc_lengths[2], arc_heights[2], arc_y_positions[2], arc_resolution, -30
)


# Create a meshgrid of points with B-spline interpolation
def interpolate_surface_b_spline(arc_1, arc_2, arc_3, resolution, offset=(0, 0, 0)):
    surface_points = []
    for i in range(len(arc_1)):
        x = np.array([arc_1[i][0], arc_2[i][0], arc_3[i][0]])
        y = np.array([arc_1[i][1], arc_2[i][1], arc_3[i][1]])
        z = np.array([arc_1[i][2], arc_2[i][2], arc_3[i][2]])

        t = np.linspace(0, 1, 3)
        spline_x = make_interp_spline(t, x, k=2)
        spline_y = make_interp_spline(t, y, k=2)
        spline_z = make_interp_spline(t, z, k=2)

        t_new = np.linspace(0, 1, resolution)
        x_new = spline_x(t_new) + offset[0]
        y_new = spline_y(t_new) + offset[1]
        z_new = spline_z(t_new) + offset[2]

        row = [(x_new[j], y_new[j], z_new[j]) for j in range(resolution)]
        surface_points.append(row)
    return surface_points


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


surface_points = interpolate_surface_b_spline(arc_1, arc_2, arc_3, arc_resolution)
surface_points_up = interpolate_surface_b_spline(
    arc_1, arc_2, arc_3, arc_resolution, offset
)

# Create the structure in CadQuery
frame = cq.Assembly()

for i in range(len(surface_points) - 1):
    for j in range(len(surface_points[i]) - 1):
        p1 = surface_points[i][j]
        p2 = surface_points[i + 1][j]
        p3 = surface_points[i + 1][j + 1]
        p4 = surface_points[i][j + 1]

        p1Up = surface_points_up[i][j]
        p2Up = surface_points_up[i + 1][j]
        p3Up = surface_points_up[i + 1][j + 1]
        p4Up = surface_points_up[i][j + 1]

        outer_edge = [
            cq.Edge.makeLine(cq.Vector(*p1Up), cq.Vector(*p2Up)),
            cq.Edge.makeLine(cq.Vector(*p2Up), cq.Vector(*p3Up)),
            cq.Edge.makeLine(cq.Vector(*p3Up), cq.Vector(*p4Up)),
            cq.Edge.makeLine(cq.Vector(*p4Up), cq.Vector(*p1Up)),
        ]
        outer_wire = cq.Wire.assembleEdges(outer_edge)
        quad_face = cq.Face.makeNSidedSurface(outer_wire, [])

        frame = frame.add(quad_face)

        # Now we add the space truss to connect both levels

        if j != len(surface_points[i]) - 2:
            # vertical connection in the y direction
            frame.add(create_cylinder(p1, p4))

        # diagonal connection in the YZ plane
        frame.add(create_cylinder(p1, p4Up))

        if i != len(surface_points) - 2:
            # horizontal connection in the x direction
            frame.add(create_cylinder(p1, p2))

            if j != len(surface_points[i]) - 2:
                # diagonal connection in the XY plane
                frame.add(create_cylinder(p1, p3))

            # diagonal connection in the XZ plane
            frame.add(create_cylinder(p1, p2Up))

        if j != len(surface_points[i]) - 2 and i != len(surface_points) - 2:
            # diagonal connection in the 1/2-XYZ plane
            frame.add(create_cylinder(p1, p3Up))

        # vertical connection in the z direction
        frame.add(create_cylinder(p1, p1Up))


# Export the final structure
output_filename = "truss_supported_pavilion"

extensions = [".stl", ".step"]

# Export the final structure in different formats
for ext in extensions:
    output_filepath = os.path.join("results", output_filename + ext)
    frame.save(output_filepath)
