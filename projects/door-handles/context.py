"""Non-printed geometry shown next to the parts: a door."""

from build123d import Color, Part, Plane, mirror

from cadkit.features import box
from params import DOOR_THICKNESS

# RGBA as numbers: a Color at module level would load the kernel on every run
# of a model script, a replay included.
WOOD = (0.80, 0.66, 0.47, 0.6)


def at_corner(shape, corner: str):
    """`shape` as drawn (at the top right corner: the door at x<0, y<0), moved
    to `corner`: mirrored across x=0 for a left corner (the door at x>0) and
    across y=0 for a bottom one (the door at y>0). Both together are a half
    turn, so the bottom left shape is the top right one, turned."""
    if corner.endswith("_left"):
        shape = mirror(shape, Plane.YZ)
    if corner.startswith("bottom_"):
        shape = mirror(shape, Plane.XZ)
    return shape


def door_corner(width: float, height: float, corner: str = "top_right") -> Part:
    """A corner of a door: side edge at x=0, top or bottom edge at y=0, face at z=0."""
    d = at_corner(box((-width, 0), (-height, 0), (-DOOR_THICKNESS, 0)), corner)
    d.color = Color(*WOOD)
    return d
