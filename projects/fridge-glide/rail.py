"""Rail for a built-in fridge's sliding door coupling, clipped onto the fridge door.

A built-in fridge carries the kitchen's furniture front on its own hinges;
the fridge door follows it through a slider (on the furniture door) running in
a rail (on the fridge door). The doors pivot about different axes, so the
slider runs along the rail as they open.

This rail needs no holes in the fridge door: a clip wraps around the door's
side edge on its opening side, pinching the door between a leg on the front
face and a short hook behind the back face (outside the gasket), joined by a
thin web on the side face. The door's front is curved from side to side; the
leg's contact face follows that arc over its whole length (the plan is drawn
with the leg reaching back past the arc, which is then cut away). The rail runs
straight along the leg, in from the edge, parallel to the furniture door.

The channel is a diamond (a square turned 45 degrees) with the slot at its
front corner, and the slider's head is a round bar: pulled or pushed, the head
wedges into a 90 degree V and centres itself, touching on two lines. Both rail
ends flare into a lead-in.

The part prints standing, as mounted: the clip's plan lies in the layers (the
strong way for its flexing), the channel's faces and the rail's underside are
at 45 degrees, and the layers run along the slider's path. The top and the
bottom coupling are the same part. It is drawn for a door opening on the right
and mirrored for one opening on the left (OPENING_SIDE).

Models: `rail` (the printed part) and `rail_on_door`. How they are built and
shown: src/cadkit/present.py.
"""

import math

from build123d import Part, Plane, Polygon, Pos, extrude, loft
from cad import model

from cadkit import present_model, with_context
from context import back_y, door_prism, fridge_door, front_y, handed
from params import (
    CHANNEL_WALL,
    CLIP_HEIGHT,
    CROWN_OFFSET,
    FRONT_LEG_THICKNESS,
    GASKET_FROM_EDGE,
    GLIDE_CLEARANCE,
    GRIP_INTERFERENCE,
    HEAD_DIAMETER,
    HOOK_DEPTH,
    HOOK_LEAD_IN,
    HOOK_THICKNESS,
    LEAD_IN,
    LEAD_IN_LENGTH,
    RAIL_LENGTH,
    SIDE_CLEARANCE,
    SLOT_WIDTH,
    WEB_THICKNESS,
)


def face_max() -> float:
    """The door's foremost point under the leg (y = 0 is its face at the rail's
    middle). Off the crown the face is tilted as well as curved, so this is at
    one end, or at the crown if it lies under the leg."""
    crown = RAIL_LENGTH / 2 + CROWN_OFFSET
    return max(front_y(x) for x in (0, crown, RAIL_LENGTH) if 0 <= x <= RAIL_LENGTH)


def leg_front() -> float:
    return face_max() + FRONT_LEG_THICKNESS


def leg_back() -> float:
    """y the leg reaches back to in the plan: 1 mm behind the door's front face
    at its ends (the arc then cuts it back to the face)."""
    return min(front_y(0), front_y(RAIL_LENGTH + 1)) - 1


def channel_half_diagonal(flare: float = 0.0) -> float:
    """Centre to corner of the diamond: its faces sit HEAD_DIAMETER / 2 +
    GLIDE_CLEARANCE (+ flare) from the centre."""
    return (HEAD_DIAMETER / 2 + GLIDE_CLEARANCE + flare) * math.sqrt(2)


def channel_centre() -> tuple[float, float]:
    """(y, z) of the channel's centre line: the head's axis when centred."""
    return leg_front() + CHANNEL_WALL + channel_half_diagonal(), 0.0


def rail_front() -> float:
    """y of the rail's front face (level with the diamond's front corner)."""
    return channel_centre()[0] + channel_half_diagonal()


def rail_half_height() -> float:
    return channel_half_diagonal() + CHANNEL_WALL


def _yz(points: list[tuple[float, float]], x: float = 0.0):
    """A polygon given as (y, z) points, in the plane x = `x`."""
    return Plane.YZ.offset(x) * Polygon(*points, align=None)


def along_x(face, length: float) -> Part:
    """Extrude a y-z cross-section along +x, whichever way its points wind."""
    return extrude(face, length, dir=(1, 0, 0))


