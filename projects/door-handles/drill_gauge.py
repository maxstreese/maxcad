"""Drill gauge to print before the drill template.

Guide holes from DRILL + 0.0 to DRILL + 0.4 mm, labelled on top. Pick the one
your drill bit turns freely in without wobble; the extra becomes
DRILL_CLEARANCE in params.py.

Modelled in its print orientation.

Model: `drill_gauge`. How it is built and shown: src/cadkit/present.py.
"""

from build123d import Align, Part, Pos, Text, extrude
from cad import model

from cadkit import present_model
from cadkit.features import box, vertical_hole
from params import DRILL, TEMPLATE_PLATE

STEPS = [0.0, 0.1, 0.2, 0.3, 0.4]
PITCH = 12.0
ENGRAVE = 0.4


def build() -> Part:
    # Same thickness as the template, so the holes print and guide the same way.
    plate = box((0, PITCH * len(STEPS)), (0, 16), (0, TEMPLATE_PLATE))
    for i, extra in enumerate(STEPS):
        x = PITCH * (i + 0.5)
        plate -= vertical_hole(x, 5, (-1, TEMPLATE_PLATE + 1), DRILL + extra)
        label = extrude(Text(f"+{extra:.1f}", 3, align=(Align.CENTER, Align.CENTER)), ENGRAVE)
        plate -= Pos(x, 12.5, TEMPLATE_PLATE - ENGRAVE) * label
    return plate


@model
def drill_gauge():
    part = build()
    part.label = "drill_gauge"
    return part


if __name__ == "__main__":
    present_model("drill_gauge", project="door-handles", part=drill_gauge, build=build)
