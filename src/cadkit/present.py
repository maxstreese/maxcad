"""Show a part in a viewer and export it for printing.

Every part script writes its part as text-to-cad models: a plain build123d
`build()` function, a `@model` function wrapping it (the printed part), and
optionally a second `@model` that places the part among context geometry
(the rail, the door) for looking at. The script ends with `present_model`,
which

- exports the printable part to out/<project>/<name>.{step,3mf,stl}, with the
  3MF/STL already rotated into the intended print orientation,
- writes what the site shows of it beside them: <name>.glb (the part in its
  use position), <name>_in_context.glb (among its context geometry, where it
  has any) and <name>.json (size, files, options; src/cadkit/site.py reads
  it), and
- shows it in a viewer.

CAD_OUT_DIR moves all of that from out/ to another folder (`just site`).

CAD_VIEWER picks the viewer:

- `text-to-cad` (default): text-to-cad's server builds the models, rebuilds
  only what an edit changed, and prints each model's page; open pages follow
  every rebuild. The printable files are written from that same build.
- `yacv`: Yet Another CAD Viewer at http://localhost:32323, from a plain
  `build()` without the server.
- `none`: only export, from a plain `build()` (`just build` and
  CI do this, so neither needs a server).
"""

import copy
import json
import os
from collections.abc import Callable
from pathlib import Path
from typing import Any

from build123d import Color, Compound, Location, Mesher, Shape, export_gltf, export_step, export_stl

from cadkit.options import describe

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = Path(os.environ.get("CAD_OUT_DIR") or REPO_ROOT / "out")

# The printed part's colour in the GLB, where the script gave it none (RGB as
# numbers: no kernel object at module level).
PART_COLOR = (0.60, 0.69, 0.80)


def present_model(
    name: str,
    *,
    project: str,
    part: Callable[[], Any],
    build: Callable[[], Shape],
    assembly: Callable[[], Any] | None = None,
    context: Callable[[], dict[str, Shape]] | None = None,
    print_orientation: Location | None = None,
    options: Any | None = None,
    variant_of: str | None = None,
) -> None:
    """The `__main__` of a part script.

    `part` and `assembly` are the script's `@model` functions; `build` and
    `context` are the plain functions behind them, used without the server.
    `print_orientation` turns the 3MF/STL only; the STEP, the GLB and the
    viewers keep the part in its use position.

    For one configuration of a part with options (src/cadkit/options.py):
    `options` is its Options, and `variant_of` the name of the part all its
    configurations belong to, under which the site lists them together.
    """
    orientation = print_orientation or Location()
    about = {"options": options, "variant_of": variant_of}
    if viewer_choice() == "text-to-cad":
        # text-to-cad prints a model's page only for calls made in the
        # script's own __main__; these come from here, so print them.
        in_context = None
        if assembly is not None:
            shown = assembly()
            print(f"view {assembly.__name__}: {shown.url}")
            in_context = shown.shape
        handle = part()
        print(f"view {part.__name__}: {handle.url}")
        # The shape comes back from the server: the same geometry, though a
        # flat face may mesh along other diagonals than a local build's.
        export_printable(
            name, handle.shape, project=project, print_orientation=orientation, in_context=in_context, **about
        )
        return

    shape = build()
    shapes = context() if context else {}
    in_context = None
    if shapes:
        # A copy goes into the assembly: the part itself keeps no parent.
        placed = copy.copy(shape)
        placed.label = name
        in_context = with_context(f"{name}_in_context", placed, shapes)
    export_printable(
        name, shape, project=project, print_orientation=orientation, in_context=in_context, **about
    )
    if viewer_choice() == "yacv":
        _show_yacv(name, shape, shapes)


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
    name: str,
    part: Shape,
    *,
    project: str,
    print_orientation: Location | None = None,
    in_context: Shape | None = None,
    options: Any | None = None,
    variant_of: str | None = None,
) -> None:
    """Write out/<project>/<name>.{step,3mf,stl,glb,json} and print the part's size.

    The STEP and the GLB keep the part in its use position; the 3MF/STL are
    turned by `print_orientation`, centred and set on the bed (z = 0).
    `in_context`, the part among its context geometry, becomes
    <name>_in_context.glb. `options` and `variant_of` as in `present_model`.
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

    files = {"glb": f"{name}.glb", "3mf": f"{name}.3mf", "step": f"{name}.step"}
    _export_glb(copy.copy(part), out / files["glb"])
    if in_context is not None:
        files["in_context_glb"] = f"{name}_in_context.glb"
        _export_glb(in_context, out / files["in_context_glb"])

    size = part.bounding_box().size
    # Summed over the solids: a Compound the server hands back reports 0 for
    # its own volume when the solid in it is mirrored.
    volume = sum(solid.volume for solid in part.solids())
    about = {
        "name": name,
        "project": project,
        "variant_of": variant_of or name,
        "size_mm": [round(size.X, 2), round(size.Y, 2), round(size.Z, 2)],
        "volume_cm3": round(volume / 1000, 2),
        "files": files,
        "options": describe(options) if options is not None else None,
    }
    (out / f"{name}.json").write_text(json.dumps(about, indent=2) + "\n")

    shown = out.relative_to(REPO_ROOT) if out.is_relative_to(REPO_ROOT) else out
    print(
        f"{name}: {size.X:.2f} x {size.Y:.2f} x {size.Z:.2f} mm, "
        f"volume {volume / 1000:.2f} cm3 -> {shown}/"
    )


def _export_glb(shape: Shape, path: Path) -> None:
    """`shape` as a binary glTF, for the site: metres, y up, with the colours
    and labels its nodes carry. A part without a colour gets PART_COLOR."""
    for node in shape.children or [shape]:
        if node.color is None:
            node.color = Color(*PART_COLOR)
    if not export_gltf(shape, path, binary=True):
        raise RuntimeError(f"could not write {path}")


def _show_yacv(name: str, part: Shape, context: dict[str, Shape]) -> None:
    from yacv_server import show

    shapes = [part, *context.values()]
    names = [name, *context.keys()]
    show(*shapes, names=names)
    print("Viewer: http://localhost:32323 (keep the tab open; re-run to update)")
