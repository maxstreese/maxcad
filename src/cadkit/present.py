"""Show a part in a viewer and export it for printing.

Every part script writes its part as text-to-cad models: a plain build123d
`build()` function, a `@model` function wrapping it (the printed part), and
optionally a second `@model` that places the part among context geometry
(the rail, the door) for looking at. The script ends with `present_model`,
which

- exports the printable part to out/<project>/<name>.{step,3mf,stl}, with the
  3MF/STL already rotated into the intended print orientation, and
- shows it in a viewer.

CAD_VIEWER picks the viewer:

- `text-to-cad` (default): text-to-cad's server builds the models, rebuilds
  only what an edit changed, and prints each model's page; open pages follow
  every rebuild. The printable files are written from that same build.
- `yacv`: Yet Another CAD Viewer at http://localhost:32323, from a plain
  `build()` without the server.
- `none`: only export, from a plain `build()` (the `mise run build` task and
  CI do this, so neither needs a server).
"""

import os
from collections.abc import Callable
from pathlib import Path
from typing import Any

from build123d import Compound, Location, Mesher, Shape, export_step, export_stl

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "out"


def present_model(
    name: str,
    *,
    project: str,
    part: Callable[[], Any],
    build: Callable[[], Shape],
    assembly: Callable[[], Any] | None = None,
    context: Callable[[], dict[str, Shape]] | None = None,
    print_orientation: Location | None = None,
) -> None:
    """The `__main__` of a part script.

    `part` and `assembly` are the script's `@model` functions; `build` and
    `context` are the plain functions behind them, used without the server.
    `print_orientation` turns the 3MF/STL only; the STEP and the viewers keep
    the part in its use position.
    """
    orientation = print_orientation or Location()
    if viewer_choice() == "text-to-cad":
        # text-to-cad prints a model's page only for calls made in the
        # script's own __main__; these come from here, so print them.
        if assembly is not None:
            print(f"view {assembly.__name__}: {assembly().url}")
        handle = part()
        print(f"view {part.__name__}: {handle.url}")
        # The shape comes back from the server: the same geometry, though a
        # flat face may mesh along other diagonals than a local build's.
        export_printable(name, handle.shape, project=project, print_orientation=orientation)
        return

    shape = build()
    export_printable(name, shape, project=project, print_orientation=orientation)
    if viewer_choice() == "yacv":
        _show_yacv(name, shape, context() if context else {})


def with_context(label: str, part: Shape, context: dict[str, Shape]) -> Compound:
    """`part` among labelled context shapes, as one assembly: the body of an
    assembly model. Labels name the nodes in the viewer's tree and in the
    references its Quick Edit hands to an agent."""
    children = [part]
    for child_label, shape in context.items():
        shape.label = child_label
        children.append(shape)
    return Compound(children=children, label=label)


def viewer_choice() -> str:
    """CAD_VIEWER, checked: `text-to-cad` (the default), `yacv` or `none`."""
    viewer = os.environ.get("CAD_VIEWER", "text-to-cad")
    if viewer not in ("text-to-cad", "yacv", "none"):
        raise ValueError(f"CAD_VIEWER={viewer!r}: expected text-to-cad, yacv or none")
    return viewer


def export_printable(
    name: str, part: Shape, *, project: str, print_orientation: Location | None = None
) -> None:
    """Write out/<project>/<name>.{step,3mf,stl} and print the part's size.

    The STEP keeps the part in its use position; the 3MF/STL are turned by
    `print_orientation`, centred and set on the bed (z = 0).
    """
    out = OUT_DIR / project
    out.mkdir(parents=True, exist_ok=True)

    export_step(part, out / f"{name}.step")

    printable = part.moved(print_orientation or Location())
    bb = printable.bounding_box()
    printable = printable.moved(Location((-bb.center().X, -bb.center().Y, -bb.min.Z)))

    mesher = Mesher()
    mesher.add_shape(printable, part_number=name)
    mesher.write(str(out / f"{name}.3mf"))
    export_stl(printable, out / f"{name}.stl")

    size = part.bounding_box().size
    print(
        f"{name}: {size.X:.2f} x {size.Y:.2f} x {size.Z:.2f} mm, "
        f"volume {part.volume / 1000:.2f} cm3 -> {out.relative_to(REPO_ROOT)}/"
    )


def _show_yacv(name: str, part: Shape, context: dict[str, Shape]) -> None:
    from yacv_server import show

    shapes = [part, *context.values()]
    names = [name, *context.keys()]
    show(*shapes, names=names)
    print("Viewer: http://localhost:32323 (keep the tab open; re-run to update)")
