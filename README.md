# maxcad

Personal CAD models for 3D printing, written as Python code with
[build123d](https://github.com/gumyr/build123d) and viewed in
[text-to-cad](https://github.com/earthtojake/text-to-cad)'s CAD Viewer (or
[Yet Another CAD Viewer](https://github.com/yeicor-3d/yet-another-cad-viewer)).

## Setup

Requires [mise](https://mise.jdx.dev). Python and all packages are pinned exactly (`requires-python` in `pyproject.toml`, `uv.lock`).

```sh
mise install    # installs the pinned uv
mise run setup  # installs Python 3.14 + dependencies into .venv
```

## Workflow

```sh
mise run view projects/curtain-rail/stopper.py       # show in browser + export
mise run build door-handles                          # export every part of a project
```

`view` hands the part, with its context geometry, to text-to-cad's local
server and prints the page's URL. Re-running the part updates the same page.
The server (`cad-server`) is a pinned dependency like the rest, in `.venv`;
`mise run setup` registers it, and a run starts it when it is not running
(`uv run cad stop` stops it). Everything text-to-cad keeps lives in `.cad/`, not in
your home directory (`mise.toml`).

In the viewer you can select, measure and annotate; its Quick Edit hands the
selection to a coding agent as references into the model.

Every part is written as text-to-cad models: its geometry stays a plain
build123d `build()` function, wrapped by `@model` functions that the server
builds itself (the printed part, and where there is context geometry an
assembly to look at, e.g. `stopper_in_rail`). A re-run rebuilds only what an
edit changed, the page follows each rebuild, and the viewer knows the script
behind every face. Each script ends with `present_model` (`src/cadkit/present.py`),
which prints the pages and writes the printable files.

`CAD_VIEWER=yacv mise run view ...` uses Yet Another CAD Viewer instead
(`http://localhost:32323`, keep the tab open). `CAD_VIEWER=none` only exports,
as `build` does. Usage stats and update checks of text-to-cad are off for
this repo (`mise.toml`).

Outputs go to `out/<project>/` (not committed):

- `<part>.step`: exact geometry in use position (open in FreeCAD to measure)
- `<part>.3mf` / `.stl`: mesh, already rotated into the intended print orientation

## Layout

```
src/cadkit/          shared helpers (export + viewer, geometry features)
projects/<name>/
  README.md          what the project is + print sheet
  params.py          every number, with ESTIMATE / PLACEHOLDER / FIT markers
  context.py         non-printed geometry for the viewer (rails, doors, screws)
  <part>.py          one printable part each
```
