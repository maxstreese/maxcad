"""Non-printed geometry: the opening side of both doors, and the fridge door's
curved front, which the rail's clip follows."""

import math

from build123d import Color, Face, Line, Part, Plane, Pos, ThreePointArc, Wire, extrude, mirror

from cadkit.features import box
from params import DOOR_GAP, DOOR_RADIUS, DOOR_THICKNESS, FRONT_THICKNESS, GAP_INWARD, OPENING_SIDE

# RGBA as numbers: a Color at module level would load the kernel on every run
# of a model script, a replay included.
FRIDGE = (0.92, 0.92, 0.90, 0.6)
WOOD = (0.80, 0.66, 0.47, 0.5)


def handed(shape):
    """`shape` as drawn (a door opening on the right), mirrored across x = 0 for
    a door opening on the left."""
    if OPENING_SIDE == "right":
        return shape
    if OPENING_SIDE == "left":
        return mirror(shape, Plane.YZ)
    raise ValueError(f"OPENING_SIDE={OPENING_SIDE!r}: expected 'left' or 'right'")


def _rise(x: float, crown: float) -> float:
    """How far the front at x stands forward of the front at the edge (x = 0),
    for a circle of DOOR_RADIUS with its crown at `crown`."""
    r = DOOR_RADIUS
    return math.sqrt(r * r - (x - crown) ** 2) - math.sqrt(r * r - crown * crown)


def crown_x() -> float:
    """Where the front's crown lies, in from the edge: the circle of DOOR_RADIUS
    through the gaps measured at the edge and at GAP_INWARD. Plain arithmetic
    (bisection), no kernel."""
    x1, gap1 = GAP_INWARD
    rise = DOOR_GAP - gap1
    lo, hi = x1 / 2, DOOR_RADIUS  # _rise(x1) grows with the crown position
    assert _rise(x1, hi) > rise, "DOOR_RADIUS too large for the measured gaps"
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if _rise(x1, mid) < rise else (lo, mid)
    return (lo + hi) / 2


def front_y(x: float) -> float:
    """y of the fridge door's front face at x: 0 at the side edge, standing
    forward towards the crown."""
    return _rise(x, crown_x())


def door_plan(x: tuple[float, float], y_back: float) -> Face:
    """The door seen from above (on z = 0), from x[0] to x[1]: the curved front
    and a straight line at y_back behind it."""
    x0, x1 = x
    xm = (x0 + x1) / 2
    front = ThreePointArc((x1, front_y(x1)), (xm, front_y(xm)), (x0, front_y(x0)))
    return Face(
        Wire(
            [
                Line((x0, y_back), (x1, y_back)),
                Line((x1, y_back), (x1, front_y(x1))),
                front,
                Line((x0, front_y(x0)), (x0, y_back)),
            ]
        )
    )


def door_prism(x: tuple[float, float], y_back: float, z: tuple[float, float]) -> Part:
    """door_plan run from z[0] up to z[1]."""
    return Pos(0, 0, z[0]) * extrude(door_plan(x, y_back), z[1] - z[0], dir=(0, 0, 1))


def back_y() -> float:
    """y of the fridge door's (flat) back face: DOOR_THICKNESS behind the front
    at the side edge."""
    return front_y(0) - DOOR_THICKNESS


def fridge_door(width: float, z: tuple[float, float]) -> Part:
    """The fridge door's opening side: side edge at x = 0, curved front through
    y = 0 at the rail's middle, flat back."""
    d = handed(door_prism((0, width), back_y(), z))
    d.color = Color(*FRIDGE)
    return d


def furniture_door(x: tuple[float, float], z: tuple[float, float]) -> Part:
    """The furniture front, its back face DOOR_GAP in front of the fridge door."""
    d = handed(box(x, (DOOR_GAP, DOOR_GAP + FRONT_THICKNESS), z))
    d.color = Color(*WOOD)
    return d
