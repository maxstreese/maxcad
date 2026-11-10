"""Rail for a built-in fridge's sliding door coupling, screwed to the furniture door.

A built-in fridge carries the kitchen's furniture front on its own hinges;
the fridge door follows it through a slider (clipped onto the fridge door's
side edge) running in a rail (on the furniture door). The doors pivot about
different axes, so the slider runs along the rail as they open: TRAVEL, away
from the furniture door's edge.

The channel is a diamond (a square turned 45 degrees) with the slot at its
corner facing the fridge door, and the slider's head is a round bar: pulled
or pushed, the head wedges into a 90 degree V and centres itself, touching on
two lines. Both ends flare into a lead-in. A flange against the furniture door
carries countersunk screws above and below the channel.

The part is a cross-section run along x; it prints flat on its flange, so the
layers run along the head's path, the slot opens upwards and every channel
face is at 45 degrees.

Model: `rail`. The rail with the slider between the doors is the slider's
`glide_on_doors`. How it is built and shown: src/cadkit/present.py.
"""

import math

from build123d import Align, Cone, Cylinder, Location, Part, Plane, Polygon, Pos, Rot, extrude, loft
from cad import model

from cadkit import present_model
from context import front_y, handed
from params import (
    CHANNEL_WALL,
    DOOR_GAP,
    FLANGE_MARGIN,
    FLANGE_THICKNESS,
    GLIDE_CLEARANCE,
    HEAD_DIAMETER,
    LEAD_IN,
    LEAD_IN_LENGTH,
    RAIL_END_MARGIN,
    RUN_CLEARANCE,
    SCREW_BEYOND_RAIL,
    SCREW_FROM_END,
    SCREW_HEAD,
    SCREW_HOLE,
    SIDE_CLEARANCE,
    SLIDER_LENGTH,
    SLOT_WIDTH,
    TRAVEL,
    WEB_THICKNESS,
)


def head_x() -> tuple[float, float]:
    """The slider's head along x, doors closed: from the clip's outer face in."""
    return -WEB_THICKNESS, -WEB_THICKNESS + SLIDER_LENGTH


def rail_x() -> tuple[float, float]:
    """The rail along x: the head's closed position to its open one (TRAVEL
    further in), plus a margin at each end."""
    x0, x1 = head_x()
    return x0 - RAIL_END_MARGIN, x1 + TRAVEL + RAIL_END_MARGIN


def channel_half_diagonal(flare: float = 0.0) -> float:
    """Centre to corner of the diamond: its faces sit HEAD_DIAMETER / 2 +
    GLIDE_CLEARANCE (+ flare) from the centre."""
    return (HEAD_DIAMETER / 2 + GLIDE_CLEARANCE + flare) * math.sqrt(2)


def channel_centre() -> tuple[float, float]:
    """(y, z) of the channel's centre line: the head's axis when centred. Its
    back corner sits CHANNEL_WALL in front of the furniture door."""
    return DOOR_GAP - CHANNEL_WALL - channel_half_diagonal(), 0.0


def rail_front() -> float:
    """y of the rail's face towards the fridge door (level with the diamond's
    slot-side corner)."""
    return channel_centre()[0] - channel_half_diagonal()


def rail_half_height() -> float:
    """Half the height of the channel's body."""
    return channel_half_diagonal() + CHANNEL_WALL


def screw_heights() -> list[float]:
    z = rail_half_height() + SCREW_BEYOND_RAIL
    return [z, -z]


def _yz(points: list[tuple[float, float]], x: float = 0.0):
    """A polygon given as (y, z) points, in the plane x = `x`."""
    return Plane.YZ.offset(x) * Polygon(*points, align=None)


def along_x(face, length: float) -> Part:
    """Extrude a y-z cross-section along +x, whichever way its points wind."""
    return extrude(face, length, dir=(1, 0, 0))


def body() -> Part:
    """Channel body and flange as one cross-section, run along the rail."""
    x0, x1 = rail_x()
    back, front, h = DOOR_GAP, rail_front(), rail_half_height()
    flange_front = DOOR_GAP - FLANGE_THICKNESS
    f = screw_heights()[0] + FLANGE_MARGIN
    profile = _yz(
        [
            (back, f),
            (flange_front, f),
            (flange_front, h),
            (front, h),
            (front, -h),
            (flange_front, -h),
            (flange_front, -f),
            (back, -f),
        ],
        x0,
    )
    return along_x(profile, x1 - x0)


