"""Non-printed geometry shown next to the parts: a door."""

from build123d import Color, Part

from cadkit.features import box
from params import DOOR_THICKNESS

# RGBA as numbers: a Color at module level would load the kernel on every run
# of a model script, a replay included.
WOOD = (0.80, 0.66, 0.47, 0.6)


def door_corner(width: float, height: float) -> Part:
    """Top right corner of a door: right edge at x=0, top edge at y=0, face at z=0."""
    d = box((-width, 0), (-height, 0), (-DOOR_THICKNESS, 0))
    d.color = Color(*WOOD)
    return d
