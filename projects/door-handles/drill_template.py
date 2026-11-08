"""Corner drill template for the door handles.

The template sits on the door's front face at the top right corner and hooks
over the right edge and the top edge with two fences, so every door gets its
holes in the same place. The fences stop short of the corner, so the corner
itself (often slightly rounded or chipped) doesn't affect the position.
Both screw holes are drilled straight through the plate, which doubles as the
drill guide.

Coordinates match context.door_corner(): right edge at x=0 (door at x<0),
top edge at y=0 (door at y<0), front face at z=0 (door at z<0).

Models: `drill_template` (the printed part) and `drill_template_on_door`
(on the door's corner, to look at). How they are built and shown:
src/cadkit/present.py.
"""

from build123d import Axis, GeomType, Location, Part, chamfer
from cad import model

from cadkit import present_model, with_context
from cadkit.features import box, vertical_hole
from context import door_corner
from params import (
    DRILL,
    DRILL_CLEARANCE,
    HANDLE_EDGE_OFFSET,
    HANDLE_SPACING,
    HANDLE_TOP_OFFSET,
    TEMPLATE_CORNER_RELIEF,
    TEMPLATE_FENCE,
    TEMPLATE_FENCE_CORNER_GAP,
    TEMPLATE_FENCE_DEPTH,
    TEMPLATE_MARGIN,
    TEMPLATE_PLATE,
)

HOLES = [
    (-HANDLE_EDGE_OFFSET, -HANDLE_TOP_OFFSET),
    (-HANDLE_EDGE_OFFSET, -HANDLE_TOP_OFFSET - HANDLE_SPACING),
]


def build() -> Part:
    x_end = -HANDLE_EDGE_OFFSET - TEMPLATE_MARGIN
    y_end = -HANDLE_TOP_OFFSET - HANDLE_SPACING - TEMPLATE_MARGIN
    gap = TEMPLATE_FENCE_CORNER_GAP
    z = (-TEMPLATE_FENCE_DEPTH, TEMPLATE_PLATE)

    # The plate covers the door face only; the fences run along the outside of
    # the right and top edges and end `gap` before the corner.
    plate = box((x_end, 0), (y_end, 0), (0, TEMPLATE_PLATE))
    right_fence = box((0, TEMPLATE_FENCE), (y_end, -gap), z)
    top_fence = box((x_end, -gap), (0, TEMPLATE_FENCE), z)
    part = plate + right_fence + top_fence

    # Soften the outside edges of the plate.
    part = chamfer(part.edges().group_by(Axis.Z)[-1], 1.0)

    # Relief grooves in the inside corners so a rounded door edge can't keep
    # the template from sitting flat and tight against both edges.
    r = TEMPLATE_CORNER_RELIEF
    part -= box((-r, r), (y_end, -gap), (-TEMPLATE_FENCE_DEPTH - 1, r))
    part -= box((x_end, -gap), (-r, r), (-TEMPLATE_FENCE_DEPTH - 1, r))

    guide = DRILL + DRILL_CLEARANCE
    for hx, hy in HOLES:
        part -= vertical_hole(hx, hy, (-1, TEMPLATE_PLATE + 1), guide)
    # Countersink-style lead-in on top so the drill tip finds the hole.
    top_edges = part.edges().filter_by_position(Axis.Z, TEMPLATE_PLATE, TEMPLATE_PLATE)
    part = chamfer([e for e in top_edges if e.geom_type == GeomType.CIRCLE], 0.8)
    return part


# Upside down: the flat top face goes on the bed, fences point up. Numbers,
# not a Location: a kernel object at module level would load the kernel on
# every run, a replay included.
PRINT_ROTATION = (180, 0, 0)
PREVIEW_DOOR_WIDTH = 120.0
PREVIEW_DOOR_HEIGHT = HANDLE_TOP_OFFSET + HANDLE_SPACING + 80


def preview_context() -> dict[str, Part]:
    """The door's top right corner, for the preview only."""
    return {"door": door_corner(PREVIEW_DOOR_WIDTH, PREVIEW_DOOR_HEIGHT)}


@model
def drill_template():
    """The printed part, in its use position."""
    part = build()
    part.label = "drill_template"
    return part


@model
def drill_template_on_door():
    """The template hooked over the door's corner: the assembly to look at."""
    return with_context("drill_template_on_door", drill_template().shape, preview_context())


if __name__ == "__main__":
    present_model(
        "drill_template",
        project="door-handles",
        part=drill_template,
        build=build,
        assembly=drill_template_on_door,
        context=preview_context,
        print_orientation=Location((0, 0, 0), PRINT_ROTATION),
    )
