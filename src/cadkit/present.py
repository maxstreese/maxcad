"""Show a part in a viewer and export it for printing.

Every part script ends with a call to `present`. It

- exports the printable part to out/<project>/<name>.{step,3mf,stl}, with the
  3MF/STL already rotated into the intended print orientation, and
- shows the part (in its use position) together with optional context
  geometry, e.g. the rail or the door, in a viewer.

CAD_VIEWER picks the viewer:

- `text-to-cad` (default): text-to-cad's CAD Viewer. The part is handed to
  its local server and the run prints the page's URL; re-running the script
  updates the same page.
- `yacv`: Yet Another CAD Viewer at http://localhost:32323.
- `none`: only export (the `mise run build` task does this).
"""

import os
from pathlib import Path

from build123d import Location, Mesher, Shape, export_step, export_stl

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "out"


def present(
    name: str,
    part: Shape,
    *,
    project: str,
    print_orientation: Location = Location(),
    context: dict[str, Shape] | None = None,
) -> None:
    """Export `part` and show it with its `context` in the viewer.

    `print_orientation` is applied to the 3MF/STL only; the STEP file and the
    viewer keep the part in its use position.
    """
    context = context or {}

    out = OUT_DIR / project
    out.mkdir(parents=True, exist_ok=True)

    export_step(part, out / f"{name}.step")

    printable = part.moved(print_orientation)
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

    viewer = os.environ.get("CAD_VIEWER", "text-to-cad")
    if viewer == "none":
        return
    if viewer == "yacv":
        _show_yacv(name, part, context)
    elif viewer == "text-to-cad":
        _show_text_to_cad(name, part, project, context)
    else:
        raise ValueError(f"CAD_VIEWER={viewer!r}: expected text-to-cad, yacv or none")


def _show_yacv(name: str, part: Shape, context: dict[str, Shape]) -> None:
    from yacv_server import show

    shapes = [part, *context.values()]
    names = [name, *context.keys()]
    show(*shapes, names=names)
    print("Viewer: http://localhost:32323 (keep the tab open; re-run to update)")


def _show_text_to_cad(
    name: str, part: Shape, project: str, context: dict[str, Shape]
) -> None:
    import cad
    from build123d import Compound

    # Labels name the nodes in the viewer's tree and in the references its
    # Quick Edit hands to an agent. moved() places the same geometry again,
    # so the caller's shapes keep their own labels.
    children = []
    for label, shape in {name: part, **context}.items():
        child = shape.moved(Location())
        child.label = label
        children.append(child)

    # The document's id comes from the calling file and the name. Every call
    # comes from this file, so the project goes into the name to keep parts
    # of different projects apart.
    doc = cad.model(
        Compound(children=children, label=name), name=f"{project}.{name}"
    )
    print(f"Viewer: {doc.url} (re-run to update)")
