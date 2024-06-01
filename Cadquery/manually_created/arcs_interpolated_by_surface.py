import cadquery as cq
import numpy as np
from scipy.interpolate import make_interp_spline
import os

# Parameters for arcs
arc_lengths = [5000, 3000, 5000]
arc_heights = [6000, 3000, 6000]
arc_y_positions = [-2000, 0, 2000]
arc_resolution = 20


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
def interpolate_surface_b_spline(arc_1, arc_2, arc_3, resolution):
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
        x_new = spline_x(t_new)
        y_new = spline_y(t_new)
        z_new = spline_z(t_new)

        row = [(x_new[j], y_new[j], z_new[j]) for j in range(resolution)]
        surface_points.append(row)
    return surface_points


surface_points = interpolate_surface_b_spline(arc_1, arc_2, arc_3, arc_resolution)

# Create the structure in CadQuery
frame = cq.Workplane("XY")

for i in range(len(surface_points) - 1):
    for j in range(len(surface_points[i]) - 1):
        p1 = surface_points[i][j]
        p2 = surface_points[i + 1][j]
        p3 = surface_points[i + 1][j + 1]
        p4 = surface_points[i][j + 1]

        outer_edge = [
            cq.Edge.makeLine(cq.Vector(*p1), cq.Vector(*p2)),
            cq.Edge.makeLine(cq.Vector(*p2), cq.Vector(*p3)),
            cq.Edge.makeLine(cq.Vector(*p3), cq.Vector(*p4)),
            cq.Edge.makeLine(cq.Vector(*p4), cq.Vector(*p1)),
        ]
        outer_wire = cq.Wire.assembleEdges(outer_edge)
        quad_face = cq.Face.makeNSidedSurface(outer_wire, [])
        frame = frame.add(quad_face)


output_filename = "arcs_interpolated_surface"

extensions = [".stl", ".step", ".svg"]

# Export the final structure in different formats
for ext in extensions:
    output_filepath = os.path.join("results", output_filename + ext)
    cq.exporters.export(frame, output_filepath)
