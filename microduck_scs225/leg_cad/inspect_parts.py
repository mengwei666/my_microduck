import FreeCAD as App
import Part
import os

files = [
    ("HD1910", "/home/mw/mw_ai/microduck_scs225/leg_cad/HD1910.step"),
    ("left_upper_leg", "/home/mw/mw_ai/microduck_scs225/leg_cad/microduck_left_upper_leg.step"),
    ("lower_leg", "/home/mw/mw_ai/microduck_scs225/leg_cad/microduck_lower_leg.step"),
    ("yaw2roll", "/home/mw/mw_ai/microduck_scs225/leg_cad/microduck_yaw2roll.step"),
    ("trunk_base", "/home/mw/mw_ai/microduck_scs225/leg_cad/microduck_trunk_base.step"),
]

for name, path in files:
    if not os.path.exists(path):
        print("MISSING", name, path); continue
    shape = Part.read(path)
    b = shape.BoundBox
    print("====", name)
    print("BBOX", tuple(round(v,2) for v in (b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax)))
    print("SIZE", round(b.XLength,2), round(b.YLength,2), round(b.ZLength,2), "SOLIDS", len(shape.Solids), "FACES", len(shape.Faces))
    # group cylindrical faces by radius and axis direction, with centers
    groups = {}
    for f in shape.Faces:
        try:
            s = f.Surface
            if s.TypeId == "Part::GeomCylinder":
                r = round(s.Radius, 2)
                a = s.Axis
                ax = (round(abs(a.x),1), round(abs(a.y),1), round(abs(a.z),1))
                c = s.Center
                key = (r, ax)
                groups.setdefault(key, []).append((round(c.x,2), round(c.y,2), round(c.z,2)))
        except Exception:
            pass
    # print only groups with small radii (likely holes) and count>1, sorted
    for (r, ax), pts in sorted(groups.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        if r <= 4.0:
            uniq = sorted(set(pts))
            print("  CYL r=%.2f axis=%s n=%d" % (r, ax, len(uniq)))
            for p in uniq[:20]:
                print("     ", p)
