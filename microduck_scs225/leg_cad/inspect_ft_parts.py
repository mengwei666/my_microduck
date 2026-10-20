import FreeCAD as App
import Part
import os, itertools, math

base = "/home/mw/mw_ai/microduck_scs225/leg_cad/ft_changed_parts"
files = [
    "left_upper_leg_左上腿-FT.STEP",
    "leg_腿部-FT.STEP",
    "yaw2roll_偏航转横滚-FT.STEP",
    "bearing_roll_轴承滚轮-FT.STEP",
    "ankle_left_脚踝左-FT.STEP",
    "01-upper_leg_rigidity_plate_上腿加固板-FT.STEP",
]
for fn in files:
    path = os.path.join(base, fn)
    if not os.path.exists(path):
        print("MISSING", fn); continue
    shape = Part.read(path)
    b = shape.BoundBox
    print("====", fn)
    print("BBOX", tuple(round(v,2) for v in (b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax)))
    print("SIZE", round(b.XLength,2), round(b.YLength,2), round(b.ZLength,2), "SOLIDS", len(shape.Solids), "FACES", len(shape.Faces))
    # collect small cylindrical faces, axis aligned to principal axis
    pts = []
    for f in shape.Faces:
        try:
            s = f.Surface
            if s.TypeId != "Part::GeomCylinder": continue
            r = s.Radius
            if not (0.6 <= r <= 2.2): continue
            a = s.Axis
            ax = [abs(a.x), abs(a.y), abs(a.z)]
            # require one axis component > 0.999
            if max(ax) < 0.999: continue
            c = s.Center
            pts.append((round(r,2), tuple(round(v,2) for v in (c.x,c.y,c.z)), tuple(round(v,1) for v in (a.x,a.y,a.z))))
        except Exception:
            pass
    # unique
    pts = sorted(set(pts))
    print("SMALL CYLINDERS", len(pts))
    for p in pts[:80]:
        print("   ", p)