def channel_profile(x: float, flare: float = 0.0):
    """The diamond plus the slot, which leaves the fridge-side corner SLOT_WIDTH
    wide and widens at 45 degrees; `flare` grows every face outward."""
    yc, zc = channel_centre()
    a = channel_half_diagonal(flare)
    s = SLOT_WIDTH / 2 + flare
    y_slot = yc - a + s  # where the slot's walls leave the diamond
    y_out = rail_front() - 1  # past the rail's front
    w = s + (y_slot - y_out)
    return _yz(
        [
            (yc + a, zc),
            (yc, zc - a),
            (y_slot, zc - s),
            (y_out, zc - w),
            (y_out, zc + w),
            (y_slot, zc + s),
            (yc, zc + a),
        ],
        x,
    )


def channel_cut() -> Part:
    """The channel along the whole rail, flaring into a lead-in at both ends
    (and 1 mm past them, so no face of the cut lies on an end face)."""
    x0, x1 = rail_x()
    sections = [
        (x0 - 1, LEAD_IN),
        (x0, LEAD_IN),
        (x0 + LEAD_IN_LENGTH, 0),
        (x1 - LEAD_IN_LENGTH, 0),
        (x1, LEAD_IN),
        (x1 + 1, LEAD_IN),
    ]
    return loft([channel_profile(x, f) for x, f in sections], ruled=True)


def countersunk_hole(x: float, y: float, z: float) -> Part:
    """Screw hole along +y from the face at y, countersunk there."""
    along_y = Rot(-90, 0, 0)  # turns +z into +y
    hole = Pos(x, y - 1, z) * along_y * Cylinder(
        SCREW_HOLE / 2, FLANGE_THICKNESS + 2, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    # 90 degree cone, starting 0.5 mm in front of the face so it cuts it cleanly.
    r0 = SCREW_HEAD / 2 + 0.5
    sink = Pos(x, y - 0.5, z) * along_y * Cone(
        r0, SCREW_HOLE / 2, r0 - SCREW_HOLE / 2, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    return hole + sink


def screw_xs() -> list[float]:
    x0, x1 = rail_x()
    return [x0 + SCREW_FROM_END, (x0 + x1) / 2, x1 - SCREW_FROM_END]


def build() -> Part:
    x0, x1 = rail_x()
    assert -x0 < SIDE_CLEARANCE, "the rail reaches past the space beside the fridge door"
    # The head must bear on the channel's faces, not on the slot's edges: its
    # contact lines lie (r + clearance) * sin 45 either side of its axis.
    contact = (HEAD_DIAMETER / 2 + GLIDE_CLEARANCE) * math.sqrt(0.5)
    assert SLOT_WIDTH / 2 < contact - 0.2, "the slot swallows the head's contact lines"
    # The flared channel must not break through the body's walls, and the head
    # must stay out of the flare at both ends of its travel.
    assert channel_half_diagonal(LEAD_IN) < rail_half_height()
    assert RAIL_END_MARGIN > LEAD_IN_LENGTH, "the head runs into the lead-in"
    # Doors closed, the rail must clear the fridge door's (curved) front.
    crown = max(front_y(x) for x in (0, x1))  # the front rises towards the crown
    assert rail_front() - crown >= RUN_CLEARANCE, "the rail hits the fridge door's front"
    part = body() - channel_cut()
    for x in screw_xs():
        for z in screw_heights():
            part -= countersunk_hole(x, DOOR_GAP - FLANGE_THICKNESS, z)
    return handed(part)


# Flat on its flange: the furniture door side (+y) goes down onto the bed.
PRINT_ROTATION = (-90, 0, 0)


@model
def rail():
    """The printed part, in its use position."""
    part = build()
    part.label = "rail"
    return part


if __name__ == "__main__":
    present_model(
        "rail",
        project="fridge-glide",
        part=rail,
        build=build,
        print_orientation=Location((0, 0, 0), PRINT_ROTATION),
    )
