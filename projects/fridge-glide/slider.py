"""Slider for the fridge door coupling, clipped onto the fridge door's side edge.

No holes in the fridge door: a clip wraps around its side edge on the opening
side, pinching the door between a short leg on the front face and a hook
behind the back face (outside the gasket), joined by a thin web on the side
face. The leg's contact face follows the door's curved front. From the leg a
neck reaches across the gap to the head, a round bar chamfered at both ends,
which runs in the rail on the furniture door.

The head sits right at the edge, so the pull that opens the fridge (breaking
its seal) always acts close to the clip, closed or open.

The part prints standing on its web: the head is then a vertical, truly round
cylinder, and the clip's walls rise straight from the bed.

Models: `slider` (the printed part) and `glide_on_doors` (slider and rail
between the closed doors). How they are built and shown: src/cadkit/present.py.
"""

from build123d import Circle, Location, Part, Plane, Polygon, Pos, chamfer, extrude
from cad import model

from cadkit import present_model, with_context
from context import back_y, door_prism, fridge_door, front_y, furniture_door, handed
from params import (
    CLIP_HEIGHT,
    FRONT_LEG_THICKNESS,
    GASKET_FROM_EDGE,
    GRIP_INTERFERENCE,
    HEAD_CHAMFER,
    HEAD_DIAMETER,
    HOOK_DEPTH,
    HOOK_LEAD_IN,
    HOOK_THICKNESS,
    LEG_BEYOND_HEAD,
    NECK_THICKNESS,
    OPENING_SIDE,
    RUN_CLEARANCE,
    SIDE_CLEARANCE,
    WEB_THICKNESS,
)
from rail import _yz, along_x, channel_centre, head_x, rail, rail_front, rail_x
from rail import build as build_rail


def leg_end() -> float:
    return head_x()[1] + LEG_BEYOND_HEAD


def leg_front() -> float:
    """The leg stands FRONT_LEG_THICKNESS in front of the door's foremost point
    under it (towards the crown, at its inner end)."""
    return max(front_y(0), front_y(leg_end())) + FRONT_LEG_THICKNESS


def leg_back() -> float:
    """y the leg reaches back to in the plan: 1 mm behind the door's front face
    (the arc then cuts it back to the face)."""
    return min(front_y(0), front_y(leg_end() + 1)) - 1


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
        (leg_end(), leg_back()),
        (leg_end(), leg_front()),
        (w, leg_front()),
        align=None,
    )
    return Pos(0, 0, -CLIP_HEIGHT / 2) * extrude(plan, CLIP_HEIGHT, dir=(0, 0, 1))


def build() -> Part:
    assert WEB_THICKNESS < SIDE_CLEARANCE, "the web does not fit beside the door"
    assert HOOK_DEPTH < GASKET_FROM_EDGE, "the hook reaches the gasket"
    assert HOOK_LEAD_IN < min(HOOK_THICKNESS, HOOK_DEPTH)
    assert rail_front() - leg_front() >= RUN_CLEARANCE, "the rail hits the slider's leg"
    yc, zc = channel_centre()
    x0, x1 = head_x()
    n = NECK_THICKNESS / 2

    head = along_x(Plane.YZ.offset(x0) * Pos(yc, zc) * Circle(HEAD_DIAMETER / 2), x1 - x0)
    head = chamfer(head.edges(), HEAD_CHAMFER)
    # From 1 mm inside the leg to the head's axis.
    neck = along_x(_yz([(leg_front() - 1, -n), (yc, -n), (yc, n), (leg_front() - 1, n)], x0), x1 - x0)
    part = clip() + neck + head
    # The door, seen from above and run over the clip's height, cuts the leg
    # back to its curved front face. It starts at the side edge and its back
    # line stays in front of the hook, so only the leg is touched.
    z = (-CLIP_HEIGHT / 2 - 1, CLIP_HEIGHT / 2 + 1)
    return handed(part - door_prism((0, leg_end() + 1), leg_back() - 1, z))


# Standing on its web: the clip's outer face (x = -WEB_THICKNESS as drawn, the
# other way round once mirrored for a left door) goes down onto the bed.
PRINT_ROTATION = (0, -90, 0) if OPENING_SIDE == "right" else (0, 90, 0)


def doors() -> dict[str, Part]:
    x0, x1 = rail_x()
    z = (-50, 50)
    return {
        "fridge_door": fridge_door(x1 + 40, z),
        "furniture_door": furniture_door((-30, x1 + 40), z),
    }


def preview_context() -> dict[str, Part]:
    """Rail and doors, built locally (without the server)."""
    return {"rail": build_rail(), **doors()}


@model
def slider():
    """The printed part, in its use position."""
    part = build()
    part.label = "slider"
    return part


@model
def glide_on_doors():
    """Slider and rail between the closed doors: the assembly to look at."""
    return with_context("glide_on_doors", slider().shape, {"rail": rail().shape, **doors()})


if __name__ == "__main__":
    present_model(
        "slider",
        project="fridge-glide",
        part=slider,
        build=build,
        assembly=glide_on_doors,
        context=preview_context,
        print_orientation=Location((0, 0, 0), PRINT_ROTATION),
    )
