"""Non-printed geometry: the rail profile, the set screw and the insert.

The rail's channel cavity is also used by the end stopper, whose slider is
the cavity shrunk by the fit clearance.
"""

import math

from build123d import Color, Edge, Face, Part, Spline, ThreePointArc, Vector, Wire

from cadkit.features import box, extrude_profile, vertical_hole
from params import (
    RAIL_CHANNEL_RADIUS,
    RAIL_CHANNEL_WALL_BOTTOM,
    RAIL_HEIGHT_LEFT,
    RAIL_HEIGHT_RIGHT,
    RAIL_INNER_HALF_WIDTH,
    RAIL_LIP_TOP,
    RAIL_OUTER_CURVE,
    RAIL_SLOT,
    RAIL_WEB_BOTTOM,
    RAIL_WEB_TOP,
    RAIL_WIDTH,
)

# RGB(A) as numbers: a Color at module level would load the kernel on every
# run of a model script, a replay included.
ALUMINIUM = (0.75, 0.77, 0.80, 0.45)
STEEL = (0.25, 0.25, 0.28)
BRASS = (0.78, 0.62, 0.30)


def _line(a: tuple[float, float], b: tuple[float, float]) -> Edge:
    return Edge.make_line(Vector(*a), Vector(*b))


def _mirror(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Left-half points -> right-half points, in order continuing around the outline."""
    return [(-x, z) for x, z in reversed(points)]


def _symmetric_face(top_z: float, left: list[tuple[float, float]]) -> Face:
    """Closed outline: flat top at top_z, both sides down along `left` and its mirror."""
    right = _mirror(left)
    top_left, top_right = (left[0][0], top_z), (right[-1][0], top_z)
    return Face(
        Wire(
            [
                _line(top_left, left[0]),
                Spline(*left),
                _line(left[-1], right[0]),
                Spline(*right),
                _line(right[-1], top_right),
                _line(top_right, top_left),
            ]
        )
    )


def _arc_midpoint(a: tuple[float, float], b: tuple[float, float], radius: float) -> tuple[float, float]:
    """Middle of the arc of `radius` from a to b whose centre lies above the chord
    (the arc sags downward, like the channel's rounded bottom)."""
    (ax, az), (bx, bz) = a, b
    chord = math.hypot(bx - ax, bz - az)
    if radius < chord / 2:
        raise ValueError(f"radius {radius} is smaller than half the chord ({chord / 2:.3f})")
    nx, nz = -(bz - az) / chord, (bx - ax) / chord  # unit normal to the chord
    if nz < 0:
        nx, nz = -nx, -nz  # pointing up, towards the centre
    sagitta = radius - math.sqrt(radius**2 - (chord / 2) ** 2)
    return ((ax + bx) / 2 - sagitta * nx, (az + bz) / 2 - sagitta * nz)


def channel_cavity() -> Face:
    """Cross-section (x, z) of the glider channel, from the web's underside down to the slot.

    Straight side walls down to RAIL_CHANNEL_WALL_BOTTOM, then on each side one
    arc of RAIL_CHANNEL_RADIUS to the slot edge, flat across the slot.
    """
    w, s = RAIL_INNER_HALF_WIDTH, RAIL_SLOT / 2
    top_l, top_r = (-w, RAIL_WEB_BOTTOM), (w, RAIL_WEB_BOTTOM)
    wall_l, wall_r = (-w, RAIL_CHANNEL_WALL_BOTTOM), (w, RAIL_CHANNEL_WALL_BOTTOM)
    lip_l, lip_r = (-s, RAIL_LIP_TOP), (s, RAIL_LIP_TOP)
    return Face(
        Wire(
            [
                _line(top_l, wall_l),
                ThreePointArc(wall_l, _arc_midpoint(wall_l, lip_l, RAIL_CHANNEL_RADIUS), lip_l),
                _line(lip_l, lip_r),
                ThreePointArc(lip_r, _arc_midpoint(lip_r, wall_r, RAIL_CHANNEL_RADIUS), wall_r),
                _line(wall_r, top_r),
                _line(top_r, top_l),
            ]
        )
    )


def rail(length: float) -> Part:
    """Rail running along +y from y=0. Lower channel traced from the drawing, upper part approximate."""
    y = (0, length)
    half = RAIL_WIDTH / 2
    lower_outer = _symmetric_face(RAIL_WEB_TOP, RAIL_OUTER_CURVE)
    lower = (
        extrude_profile(lower_outer, y)
        - extrude_profile(channel_cavity(), y)
        - box((-RAIL_SLOT / 2, RAIL_SLOT / 2), y, (-1, 1))  # the slot through the lips
    )
    upper = (
        box((-half, -RAIL_INNER_HALF_WIDTH), y, (RAIL_WEB_TOP - 0.1, RAIL_HEIGHT_LEFT))
        + box((RAIL_INNER_HALF_WIDTH, half), y, (RAIL_WEB_TOP - 0.1, RAIL_HEIGHT_RIGHT))
        + box((-RAIL_INNER_HALF_WIDTH, -half + 2.2), y, (8.3, 9.3))  # upper left hook
        + box((half - 3.0, RAIL_INNER_HALF_WIDTH), y, (RAIL_HEIGHT_RIGHT - 1, RAIL_HEIGHT_RIGHT))
    )
    r = lower + upper
    r.color = Color(*ALUMINIUM)
    return r


def screw(x: float, y: float, z: tuple[float, float], diameter: float) -> Part:
    s = vertical_hole(x, y, z, diameter)
    s.color = Color(*STEEL)
    return s


def insert(x: float, y: float, top: float, length: float, diameter: float, bore: float) -> Part:
    """Heat-set insert, top face at `top`: a plain tube (no knurl)."""
    i = vertical_hole(x, y, (top - length, top), diameter) - vertical_hole(
        x, y, (top - length - 1, top + 1), bore
    )
    i.color = Color(*BRASS)
    return i
