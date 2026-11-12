"""Declared options of a part: what someone may choose, and within which limits.

Every number in a project's `params.py` can be edited, but nothing promises
the part still builds or works afterwards. An option is such a promise: a
project's `options.py` lists the few values meant to be chosen in a frozen
dataclass, each with its limits, and names the configurations that get built
(`VARIANTS`). Everything else stays a fixed number in `params.py`.

    @dataclass(frozen=True)
    class Options:
        spacing: float = number(96.0, "screw centre distance", low=32.0, high=224.0)
        corner: Literal["top_right", "top_left"] = choice("top_right", "the corner it hooks over")

        def __post_init__(self):
            check(self)

A number option has a range, a choice option is a `Literal` of its values
(a feature of the part, not a dimension). `check` refuses anything outside
them, so a part's `build(options)` only ever sees values it was made for.
No kernel in here: an `options.py` stays plain numbers and strings.
"""

from dataclasses import Field, field, fields
from typing import Any, Literal, get_args, get_origin, get_type_hints


def number(default: float, doc: str, *, low: float, high: float, unit: str = "mm") -> Any:
    """A numeric option, valid from `low` to `high` (both included)."""
    return field(default=default, metadata={"doc": doc, "low": low, "high": high, "unit": unit})


def choice(default: str, doc: str) -> Any:
    """An option picked from the values of the field's `Literal` type."""
    return field(default=default, metadata={"doc": doc})


def check(options: Any) -> None:
    """Raise ValueError unless every field of `options` is within what it declares."""
    hints = get_type_hints(type(options))
    for f in fields(options):
        value = getattr(options, f.name)
        hint = hints[f.name]
        if get_origin(hint) is Literal:
            if value not in get_args(hint):
                expected = ", ".join(repr(v) for v in get_args(hint))
                raise ValueError(f"{f.name}={value!r}: expected one of {expected}")
        else:
            _check_number(f, value)


def _check_number(f: Field, value: Any) -> None:
    if "low" not in f.metadata:
        raise TypeError(f"{f.name}: declare it with number(...) or as a Literal with choice(...)")
    low, high, unit = f.metadata["low"], f.metadata["high"], f.metadata["unit"]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{f.name}={value!r}: expected a number")
    if not low <= value <= high:
        raise ValueError(f"{f.name}={value!r}: expected {low} to {high} {unit}")
