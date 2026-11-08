"""Stopper for the curtain rail's lower (glider) channel, entirely inside the rail.

The body follows the channel's cross-section, including its rounded bottom,
shrunk by the fit clearance all around. A short stem fills the 6 mm slot up
to the rail's underside. An M3x5 set screw (flat point) threads straight
into a 2.5 mm hole in the plastic and is reached from below through the slot
with a 1.5 mm hex key. Tightening it presses the tip against the underside
of the web; the reaction pushes the body down into the rounded bottom of the
channel, which centres it and clamps it along the whole curve. Since nothing
sticks out, it can be clamped anywhere along the rail.

Coordinates match context.rail(): x across, z up from the rail bottom,
the stopper is pushed in along +y (the +y end is the tapered nose).

This part is the pilot for text-to-cad models: `build()` is plain build123d,
and the two `@model` functions are thin wrappers around it that text-to-cad's
server builds, rebuilds and shows (`stopper`, the printed part, and
`stopper_in_rail`, the assembly with the rail and the set screw). With
CAD_VIEWER=none or yacv the script takes the old path through `present`
instead, so `mise run build` and CI need no server.
"""

from build123d import Compound, Location, Part, offset
from cad import model

from cadkit import export_printable, present, viewer_choice
from cadkit.features import box, loft_profiles, vertical_hole
from context import channel_cavity, rail, screw
from params import (
    FIT_SLIDE,
    FIT_SLOT,
    M3_TAP_DRILL,
    RAIL_SLOT,
    RAIL_WEB_BOTTOM,
    SET_SCREW_LENGTH,
    STOPPER_LENGTH,
    STOPPER_NOSE_CHAMFER,
)


def build(length: float = STOPPER_LENGTH, slide: float = FIT_SLIDE, slot: float = FIT_SLOT) -> Part:
    """The stopper; `length` and the clearances can be overridden."""
    # Body = channel cross-section shrunk by the clearance all around, with a
    # 45 degree lead-in taper on the nose so it pushes into the rail easily.
    profile = offset(channel_cavity(), -slide)
    nose_profile = offset(channel_cavity(), -slide - STOPPER_NOSE_CHAMFER)
    nose_start = length - STOPPER_NOSE_CHAMFER
    body = loft_profiles([(0, profile), (nose_start, profile), (length, nose_profile)])

    # Stem in the slot. Its bottom sits `slide` above the rail's underside, so it
    # ends up flush once the screw has pushed the body down into its seat. It
    # stops where the nose taper starts, so it never pokes out through the taper.
    stem_half = RAIL_SLOT / 2 - slot
    stem = box((-stem_half, stem_half), (0, nose_start), (slide, 2.0))

    part = body + stem
    part -= vertical_hole(0, length / 2, (0, RAIL_WEB_BOTTOM), M3_TAP_DRILL)
    return part


PREVIEW_INSET = 5.0  # how far the stopper sits inside the rail in the preview
PREVIEW_RAIL_LENGTH = 60.0
# Upside down: the flat top on the bed, the rounded bottom facing up (no
# overhangs), and the screw hole printed vertically for good threads. Numbers,
# not a Location: a kernel object at module level would load the kernel on
# every run, a replay included.
PRINT_ROTATION = (180, 0, 0)


def preview_context() -> dict[str, Part]:
    """What the stopper sits in, for the preview only: the rail and the set screw."""
    return {
        "rail": rail(PREVIEW_RAIL_LENGTH).moved(Location((0, -PREVIEW_INSET, 0))),
        "set_screw_m3x5": screw(
            0, STOPPER_LENGTH / 2, (RAIL_WEB_BOTTOM - SET_SCREW_LENGTH, RAIL_WEB_BOTTOM), 3.0
        ),
    }


@model
def stopper():
    """The printed part, in its use position."""
    part = build()
    part.label = "stopper"
    return part


@model
def stopper_in_rail():
    """The stopper clamped in the rail with its set screw: the assembly to look at."""
    children = [stopper().shape]
    for label, shape in preview_context().items():
        shape.label = label
        children.append(shape)
    return Compound(children=children, label="stopper_in_rail")


if __name__ == "__main__":
    print_orientation = Location((0, 0, 0), PRINT_ROTATION)
    if viewer_choice() == "text-to-cad":
        # Built and shown by text-to-cad's server (prints id: and view:);
        # the printable files are written from the same build.
        stopper_in_rail()
        export_printable(
            "stopper", stopper().shape, project="curtain-rail", print_orientation=print_orientation
        )
    else:
        present(
            "stopper",
            build(),
            project="curtain-rail",
            print_orientation=print_orientation,
            context=preview_context(),
        )
