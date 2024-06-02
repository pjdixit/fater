(length, height, diam, thickness, padding, chamfer_size, fillet_radius, slot_length, slot_width, hole_diam) = (
    30.0, 40.0, 22.0, 10.0, 8.0, 2.0, 1.5, 15.0, 5.0, 3.0)

result = (
    Workplane("XY")
    .box(length, height, thickness)
    .edges("|Z").chamfer(chamfer_size)  # Adding chamfers to vertical edges
    .edges(">Z").fillet(fillet_radius)  # Adding fillets to top horizontal edges
    .faces(">Z")
    .workplane()
    .hole(diam)
    .faces(">Z")
    .workplane()
    .rect(length - padding, height - padding, forConstruction=True)
    .vertices()
    .cboreHole(2.4, 4.4, 2.1)
    .faces(">Z")
    .workplane()
    .slot2D(slot_length, slot_width)
    .cutThruAll()
    .faces(">Z")
    .workplane()
    .rarray(hole_diam * 2, hole_diam * 2, 3, 3)
    .circle(hole_diam / 2)
    .cutThruAll()
    .faces(">Z")
    .workplane()
    .rect(length - padding * 2, height - padding * 2, forConstruction=True)
    .vertices()
    .hole(hole_diam)
)

show_object(result)
