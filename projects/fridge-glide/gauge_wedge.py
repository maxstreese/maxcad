"""Wedge for the profile gauge (gauge.py): it holds the gauge's hook on the
fridge door's back face while the front is measured.

The gauge's leg stands off the door's front; right opposite the hook its inner
face is a seat sloped along the door's edge (WEDGE_SLOPE). The wedge has the
same slope: pushed up between the door's front and the seat (thick end down)
it presses the door against the hook, and it holds itself. Only a narrow rib
touches the door, in line with the hook, so the clamping does not turn the
gauge off the door's side face.

It prints lying on its side, so the slope lies in the bed plane.

Model: `gauge_wedge`. It is shown on the door with the gauge (`gauge_on_door`).
How it is built and shown: src/cadkit/present.py.
"""

from build123d import Location, Part
from cad import model

from cadkit import present_model
from cadkit.features import box
from context import front_y, handed
from params import (
    GAUGE_HEIGHT,
    GAUGE_STANDOFF,
    OPENING_SIDE,
    SEAT_TOP_DEPTH,
    WEDGE_LENGTH,
    WEDGE_RIB,
    WEDGE_RIB_X,
    WEDGE_SEAT_X,
    WEDGE_SLOPE,
    WEDGE_TIP_Z,
    WEDGE_X,
)
from rail import _yz, along_x


def seat_y(z: float) -> float:
    """y of the gauge's wedge seat at height z: SEAT_TOP_DEPTH behind the leg's
    inner face at the gauge's top, further from the door towards its bottom."""
    return GAUGE_STANDOFF + SEAT_TOP_DEPTH + (GAUGE_HEIGHT / 2 - z) * WEDGE_SLOPE


def build() -> Part:
    """The wedge where it comes to rest on a door of DOOR_THICKNESS with the
    assumed front: tip at WEDGE_TIP_Z, thick end below the gauge. The rib's
    inner corner touches the front, which stands furthest forward there."""
    x0, x1 = WEDGE_X
    assert 0 < x0 < WEDGE_RIB_X < x1 < WEDGE_SEAT_X
    top, bottom = WEDGE_TIP_Z, WEDGE_TIP_Z - WEDGE_LENGTH
    assert -GAUGE_HEIGHT / 2 < top < GAUGE_HEIGHT / 2
    door = max(front_y(x0), front_y(WEDGE_RIB_X))
    face = door + WEDGE_RIB
    body = along_x(
        _yz([(face, top), (seat_y(top), top), (seat_y(bottom), bottom), (face, bottom)], x0),
        x1 - x0,
    )
    rib = box((x0, WEDGE_RIB_X), (door, face + 1), (bottom, top))
    return handed(body + rib)


# Lying on the side the rib is flush with (x = WEDGE_X[0] as drawn).
PRINT_ROTATION = (0, -90, 0) if OPENING_SIDE == "right" else (0, 90, 0)


@model
def gauge_wedge():
    """The printed part, in its use position."""
    part = build()
    part.label = "gauge_wedge"
    return part


if __name__ == "__main__":
    present_model(
        "gauge_wedge",
        project="fridge-glide",
        part=gauge_wedge,
        build=build,
        print_orientation=Location((0, 0, 0), PRINT_ROTATION),
    )
