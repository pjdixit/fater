import cadquery as cq
import math
import os


def sine_wave_points(u, F=2, phase=0, amplitude=80, length=250):
    """
    Define points for a sine wave with a phase shift that creates a wavy ribbon.

    Args:
    u (float): Parameter along the length of the ribbon.
    phase (float): Phase shift for the sine wave.
    amplitude (float): Amplitude of the sine wave.
    length (float): Total length of the ribbon.

    Returns:
    Tuple[float, float]: The (x, y) coordinates.
    """
    x = u * length
    y = amplitude * math.sin(2 * math.pi * F * u + phase)
    return (x, y)


# Parameters
AMPLITUDE = 20
LENGTH = 250
THICKNESS = 20  # Thickness of the extrusion
NUM_POINTS = 50  # Number of points to define the sine wave
HEIGHT = 100
offset_step = THICKNESS  # Adjust this value for desired spacing

# Create a Workplane object
wp = cq.Workplane("YZ")
assy = cq.Assembly()

peak_points = [
    sine_wave_points(u) for u in [j / (NUM_POINTS - 1) for j in range(NUM_POINTS)]
]


for i, point in enumerate(peak_points):
    peak_point = (point[1], HEIGHT)
    top_point = (-200, 0)
    bottom_point = (200, 0)
    triangle_points = [top_point, peak_point, bottom_point, top_point]
    triangle_profile = wp.polyline(triangle_points).close()
    tetrahedron = triangle_profile.extrude(THICKNESS).edges(">Z").fillet(50)

    assy.add(tetrahedron.translate((i * offset_step, 0, 0)), name=f"tetrhadron {i}")

# Export the final structure
output_filename = "sine_mountain"

extensions = [".stl", ".step"]

# Export the final structure in different formats
for ext in extensions:
    output_filepath = os.path.join("results", output_filename + ext)
    assy.save(output_filepath)
