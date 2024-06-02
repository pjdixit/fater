import cadquery as cq

b1 = cq.Workplane().box(1, 1, 1)
b2 = cq.Workplane().sphere(0.15)

assy = (
    cq.Assembly()
    .add(b1, name="b1")
    .add(b2, loc=cq.Location((0, 0, 4)), name="b2", color=cq.Color("red"))
    .add(b1, loc=cq.Location((-2, 0, 0)), name="b3", color=cq.Color("red"))
)

pnt = (0.5, 0.5, 0.5)

# fix the position of b1
assy.constrain("b1", "Fixed")
# fix b2 center at point
assy.constrain("b2", "FixedPoint", pnt)
# fix b3 vertex position at point
assy.constrain("b3@vertices@<X and <Y and <Z", "FixedPoint", pnt)

assy.solve()
show_object(assy)