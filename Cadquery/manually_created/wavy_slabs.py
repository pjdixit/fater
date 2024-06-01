import cadquery as cq
import math
import os


def sine_wave_points(u, phase, amplitude, length):
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
    y = amplitude * math.sin(2 * math.pi * (1 / 2) * u + phase)
    return (x, y)


# Parameters
N_RIBBONS = 50
AMPLITUDE = 20
LENGTH = 250
THICKNESS = 2  # Thickness of the extrusion
NUM_POINTS = 100  # Number of points to define the sine wave

phases = [i * math.pi / 4 for i in range(N_RIBBONS)]
offset_step = THICKNESS  # Adjust this value for desired spacing

# Create a Workplane object
wp = cq.Workplane("XY")
assy = cq.Assembly()

# Generate the wavy ribbons with different phase shifts and offsets
for i, phase in enumerate(phases):
    # Generate points for the sine wave
    points = [
        sine_wave_points(u, phase, AMPLITUDE, LENGTH)
        for u in [j / NUM_POINTS for j in range(NUM_POINTS + 1)]
    ]

    # Create a closed profile by adding lines to close the shape
    points.append((LENGTH, -AMPLITUDE - 1))
    points.append((0, -AMPLITUDE - 1))
    points.append(points[0])  # Close the profile by returning to the first point

    # Create a 2D wire from the points
    wire = wp.polyline(points).close()

    # Extrude the closed profile
    ribbon = wire.extrude(THICKNESS)

    # Add to assembly with an offset
    assy.add(
        ribbon.translate((0, 0, i * offset_step)),
        name=f"ribbon {i}",
        color=cq.Color("green"),
    )

output_filename = "wavy_slabs"

extensions = [".stl", ".step"]

# Export the final structure in different formats
for ext in extensions:
    output_filepath = os.path.join("results", output_filename + ext)
    assy.save(output_filepath)
