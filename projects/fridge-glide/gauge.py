"""Profile gauge for the fridge door's front: a measuring aid, not part of the
coupling.

The slider's clip sits on the first millimetres of the fridge door's curved
front, and calipers cannot measure that shape. This gauge turns it into depth
readings. It is a rigid C around the door's side edge, used with the door
open, on the surfaces the clip sits on: its web against the side face, its
hook behind the back face. Its straight leg stands off the front, and its
outer face is parallel to the hook's face, gauge_reference() in front of it.
A caliper's depth rod through each hole in the leg reads the distance to the
door's front at that station (GAUGE_STATIONS, in from the side edge):

    door thickness at the station = gauge_reference() - reading

The wedge (gauge_wedge.py), pushed up between the door and the seat sloped
into the leg, holds the hook on the back face meanwhile.

It prints as drawn, the C lying flat: its spans are in the bed plane.

Models: `gauge` (the printed part) and `gauge_on_door` (gauge and wedge on the
door's edge). How they are built and shown: src/cadkit/present.py.
"""

from build123d import Align, Cylinder, Part, Polygon, Pos, Rot, extrude
from cad import model

from cadkit import present_model, with_context
from context import back_y, fridge_door, front_y, handed
from gauge_wedge import build as build_wedge
from gauge_wedge import gauge_wedge, seat_y
from params import (
    DOOR_THICKNESS,
    GASKET_FROM_EDGE,
    GAUGE_CORNER_RELIEF,
    GAUGE_HEIGHT,
    GAUGE_HOLE,
    GAUGE_HOLE_HEIGHTS,
    GAUGE_HOOK_THICKNESS,
    GAUGE_LEG,
    GAUGE_LEG_BEYOND,
    GAUGE_STANDOFF,
    GAUGE_STATIONS,
    GAUGE_WEB,
    HOOK_DEPTH,
    HOOK_LEAD_IN,
    WEDGE_SEAT_X,
)
from rail import _yz, along_x


def leg_outer() -> float:
    """y of the leg's outer face, the caliper's reference face."""
    return GAUGE_STANDOFF + GAUGE_LEG


def gauge_reference() -> float:
    """From the hook's face (on the door's back) to the leg's outer face, as
    drawn. Measure it on the print: over the leg's outer face and the hook's
    outer face, less the hook's thickness."""
    return DOOR_THICKNESS + leg_outer()


def leg_end() -> float:
    return GAUGE_STATIONS[-1] + GAUGE_LEG_BEYOND


def frame() -> Part:
    """The C in plan (x, y), run over GAUGE_HEIGHT: hook behind the back face,
    web on the side face, a straight leg in front of the front face."""
    y_in = back_y()  # the hook's face: on the door's back, no pinch
    y_out = y_in - GAUGE_HOOK_THICKNESS
    w = -GAUGE_WEB
    plan = Polygon(
        (w, y_out),
        (HOOK_DEPTH, y_out),
        (HOOK_DEPTH, y_in - HOOK_LEAD_IN),
        (HOOK_DEPTH - HOOK_LEAD_IN, y_in),
        (0, y_in),
        (0, GAUGE_STANDOFF),
        (leg_end(), GAUGE_STANDOFF),
        (leg_end(), leg_outer()),
        (w, leg_outer()),
        align=None,
    )
    return Pos(0, 0, -GAUGE_HEIGHT / 2) * extrude(plan, GAUGE_HEIGHT, dir=(0, 0, 1))


def corner_relief() -> Part:
    """Round cut in the corner between hook and web, so a sharp door edge
    cannot hold the gauge off either face."""
    return Pos(0, back_y(), 0) * Cylinder(GAUGE_CORNER_RELIEF, GAUGE_HEIGHT + 2)


def wedge_seat() -> Part:
    """Cut that slopes the leg's inner face, from the side edge to WEDGE_SEAT_X,
    into the wedge's seat: SEAT_TOP_DEPTH deep at the top, deepest at the
    bottom (and 1 mm past both)."""
    top, bottom = GAUGE_HEIGHT / 2 + 1, -GAUGE_HEIGHT / 2 - 1
    y = GAUGE_STANDOFF - 1
    profile = _yz([(y, top), (seat_y(top), top), (seat_y(bottom), bottom), (y, bottom)])
    return along_x(profile, WEDGE_SEAT_X)


def station_holes() -> list[tuple[float, float]]:
    """(x, z) of the depth rod's holes: the stations, alternating between the
    two heights so neighbouring holes keep a wall between them."""
    return [(x, GAUGE_HOLE_HEIGHTS[i % 2]) for i, x in enumerate(GAUGE_STATIONS)]


def hole(x: float, z: float) -> Part:
    """Through the leg along y."""
    return Pos(x, GAUGE_STANDOFF - 1, z) * Rot(-90, 0, 0) * Cylinder(
        GAUGE_HOLE / 2, GAUGE_LEG + 2, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )


def build() -> Part:
    assert HOOK_DEPTH < GASKET_FROM_EDGE, "the hook reaches the gasket"
    assert GAUGE_CORNER_RELIEF < HOOK_DEPTH - HOOK_LEAD_IN, "the relief leaves the hook no face"
    # The leg must stand clear of the door's front all along (by the assumed
    # curve: the front rises towards the crown).
    assert max(front_y(0), front_y(leg_end())) + 1 <= GAUGE_STANDOFF, "the leg touches the door"
    # The seat must leave the leg a wall, and the wedge must stay below the holes.
    assert leg_outer() - seat_y(-GAUGE_HEIGHT / 2) >= 3, "the wedge seat cuts through the leg"
    r = GAUGE_HOLE / 2
    assert all(r + 2 <= z <= GAUGE_HEIGHT / 2 - r - 2 for z in GAUGE_HOLE_HEIGHTS)
    part = frame() - corner_relief() - wedge_seat()
    for x, z in station_holes():
        part -= hole(x, z)
    return handed(part)


def door() -> dict[str, Part]:
    return {"fridge_door": fridge_door(leg_end() + 30, (-GAUGE_HEIGHT / 2 - 40, GAUGE_HEIGHT / 2 + 20))}


def preview_context() -> dict[str, Part]:
    """Wedge and door, built locally (without the server)."""
    return {"gauge_wedge": build_wedge(), **door()}


@model
def gauge():
    """The printed part, in its use position."""
    part = build()
    part.label = "gauge"
    return part


@model
def gauge_on_door():
    """Gauge and wedge on the open fridge door's edge: the assembly to look at."""
    return with_context("gauge_on_door", gauge().shape, {"gauge_wedge": gauge_wedge().shape, **door()})


if __name__ == "__main__":
    present_model(
        "gauge",
        project="fridge-glide",
        part=gauge,
        build=build,
        assembly=gauge_on_door,
        context=preview_context,
    )
