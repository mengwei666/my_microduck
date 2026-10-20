import FreeCAD as App
import Part

for name, path in [
    ("body_only", "/home/mw/mw_ai/microduck_scs225/scs225_cad/SCS225_body_only.step"),
    ("simplified", "/home/mw/mw_ai/microduck_scs225/scs225_cad/SCS225_simplified.step"),
    ("ST3215_reference", "/home/mw/mw_ai/microduck_scs225/scs225_cad/SCS225_reference_ST3215.step"),
]:
    shape = Part.read(path)
    print("====", name)
    b = shape.BoundBox
    print("BBOX", tuple(round(v, 3) for v in (b.XMin, b.YMin, b.ZMin, b.XMax, b.YMax, b.ZMax)))
    print("SIZE", round(b.XLength, 3), round(b.YLength, 3), round(b.ZLength, 3))
    holes = []
    for f in shape.Faces:
        try:
            s = f.Surface
            if s.TypeId == "Part::GeomCylinder" and abs(s.Radius - 1.75) < 0.01:
                c = s.Center
                a = s.Axis
                holes.append((round(c.x, 3), round(c.y, 3), round(c.z, 3),
                              round(abs(a.x), 3), round(abs(a.y), 3), round(abs(a.z), 3)))
        except Exception:
            pass
    print("r=1.75 holes:", sorted(set(holes)))
