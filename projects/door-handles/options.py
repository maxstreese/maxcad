"""What the drill template lets you choose, and the configurations that get built.

These are the project's options (src/cadkit/options.py): the template builds
for any values within the limits below. Everything else is a fixed number in
params.py. The drill gauge has no options.
"""

from dataclasses import dataclass
from typing import Literal

from cadkit.options import check, choice, number


@dataclass(frozen=True)
class Options:
    spacing: float = number(96.0, "screw centre distance of the handle", low=32.0, high=224.0)
    edge_offset: float = number(
        28.0,
        "side edge of the door to the screw centre line; also the length of the fence on the top or bottom edge",
        low=20.0,
        high=100.0,
    )
    end_offset: float = number(
        28.0,
        "the corner's top or bottom edge of the door to the screw nearest to it",
        low=10.0,
        high=100.0,
    )
    corner: Literal["top_right", "top_left", "bottom_right", "bottom_left"] = choice(
        "top_right",
        "the corner of the door the template hooks over, seen from the front",
    )

    def __post_init__(self) -> None:
        check(self)

    @property
    def at_left(self) -> bool:
        return self.corner in ("top_left", "bottom_left")

    @property
    def at_bottom(self) -> bool:
        return self.corner in ("bottom_right", "bottom_left")

    @property
    def printed_as(self) -> tuple:
        """What tells one printed template from another. Four corners make two
        parts: a template turned half round fits the diagonally opposite
        corner, so only whether it is the mirrored one counts."""
        return self.spacing, self.edge_offset, self.end_offset, self.at_left != self.at_bottom


# Every configuration that gets built and exported, by the name of its model
# and of its files in out/door-handles/. The first is the one in use. No two
# may print the same part (drill_template.py checks).
VARIANTS = {
    "drill_template": Options(),
    "drill_template_top_left": Options(corner="top_left"),
    "drill_template_128": Options(spacing=128.0),
}
