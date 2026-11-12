# maxcad

Personal CAD models for 3D printing, written as Python code with
[build123d](https://github.com/gumyr/build123d) and viewed in
[text-to-cad](https://github.com/earthtojake/text-to-cad)'s CAD Viewer (or
[Yet Another CAD Viewer](https://github.com/yeicor-3d/yet-another-cad-viewer)).

## Setup

Requires [Nix](https://nixos.org) with flakes, and ideally
[direnv](https://direnv.net) (with nix-direnv), which enters the dev shell on
`cd`; without it, run `nix develop` first. The shell (`flake.nix`) brings
Python 3.14, uv, just and the libraries the wheels need, pinned by
`flake.lock`; the Python packages are pinned exactly in `pyproject.toml` and
`uv.lock`.

```sh
direnv allow    # once: enter the dev shell on cd (or: nix develop)
just setup      # installs the dependencies into .venv, registers text-to-cad's server
```

## Workflow

```sh
just view projects/curtain-rail/stopper.py       # show in browser + export
just build door-handles                          # export every part of a project
just                                             # list every recipe
```

`view` hands the part, with its context geometry, to text-to-cad's local
server and prints the page's URL. Re-running the part updates the same page.
The server (`cad-server`) is a pinned dependency like the rest, in `.venv`;
`just setup` registers it, and a run starts it when it is not running
(`uv run cad stop` stops it). Everything text-to-cad keeps lives in `.cad/`, not in
your home directory (`flake.nix`).

In the viewer you can select, measure and annotate; its Quick Edit hands the
selection to a coding agent as references into the model.

Every part is written as text-to-cad models: its geometry stays a plain
build123d `build()` function, wrapped by `@model` functions that the server
builds itself (the printed part, and where there is context geometry an
assembly to look at, e.g. `stopper_in_rail`). A re-run rebuilds only what an
edit changed, the page follows each rebuild, and the viewer knows the script
behind every face. Each script ends with `present_model` (`src/cadkit/present.py`),
which prints the pages and writes the printable files.

`CAD_VIEWER=yacv just view ...` uses Yet Another CAD Viewer instead
(`http://localhost:32323`, keep the tab open). `CAD_VIEWER=none` only exports,
as `build` does. Usage stats and update checks of text-to-cad are off for
this repo (`flake.nix`).

### With a coding agent

The repo carries what text-to-cad's Claude Code plugin would bring, without
installing anything per user: its MCP server (`cad-mcp`, pinned in
`pyproject.toml`, started by `.mcp.json` in the dev shell so it finds `.cad/`) and
its `cad` and `print3d` skills (copied into `.claude/skills/` from the release
`uv.lock` pins; `just skills` refreshes them, CI checks them, Renovate
syncs them on a `cad` bump). `CLAUDE.md` says where this repo differs from a
standard install. Claude Code asks once to approve the `cad` MCP server.

Outputs go to `out/<project>/` (not committed):

- `<part>.step`: exact geometry in use position (open in FreeCAD to measure)
- `<part>.3mf` / `.stl`: mesh, already rotated into the intended print orientation
- `<part>.glb`, `<part>_in_context.glb`, `<part>.json`: what the site shows
  of the part (below)

## Site

```sh
just site          # build every project and generate site/
just site-serve    # look at it: http://localhost:8000
```

A static site with a page per project: each part in a 3D viewer (alone or
among its context geometry), its variants and options where it has them, and
its 3MF and STEP to download; the text is the project's `README.md`. Pushing
to `main` publishes it to GitHub Pages (`.github/workflows/pages.yml`).

`src/cadkit/site.py` generates it as plain HTML from what the part scripts
export: the GLB to show and a small JSON saying what the part is. No
framework and no Node: the viewer is
[`<model-viewer>`](https://modelviewer.dev), pinned in `flake.nix` and copied
into the site, so a page loads nothing from another server. A new project or
part appears without anyone adding it.

## Layout

```
src/cadkit/          shared helpers (export + viewer, geometry features, options,
                     the site's generator and its stylesheet and script)
projects/<name>/
  README.md          what the project is + print sheet
  params.py          every number, with ESTIMATE / PLACEHOLDER / FIT markers
  options.py         where a part has them: the values meant to be chosen, with
                     their limits, and the variants that get built (door-handles)
  context.py         non-printed geometry for the viewer (rails, doors, screws)
  <part>.py          one printable part each
```
