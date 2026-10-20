import FreeCAD as App
import Part
import os

files = [
    ("yaw2roll", "/home/mw/mw_ai/microduck_scs225/leg_cad/microduck_yaw2roll.step"),
    ("trunk_base", "/home/mw/mw_ai/microduck_scs225/leg_cad/microduck_trunk_base.step"),
    ("left_upper_leg", "/home/mw/mw_ai/microduck_scs225/leg_cad/microduck_left_upper_leg.step"),
    ("lower_leg", "/home/mw/mw_ai/microduck_scs225/leg_cad/microduck_lower_leg.step"),
    ("HD1910", "/home/mw/mw_ai/microduck_scs225/leg_cad/HD1910.step"),
]

for name, path in files:
    if not os.path.exists(path):
        print("MISSING", name); continue
    shape = Part.read(path)
    b = shape.BoundBox
    print("====", name)
    print("BBOX", tuple(round(v,2) for v in (b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax)))
    # only cylindrical faces with radius 0.5..3.0, axes aligned to a principal axis
    groups = {}
    for f in shape.Faces:
        try:
            s = f.Surface
            if s.TypeId != "Part::GeomCylinder": continue
            r = round(s.Radius,2)
            if not (0.5 <= r <= 3.0): continue
            a = s.Axis
            ax = (round(a.x,1), round(a.y,1), round(a.z,1))
            c = s.Center
            key = (r, ax)
            groups.setdefault(key, []).append((round(c.x,2), round(c.y,2), round(c.z,2)))
        except Exception:
            pass
    for (r, ax), pts in sorted(groups.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        uniq = sorted(set(pts))
        print("  r=%.2f axis=%s n=%d" % (r, ax, len(uniq)))
        for p in uniq[:12]:
            print("     ", p)
