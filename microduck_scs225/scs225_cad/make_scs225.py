import FreeCAD as App
import Part
from FreeCAD import Vector

# Simplified SCS225 envelope, built from the official Feetech SCS225 drawing
# (45.23 x 24.73 x 35 mm, 4x mounting holes 20.7 x 20.5, output shaft 10.11 mm
# from one end, 25T/OD5.9 shaft, M3 horn screw).
#
# Coordinate system:
#   origin = output shaft centre, on the top face of the case
#   +Z = output shaft axis
#   +X = away from the shaft end (the long side of the case)
#   +Y = right side when looking down the shaft
#
# This is an *envelope* model for checking mounting holes and clearances.
# It is not a cosmetic replica; use the real ST3215/SCS215 STEP for the case
# shape and compare it with the physical SCS225.

L = 45.23          # case length
W = 24.73          # case width
H = 35.00          # case height
SHAFT_FROM_END = 10.11
MOUNT_DX = 20.7    # mounting hole row spacing, length direction
MOUNT_DY = 20.5    # mounting hole row spacing, width direction
MOUNT_R = 1.75     # mounting hole radius (approx. for M3 clearance)
CASE_SCREW_R = 1.1 # PA2.0 self-tapping case screws
SHAFT_BOSS_R = 3.0 # 6 mm boss
SPLINE_R = 2.95    # 25T spline, OD 5.9 mm
SHAFT_UP = 3.4
SHAFT_DOWN = 4.1

x0 = -SHAFT_FROM_END
x1 = L - SHAFT_FROM_END

body = Part.makeBox(L, W, H, Vector(x0, -W / 2.0, -H))

# Mounting holes: near row is 8.3 mm from the shaft, far row 20.7 mm further.
mount_x = [8.3, 8.3 + MOUNT_DX]
mount_y = [-MOUNT_DY / 2.0, MOUNT_DY / 2.0]

cutters = []
for x in mount_x:
    for y in mount_y:
        cutters.append(
            Part.makeCylinder(
                MOUNT_R, H + 2.0, Vector(x, y, -H - 1.0), Vector(0, 0, 1)
            )
        )

# Case screws at the four corners (approximate, from the SCS215/ST3215 STEP).
for x, y in [(-7.1, -9.35), (-7.1, 9.35), (32.75, -10.0), (32.75, 10.0)]:
    cutters.append(
        Part.makeCylinder(
            CASE_SCREW_R, H + 2.0, Vector(x, y, -H - 1.0), Vector(0, 0, 1)
        )
    )

shape = body
for c in cutters:
    shape = shape.cut(c)

# Output shaft: 6 mm boss, 25T spline approximation, M3 centre hole.
shape = shape.fuse(Part.makeCylinder(SHAFT_BOSS_R, 1.0, Vector(0, 0, 0), Vector(0, 0, 1)))
shape = shape.fuse(Part.makeCylinder(SPLINE_R, SHAFT_UP, Vector(0, 0, 0), Vector(0, 0, 1)))
shape = shape.cut(Part.makeCylinder(1.5, 6.0, Vector(0, 0, 0), Vector(0, 0, 1)))

# Opposite (bottom) shaft.
shape = shape.fuse(
    Part.makeCylinder(SHAFT_BOSS_R, SHAFT_DOWN, Vector(0, 0, -H - SHAFT_DOWN), Vector(0, 0, 1))
)

body_only = shape
out_body = "/home/mw/mw_ai/microduck_scs225/scs225_cad/SCS225_body_only.step"
body_only.exportStep(out_body)
print("WROTE", out_body)
print("BODY BBOX", body_only.BoundBox)

# Connector envelope: 5264-3P, on the far side of the case.
shape = shape.fuse(Part.makeBox(8.0, 6.0, 9.0, Vector(24.0, W / 2.0, -22.0)))

# Small identification mark: a raised bar on the top face, away from the shaft.
shape = shape.fuse(Part.makeBox(4.0, 2.0, 0.4, Vector(20.0, -1.0, 0.0)))

out = "/home/mw/mw_ai/microduck_scs225/scs225_cad/SCS225_simplified.step"
shape.exportStep(out)
print("WROTE", out)
print("FULL BBOX", shape.BoundBox)
print("SOLIDS", len(shape.Solids), "FACES", len(shape.Faces))
