# maxcad

Personal CAD models for 3D printing, written as Python code with
[build123d](https://github.com/gumyr/build123d) and viewed in
[Yet Another CAD Viewer](https://github.com/yeicor-3d/yet-another-cad-viewer).

## Setup

Requires [mise](https://mise.jdx.dev). Python and all packages are pinned (`.python-version`, `uv.lock`).

```sh
mise install    # installs the pinned uv
mise run setup  # installs Python 3.13 + dependencies into .venv
```

## Workflow

```sh
mise run view projects/curtain-rail/stopper.py       # show in browser + export
mise run build door-handles                          # export every part of a project
```

`view` prints `http://localhost:32323`. Open it, and keep the tab open: each
re-run of a part pushes the new version into the same tab.

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
