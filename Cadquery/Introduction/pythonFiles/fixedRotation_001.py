import cadquery as cq

b1 = cq.Workplane().box(1, 1, 1)
b2 = cq.Workplane().rect(0.1, 0.1).extrude(1, taper=-15)

assy = (
    cq.Assembly()
    .add(b1, name="b1")
    .add(b2, loc=cq.Location((0, 0, 4)), name="b2", color=cq.Color("red"))
)

# fix the position of b1
assy.constrain("b1", "Fixed")
# fix b2 bottom face position (but not rotation)
assy.constrain("b2@faces@<Z", "FixedPoint", (0, 0, 0.5))
# fix b2 rotational degrees of freedom too
assy.constrain("b2", "FixedRotation", (45, 0, 45))

assy.solve()
show_object(assy)