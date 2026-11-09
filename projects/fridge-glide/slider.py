"""Slider for the fridge door coupling, screwed to the furniture door.

A round head (a bar along the rail, chamfered at both ends to find the rail's
lead-in) runs in the rail's diamond channel; a neck through the slot joins it
to a plate on the furniture door's back, with one countersunk screw above
and one below the rail. The top and the bottom coupling are the same part.

The part is a cross-section run along x, plus the head's chamfers and the
screw holes, so it prints standing on one end: the head comes out truly round,
and its rings ride over the rail's smooth channel faces.

Models: `slider` (the printed part) and `glide_on_doors` (rail, slider and
both doors). How they are built and shown: src/cadkit/present.py.
"""

from build123d import Align, Circle, Cone, Cylinder, Location, Part, Plane, Pos, Rot, chamfer
from cad import model

from cadkit import present_model, with_context
from context import fridge_door, furniture_door, handed
from params import (
    DOOR_GAP,
    HEAD_CHAMFER,
    HEAD_DIAMETER,
    NECK_THICKNESS,
    PLATE_MARGIN,
    PLATE_THICKNESS,
    RAIL_LENGTH,
    RUN_CLEARANCE,
    SCREW_BEYOND_RAIL,
    SCREW_HEAD,
    SCREW_HOLE,
    SLIDER_LENGTH,
)
from rail import _yz, along_x, channel_centre, rail, rail_front, rail_half_height
from rail import build as build_rail

# In use the slider sits in the middle of the rail (the doors half open).
X0 = (RAIL_LENGTH - SLIDER_LENGTH) / 2


def screw_heights() -> list[float]:
    z = rail_half_height() + SCREW_BEYOND_RAIL
    return [z, -z]


def countersunk_hole(x: float, y: float, z: float) -> Part:
    """Screw hole along +y from the plate's rail side (y), countersunk there."""
    along_y = Rot(-90, 0, 0)  # turns +z into +y
    hole = Pos(x, y - 1, z) * along_y * Cylinder(
        SCREW_HOLE / 2, PLATE_THICKNESS + 2, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    # 90 degree cone, starting 0.5 mm in front of the face so it cuts it cleanly.
    r0 = SCREW_HEAD / 2 + 0.5
    sink = Pos(x, y - 0.5, z) * along_y * Cone(
        r0, SCREW_HOLE / 2, r0 - SCREW_HOLE / 2, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    return hole + sink


def build() -> Part:
    yc, zc = channel_centre()
    y_plate = DOOR_GAP - PLATE_THICKNESS
    assert y_plate - rail_front() >= RUN_CLEARANCE, "DOOR_GAP too small: the plate hits the rail"
    top = screw_heights()[0] + PLATE_MARGIN
    bottom = -top
    n = NECK_THICKNESS / 2

    head = along_x(Plane.YZ.offset(X0) * Pos(yc, zc) * Circle(HEAD_DIAMETER / 2), SLIDER_LENGTH)
    head = chamfer(head.edges(), HEAD_CHAMFER)
    neck_and_plate = along_x(
        _yz(
            [
                (yc, zc - n),
                (y_plate, zc - n),
                (y_plate, bottom),
                (DOOR_GAP, bottom),
                (DOOR_GAP, top),
                (y_plate, top),
                (y_plate, zc + n),
                (yc, zc + n),
            ],
            X0,
        ),
        SLIDER_LENGTH,
    )
    part = head + neck_and_plate
    for z in screw_heights():
        part -= countersunk_hole(X0 + SLIDER_LENGTH / 2, y_plate, z)
    return handed(part)


# Standing on one end: the slider's x (along the rail) becomes the print's z.
PRINT_ROTATION = (0, -90, 0)


def doors() -> dict[str, Part]:
    z = (-60, 60)
    return {
        "fridge_door": fridge_door(RAIL_LENGTH + 60, z),
        "furniture_door": furniture_door((-40, RAIL_LENGTH + 60), z),
    }


def preview_context() -> dict[str, Part]:
    """Rail and doors, built locally (without the server)."""
    return {"rail": build_rail(), **doors()}


@model
def slider():
    """The printed part, in its use position (in the middle of the rail)."""
    part = build()
    part.label = "slider"
    return part


@model
def glide_on_doors():
    """Rail and slider between the closed doors: the assembly to look at."""
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
