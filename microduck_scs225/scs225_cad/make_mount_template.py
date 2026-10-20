import FreeCAD as App
import Part
from FreeCAD import Vector

# SCS225 mounting-hole drill/alignment template.
# Origin = output shaft centre. +X away from the shaft end. Plate lies in XY.
L = 45.23
W = 24.73
T = 2.0
x0 = -10.11
x1 = L - 10.11

plate = Part.makeBox(L, W, T, Vector(x0, -W / 2.0, 0.0))

holes = []
for x in (8.3, 29.0):
    for y in (-10.25, 10.25):
        holes.append(Part.makeCylinder(1.75, T + 2.0, Vector(x, y, -1.0), Vector(0, 0, 1)))

# Centre opening for the output boss / alignment.
holes.append(Part.makeCylinder(5.0, T + 2.0, Vector(0, 0, -1.0), Vector(0, 0, 1)))

# Shaft-side marker: 3 mm hole on the -X side.
holes.append(Part.makeCylinder(1.5, T + 2.0, Vector(-7.0, 0, -1.0), Vector(0, 0, 1)))

for h in holes:
    plate = plate.cut(h)

out = "/home/mw/mw_ai/microduck_scs225/scs225_cad/SCS225_mount_template.step"
plate.exportStep(out)
print("WROTE", out, "BBOX", plate.BoundBox)