def clip() -> Part:
    """The clip in plan (x, y), run over CLIP_HEIGHT: hook behind the back face,
    web on the side face, leg along the front face."""
    y_in = back_y() + GRIP_INTERFERENCE  # the hook's inner face: pinches the door
    y_out = y_in - HOOK_THICKNESS
    w = -WEB_THICKNESS
    plan = Polygon(
        (w, y_out),
        (HOOK_DEPTH, y_out),
        (HOOK_DEPTH, y_in - HOOK_LEAD_IN),
        (HOOK_DEPTH - HOOK_LEAD_IN, y_in),
        (0, y_in),
        (0, leg_back()),
        (RAIL_LENGTH, leg_back()),
        (RAIL_LENGTH, leg_front()),
        (w, leg_front()),
        align=None,
    )
    return Pos(0, 0, -CLIP_HEIGHT / 2) * extrude(plan, CLIP_HEIGHT, dir=(0, 0, 1))


def rail_body() -> Part:
    """The rail in front of the leg, from the web's outer face to the leg's end.
    Its underside slopes back to the leg at 45 degrees, so it prints standing."""
    front, h = rail_front(), rail_half_height()
    back = leg_front() - 1  # 1 mm into the leg, so the two fuse into one
    return along_x(
        _yz([(back, h), (front, h), (front, -h), (back, -h - (front - back))], -WEB_THICKNESS),
        RAIL_LENGTH + WEB_THICKNESS,
    )


def channel_profile(x: float, flare: float = 0.0):
    """The diamond plus the slot, which leaves the front corner SLOT_WIDTH wide
    and widens at 45 degrees; `flare` grows every face outward."""
    yc, zc = channel_centre()
    a = channel_half_diagonal(flare)
    s = SLOT_WIDTH / 2 + flare
    y_slot = yc + a - s  # where the slot's walls leave the diamond
    y_out = rail_front() + 1  # past the front face
    w = s + (y_out - y_slot)
    return _yz(
        [
            (yc - a, zc),
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
    x0, x1 = -WEB_THICKNESS, RAIL_LENGTH
    sections = [
        (x0 - 1, LEAD_IN),
        (x0, LEAD_IN),
        (x0 + LEAD_IN_LENGTH, 0),
        (x1 - LEAD_IN_LENGTH, 0),
        (x1, LEAD_IN),
        (x1 + 1, LEAD_IN),
    ]
    return loft([channel_profile(x, f) for x, f in sections], ruled=True)


def build() -> Part:
    assert WEB_THICKNESS < SIDE_CLEARANCE, "the web does not fit beside the door"
    assert HOOK_DEPTH < GASKET_FROM_EDGE, "the hook reaches the gasket"
    assert HOOK_LEAD_IN < min(HOOK_THICKNESS, HOOK_DEPTH)
    # The flared channel must not break through the rail's top, bottom or back.
    assert channel_half_diagonal(LEAD_IN) < rail_half_height()
    # The rail's sloped underside must end on the leg, inside the clip.
    assert rail_half_height() + (rail_front() - leg_front() + 1) < CLIP_HEIGHT / 2
    part = clip() + rail_body() - channel_cut()
    # The door, seen from above and run over the clip's height, cuts the leg
    # back to its curved front face. It starts at the side edge and its back
    # line stays in front of the hook, so only the leg is touched.
    z = (-CLIP_HEIGHT / 2 - 1, CLIP_HEIGHT / 2 + 1)
    return handed(part - door_prism((0, RAIL_LENGTH + 1), leg_back() - 1, z))


def preview_context() -> dict[str, Part]:
    return {"fridge_door": fridge_door(RAIL_LENGTH + 60, (-60, 60))}


@model
def rail():
    """The printed part, in its use position (and print orientation)."""
    part = build()
    part.label = "rail"
    return part


@model
def rail_on_door():
    """The rail clipped around the fridge door's side edge."""
    return with_context("rail_on_door", rail().shape, preview_context())


if __name__ == "__main__":
    present_model(
        "rail",
        project="fridge-glide",
        part=rail,
        build=build,
        assembly=rail_on_door,
        context=preview_context,
    )
