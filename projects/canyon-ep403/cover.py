"""Canyon EP403-16 cable cover: the plate under the bottom bracket that covers
the frame's cable port, with a slit to slide it over a hose already in place.

The outline (plan view) and the bend (flat, then one radius) follow a friend's
Solid Edge sketches of his original; params.py marks which numbers are his,
which are read off the photos, and which are placeholders (thickness, screw
holes). "Simoncello" is engraved into the flat outer face.

The 3D part is the bent strip (side view) cut by the outline (plan view),
which reads his overall length of 37 as the length straight across, as his
side view draws it.

Model: `ep403_cover`. How it is built and shown: src/cadkit/present.py.
"""

import math

from build123d import (
    Align,
    Circle,
    Cylinder,
    Face,
    Line,
    Location,
    Part,
    Plane,
    Polyline,
    Pos,
    Rot,
    Text,
    ThreePointArc,
    Vector,
    Wire,
    extrude,
)
from cad import model

from cadkit import present_model
from params import (
    BEND_RADIUS,
    BOTTOM_CORNER_RADIUS,
    BOTTOM_FLAT,
    FLAT_LENGTH,
    HOLE_DIAMETER,
    HOLE_FROM_END,
    HOLE_OFFSET,
    KEYHOLE_FROM_END,
    KEYHOLE_RADIUS,
    KEYHOLE_X,
    LEFT_ARC_RADIUS,
    LETTERING,
    LETTERING_DEPTH,
    LETTERING_SIZE,
    LEFT_STRAIGHT,
    LEFT_X,
    LENGTH,
    SLIT_MOUTH_LEFT_X,
    SLIT_MOUTH_RADIUS,
    SLIT_WIDTH_MOUTH,
    SLIT_WIDTH_TOP,
    THICKNESS,
    TOP_CORNER_RADIUS,
    TOP_EDGE,
)

# Printed on its right side: that side is one straight line in plan, so the
# bent part has a single flat face there (the left side's arc bulges past its
# straight edge, so the left side has none). Lying on it, the bend is printed
# in the layer plane, true to shape and without supports, and the layers run
# along the slit's two fingers, which flex when the cover is slid over the hose.


def print_orientation() -> Location:
    """Turn the right side parallel to y, then lay the part on it."""
    top_right_x = LEFT_X + 2 * TOP_CORNER_RADIUS + TOP_EDGE
    bottom_right_x = _bottom_right()[0]
    slant = math.degrees(math.atan2(top_right_x - bottom_right_x, LENGTH))
    return Location((0, 0, 0), (0, 90, 0)) * Location((0, 0, 0), (0, 0, slant))


def _arc_midpoint(a, b, radius, outward):
    """Middle of the arc of `radius` from a to b that bulges towards `outward`
    (a point on the side the arc should bulge to)."""
    (ax, ay), (bx, by) = a, b
    chord = math.hypot(bx - ax, by - ay)
    nx, ny = -(by - ay) / chord, (bx - ax) / chord
    mx, my = (ax + bx) / 2, (ay + by) / 2
    if (outward[0] - mx) * nx + (outward[1] - my) * ny < 0:
        nx, ny = -nx, -ny
    sagitta = radius - math.sqrt(radius**2 - (chord / 2) ** 2)
    return (mx + sagitta * nx, my + sagitta * ny)


def _bottom_right() -> tuple[float, float]:
    """The bottom-right corner (before rounding): the slit's mouth, its corner
    radius, the measured flat end, then the corner radius."""
    mouth_right_x = SLIT_MOUTH_LEFT_X + SLIT_WIDTH_MOUTH
    return (mouth_right_x + SLIT_MOUTH_RADIUS + BOTTOM_FLAT + BOTTOM_CORNER_RADIUS, -LENGTH)


def _keyhole_centre() -> tuple[float, float]:
    return (KEYHOLE_X, -LENGTH + KEYHOLE_FROM_END + KEYHOLE_RADIUS)


def _slit_centre_x(y: float) -> float:
    """The slit's centre line, from the keyhole to the middle of its mouth."""
    kx, ky = _keyhole_centre()
    mouth_x = SLIT_MOUTH_LEFT_X + SLIT_WIDTH_MOUTH / 2
    return kx + (mouth_x - kx) * (ky - y) / (ky + LENGTH)


