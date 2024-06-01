import cadquery as cq

# Define your sections
lofted_shape = (
    cq.Workplane("XY")
    .circle(10)
    .workplane(offset=10)
    .rect(20, 10)
    .workplane(offset=20)
    .circle(5)
    .loft()
)


cq.exporters.export(lofted_shape, "results/loft.step")
