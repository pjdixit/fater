import cadquery as cq

R = 0.5  # Radius of the helix
r = 0.2  # inner radius of the spring
p = 0.4  # Pitch of the helix - vertical distance between loops
h = 2.4  # Height of the helix - total height

# Helix
wire = cq.Wire.makeHelix(pitch=p, height=h, radius=r)
helix = cq.Workplane(obj=wire)

# Final result: A 2D shape swept along a helix.
result = (
    cq.Workplane("XZ")  # helix is moving up the Z axis
    .center(R, 0)  # offset isosceles trapezoid
    .circle(r)
    .sweep(helix, isFrenet=True)  # Frenet keeps orientation as expected
)

# Show the spring
cq.exporters.export(result, "results/spring.step")