def outline() -> Face:
    """The part seen from above, in the XY plane."""
    mouth_right_x = SLIT_MOUTH_LEFT_X + SLIT_WIDTH_MOUTH
    top_left = (LEFT_X, 0.0)
    top_right = (LEFT_X + 2 * TOP_CORNER_RADIUS + TOP_EDGE, 0.0)
    bottom_right = _bottom_right()
    left_low = (LEFT_X, -TOP_CORNER_RADIUS - LEFT_STRAIGHT)
    mouth_left = (SLIT_MOUTH_LEFT_X, -LENGTH)
    arc_mid = _arc_midpoint(left_low, mouth_left, LEFT_ARC_RADIUS, outward=(LEFT_X - 10, -LENGTH - 10))

    outer = Face(
        Wire(
            [
                *Polyline(left_low, top_left, top_right, bottom_right, mouth_left).edges(),
                ThreePointArc(mouth_left, arc_mid, left_low),
            ]
        )
    )
    outer = outer.fillet_2d(TOP_CORNER_RADIUS, [v for v in outer.vertices() if abs(v.Y) < 1e-6])
    outer = outer.fillet_2d(
        BOTTOM_CORNER_RADIUS,
        [v for v in outer.vertices() if abs(v.X - bottom_right[0]) < 1e-6 and abs(v.Y + LENGTH) < 1e-6],
    )

    # The slit, tapering from the keyhole to its mouth, run past the end so it
    # opens cleanly; then the keyhole.
    kx, ky = _keyhole_centre()
    below = -LENGTH - 1.0
    def along(x_top, x_mouth):  # the slit's side, extended past the end
        return x_top + (x_mouth - x_top) * (ky - below) / (ky + LENGTH)
    slit = Face(
        Wire.make_polygon(
            [
                Vector(kx - SLIT_WIDTH_TOP / 2, ky),
                Vector(kx + SLIT_WIDTH_TOP / 2, ky),
                Vector(along(kx + SLIT_WIDTH_TOP / 2, mouth_right_x), below),
                Vector(along(kx - SLIT_WIDTH_TOP / 2, SLIT_MOUTH_LEFT_X), below),
            ],
            close=True,
        )
    )
    keyhole = Pos(kx, ky) * Circle(KEYHOLE_RADIUS)
    face = (outer - slit - keyhole).faces()[0]

    mouth = [v for v in face.vertices() if abs(v.Y + LENGTH) < 1e-6 and SLIT_MOUTH_LEFT_X - 0.5 < v.X < mouth_right_x + 0.5]
    return face.fillet_2d(SLIT_MOUTH_RADIUS, mouth)


def bent_strip(width: float = 60.0) -> Part:
    """The side view: flat for FLAT_LENGTH from the top edge, then BEND_RADIUS
    bending down (-z), THICKNESS on the outside of the bend; extruded across x."""
    reach = LENGTH + 1.0  # a little past the end, so the outline does the cutting
    angle = math.asin((reach - FLAT_LENGTH) / BEND_RADIUS)

    def on_arc(r, a):  # (y, z) on a circle about the bend's centre
        return (-FLAT_LENGTH - r * math.sin(a), -BEND_RADIUS + r * math.cos(a))

    r_in, r_out = BEND_RADIUS, BEND_RADIUS + THICKNESS
    profile = Face(
        Wire(
            [
                Line((1.0, 0.0), (-FLAT_LENGTH, 0.0)),
                ThreePointArc((-FLAT_LENGTH, 0.0), on_arc(r_in, angle / 2), on_arc(r_in, angle)),
                Line(on_arc(r_in, angle), on_arc(r_out, angle)),
                ThreePointArc(on_arc(r_out, angle), on_arc(r_out, angle / 2), (-FLAT_LENGTH, THICKNESS)),
                Line((-FLAT_LENGTH, THICKNESS), (1.0, THICKNESS)),
                Line((1.0, THICKNESS), (1.0, 0.0)),
            ]
        )
    )
    # The profile is drawn with (y, z) as its (x, y); Plane.YZ maps them so.
    return extrude(Plane.YZ.location * profile, amount=width / 2, both=True)


def screw_holes() -> Part:
    """Two holes beside the slit near its mouth, square to the surface there."""
    y = -LENGTH + HOLE_FROM_END
    angle = math.asin(max(0.0, -y - FLAT_LENGTH) / BEND_RADIUS)
    z = -BEND_RADIUS + BEND_RADIUS * math.cos(angle) + THICKNESS / 2
    holes = Part()
    for x in (_slit_centre_x(y) - HOLE_OFFSET, _slit_centre_x(y) + HOLE_OFFSET):
        # Rot about x tilts the cylinder's axis from +z to the surface normal.
        holes += Pos(x, y, z) * Rot(math.degrees(angle), 0, 0) * Cylinder(HOLE_DIAMETER / 2, 4 * THICKNESS)
    return holes


def lettering() -> Part:
    """LETTERING, cut LETTERING_DEPTH into the flat outer face (z = THICKNESS):
    centred across the face, and between the top edge and the keyhole."""
    left, right = LEFT_X, LEFT_X + 2 * TOP_CORNER_RADIUS + TOP_EDGE
    keyhole_top = _keyhole_centre()[1] + KEYHOLE_RADIUS
    text = Text(LETTERING, font_size=LETTERING_SIZE, align=(Align.CENTER, Align.CENTER))
    # From just above the face down to the engraving's floor.
    return Pos((left + right) / 2, keyhole_top / 2, THICKNESS - LETTERING_DEPTH) * extrude(
        text, amount=LETTERING_DEPTH + 1
    )


def build() -> Part:
    # Both ways, so the prism covers the whole bend whichever way the
    # outline's face happens to point.
    plan = extrude(outline(), amount=30, both=True)
    return (bent_strip() & plan) - screw_holes() - lettering()


@model
def ep403_cover():
    """The printed part, in its use position."""
    part = build()
    part.label = "ep403_cover"
    return part


if __name__ == "__main__":
    present_model(
        "ep403_cover",
        project="canyon-ep403",
        part=ep403_cover,
        build=build,
        print_orientation=print_orientation(),
    )
