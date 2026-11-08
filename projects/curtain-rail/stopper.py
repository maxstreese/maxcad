"""Stopper for the curtain rail's lower (glider) channel, entirely inside the rail.

The body follows the channel's cross-section, including its rounded bottom,
shrunk by the fit clearance all around. A short stem fills the 6 mm slot up
to the rail's underside. An M3x5 set screw (flat point) runs in a heat-set
insert (CNC Kitchen M3 x 3 short), pressed in from the top face, and is
reached from below through the slot and a free hole in the stem with a
1.5 mm hex key. Tightening it presses the tip against the underside
of the web; the reaction pushes the body down into the rounded bottom of the
channel, which centres it and clamps it along the whole curve. Since nothing
sticks out, it can be clamped anywhere along the rail.

Coordinates match context.rail(): x across, z up from the rail bottom,
the stopper is pushed in along +y (the +y end is the tapered nose).

Models: `stopper` (the printed part) and `stopper_in_rail` (with the rail,
the insert and the set screw, to look at). How they are built and shown: src/cadkit/present.py.
"""

from build123d import Location, Part, offset
from cad import model

from cadkit import present_model, with_context
from cadkit.features import box, loft_profiles, vertical_hole
from context import channel_cavity, insert, rail, screw
from params import (
    FIT_SLIDE,
    FIT_SLOT,
    INSERT_DIAMETER,
    INSERT_HOLE,
    INSERT_HOLE_EXTRA,
    INSERT_LENGTH,
    M3_CLEARANCE,
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

    # The insert goes in from the top face (the stem is too narrow for its
    # walls), a little deeper than it is long; below it a free hole for the
    # screw through the stem.
    top = RAIL_WEB_BOTTOM - slide
    insert_bottom = top - INSERT_LENGTH - INSERT_HOLE_EXTRA
    part = body + stem
    part -= vertical_hole(0, length / 2, (insert_bottom, top + 1), INSERT_HOLE)
    part -= vertical_hole(0, length / 2, (-1, insert_bottom + 0.1), M3_CLEARANCE)
    return part


PREVIEW_INSET = 5.0  # how far the stopper sits inside the rail in the preview
PREVIEW_RAIL_LENGTH = 60.0
# Upside down: the flat top on the bed, the rounded bottom facing up (no
# overhangs), the insert hole opening on the bed side and printed vertically,
# round. Numbers,
# not a Location: a kernel object at module level would load the kernel on
# every run, a replay included.
PRINT_ROTATION = (180, 0, 0)


def preview_context() -> dict[str, Part]:
    """What the stopper sits in, for the preview only: the rail, the insert and the set screw."""
    return {
        "rail": rail(PREVIEW_RAIL_LENGTH).moved(Location((0, -PREVIEW_INSET, 0))),
        "insert_m3x3": insert(
            0, STOPPER_LENGTH / 2, RAIL_WEB_BOTTOM - FIT_SLIDE, INSERT_LENGTH, INSERT_DIAMETER, 3.0
        ),
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
    return with_context("stopper_in_rail", stopper().shape, preview_context())


if __name__ == "__main__":
    present_model(
        "stopper",
        project="curtain-rail",
        part=stopper,
        build=build,
        assembly=stopper_in_rail,
        context=preview_context,
        print_orientation=Location((0, 0, 0), PRINT_ROTATION),
    )
