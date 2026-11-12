"""Corner drill template for the door handles.

The template sits on the door's front face at a corner and hooks over the
side edge and the top (or bottom) edge with two fences, so every door gets its
holes in the same place. The fences stop short of the corner, so the corner itself
(often slightly rounded or chipped) doesn't affect the position.
Both screw holes are drilled straight through the plate, which doubles as the
drill guide.

Where the holes go is the template's options (options.py): `build(options)`
makes it for any of them, and each configuration named in VARIANTS is a model
and a set of printable files of its own.

Coordinates match context.door_corner(), drawn for the top right corner: side
edge at x=0 (door at x<0), top edge at y=0 (door at y<0), front face at z=0
(door at z<0). context.at_corner() moves the finished part to another corner;
four corners make two printed parts, a template and its mirror image.

Models, per variant: the printed part (`drill_template`, ...) and the part on
the door's corner, to look at (`drill_template_on_door`, ...). How they are
built and shown: src/cadkit/present.py.
"""

from functools import partial

from build123d import Axis, Compound, GeomType, Location, Part, chamfer
from cad import model

from cadkit import present_model, with_context
from cadkit.features import box, vertical_hole
from context import at_corner, door_corner
from options import VARIANTS, Options
from params import (
    DRILL,
    DRILL_CLEARANCE,
    TEMPLATE_CORNER_RELIEF,
    TEMPLATE_FENCE,
    TEMPLATE_FENCE_CORNER_GAP,
    TEMPLATE_FENCE_DEPTH,
    TEMPLATE_MARGIN,
    TEMPLATE_PLATE,
)


def holes(options: Options) -> list[tuple[float, float]]:
    """(x, y) of the two screw holes, as drawn (top right corner)."""
    x = -options.edge_offset
    return [(x, -options.end_offset), (x, -options.end_offset - options.spacing)]


def build(options: Options = Options()) -> Part:
    x_end = -options.edge_offset - TEMPLATE_MARGIN
    y_end = -options.end_offset - options.spacing - TEMPLATE_MARGIN
    gap = TEMPLATE_FENCE_CORNER_GAP
    z = (-TEMPLATE_FENCE_DEPTH, TEMPLATE_PLATE)

    # The plate covers the door face only; the fences run along the outside of
    # the door's two edges at the corner and end `gap` before the corner.
    plate = box((x_end, 0), (y_end, 0), (0, TEMPLATE_PLATE))
    side_fence = box((0, TEMPLATE_FENCE), (y_end, -gap), z)
    top_fence = box((x_end, -gap), (0, TEMPLATE_FENCE), z)
    part = plate + side_fence + top_fence

    # Soften the outside edges of the plate.
    part = chamfer(part.edges().group_by(Axis.Z)[-1], 1.0)

    # Relief grooves in the inside corners so a rounded door edge can't keep
    # the template from sitting flat and tight against both edges.
    r = TEMPLATE_CORNER_RELIEF
    part -= box((-r, r), (y_end, -gap), (-TEMPLATE_FENCE_DEPTH - 1, r))
    part -= box((x_end, -gap), (-r, r), (-TEMPLATE_FENCE_DEPTH - 1, r))

    guide = DRILL + DRILL_CLEARANCE
    for hx, hy in holes(options):
        part -= vertical_hole(hx, hy, (-1, TEMPLATE_PLATE + 1), guide)
    # Countersink-style lead-in on top so the drill tip finds the hole.
    top_edges = part.edges().filter_by_position(Axis.Z, TEMPLATE_PLATE, TEMPLATE_PLATE)
    part = chamfer([e for e in top_edges if e.geom_type == GeomType.CIRCLE], 0.8)
    return at_corner(part, options.corner)


# Upside down: the flat top face goes on the bed, fences point up. Numbers,
# not a Location: a kernel object at module level would load the kernel on
# every run, a replay included.
PRINT_ROTATION = (180, 0, 0)
PREVIEW_DOOR_BEYOND = 80.0  # door shown beyond the holes, across and down


def preview_context(options: Options = Options()) -> dict[str, Part]:
    """The door's corner the template is made for, for the preview only."""
    width = options.edge_offset + PREVIEW_DOOR_BEYOND
    height = options.end_offset + options.spacing + PREVIEW_DOOR_BEYOND
    return {"door": door_corner(width, height, options.corner)}


def variant(name: str) -> Part:
    """The template of VARIANTS[name], in its use position, labelled `name`."""
    part = build(VARIANTS[name])
    part.label = name
    return part


def on_door(name: str, part) -> Compound:
    """`part`, the built template of VARIANTS[name], hooked over its door's corner."""
    return with_context(f"{name}_on_door", part, preview_context(VARIANTS[name]))


# One @model per variant and one for its assembly: text-to-cad gives each
# configuration an id and a page of its own.


@model
def drill_template():
    """The template in use: the printed part, in its use position."""
    return variant("drill_template")


@model
def drill_template_on_door():
    """The template hooked over the door's corner: the assembly to look at."""
    return on_door("drill_template", drill_template().shape)


@model
def drill_template_top_left():
    return variant("drill_template_top_left")


@model
def drill_template_top_left_on_door():
    return on_door("drill_template_top_left", drill_template_top_left().shape)


@model
def drill_template_128():
    return variant("drill_template_128")


@model
def drill_template_128_on_door():
    return on_door("drill_template_128", drill_template_128().shape)


MODELS = {
    "drill_template": (drill_template, drill_template_on_door),
    "drill_template_top_left": (drill_template_top_left, drill_template_top_left_on_door),
    "drill_template_128": (drill_template_128, drill_template_128_on_door),
}

if __name__ == "__main__":
    assert MODELS.keys() == VARIANTS.keys(), "every variant in options.py needs its models here"
    prints = [options.printed_as for options in VARIANTS.values()]
    assert len(set(prints)) == len(prints), (
        "two variants in options.py print the same part (diagonally opposite corners share one)"
    )
    for name, (part, assembly) in MODELS.items():
        present_model(
            name,
            project="door-handles",
            part=part,
            build=partial(build, VARIANTS[name]),
            assembly=assembly,
            context=partial(preview_context, VARIANTS[name]),
            print_orientation=Location((0, 0, 0), PRINT_ROTATION),
            options=VARIANTS[name],
            variant_of="drill_template",
        )
