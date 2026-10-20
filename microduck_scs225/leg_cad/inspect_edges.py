import FreeCAD as App
import Part
import os

base = "/home/mw/mw_ai/microduck_scs225/leg_cad"
files = [
    "left_upper_leg_FT.step",
    "leg_FT.step",
    "yaw2roll_FT.step",
    "bearing_roll_FT.step",
    "ankle_left_FT.step",
    "rigidity_plate_FT.step",
    "microduck_trunk_base.step",
]
for fn in files:
    path = os.path.join(base, fn)
    if not os.path.exists(path):
        print("MISSING", fn); continue
    shape = Part.read(path)
    print("====", fn)
    circles = []
    for e in shape.Edges:
        try:
            c = e.Curve
            if c.TypeId != "Part::GeomCircle": continue
            r = c.Radius
            if not (0.5 <= r <= 2.5): continue
            cen = c.Center
            ax = c.Axis
            circles.append((round(r,2), tuple(round(v,2) for v in (cen.x,cen.y,cen.z)), tuple(round(v,1) for v in (ax.x,ax.y,ax.z))))
        except Exception:
            pass
    circles = sorted(set(circles))
    print("CIRCLES", len(circles))
    for p in circles[:160]:
        print("   ", p)
