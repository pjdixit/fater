from cadquery import *

# Base parameters
w = 10
d = 10
h = 10

# Define parts with additional features
part1 = (
    Workplane()
    .box(2 * w, 2 * d, h)
    .fillet(2)  # Adding fillets to edges
)

part2 = (
    Workplane()
    .box(w, d, 2 * h)
    .edges(">Z").chamfer(1)  # Adding chamfers to edges
    .faces(">Z")
    .workplane()
    .hole(d / 2)  # Adding a central hole
)

part3 = (
    Workplane()
    .box(w, d, 3 * h)
    .faces("<Y")
    .workplane()
    .rarray(2 * w, 2 * h, 2, 3)  # Creating an array of holes
    .hole(d / 3)
)

# Define additional complex parts
part4 = (
    Workplane()
    .sphere(h)  # Adding a sphere
    .translate((2 * w, 2 * d, 3 * h))  # Placing it at a different location
)

part5 = (
    Workplane()
    .cylinder(1.5 * h, d / 2)  # Adding a cylinder
    .translate((-1.5 * w, 1.5 * d, 0))  # Placing it at a different location
)

# Create assembly with defined parts and additional parts
assy = (
    Assembly(part1, loc=Location(Vector(-w, 0, h / 2)))
    .add(part2, loc=Location(Vector(1.5 * w, -0.5 * d, h / 2)), color=Color(0, 0, 1, 0.5))
    .add(part3, loc=Location(Vector(-0.5 * w, -0.5 * d, 2 * h)), color=Color("red"))
    .add(part4, loc=Location(Vector(2 * w, 2 * d, 3 * h)), color=Color("green"))
    .add(part5, loc=Location(Vector(-1.5 * w, 1.5 * d, 0)), color=Color("yellow"))
)

# Export the assembly
show_object(assy)
