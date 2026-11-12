# CLAUDE.md

Personal CAD models for 3D printing: build123d scripts in `projects/<name>/`, built and shown by
text-to-cad (README has the layout and workflow).

## text-to-cad here differs from a standard install

The `cad` and `print3d` skills in `.claude/skills/` are text-to-cad's own, copied unmodified from
the release `uv.lock` pins. They assume a per-user install (`~/.local/bin/cad`, an install script,
uvx). This repo carries everything itself instead, and these rules win over the skills where they
disagree:

- **Never install text-to-cad**: no `install.sh`, `cad setup`, `uvx … cad-server`, plugin, or
  anything under `~/.local/bin`, `~/.local/state/cad` or `~/.cache/cad`. The library, server and
  MCP server (`cad`, `cad-server`, `cad-mcp`) are pinned in `pyproject.toml`; if the server is not
  registered, run `just setup`.
- **The `cad` command is `uv run cad …`** (`uv run cad status`, `uv run cad model snapshot <id>
  out.png`, …), in the flake's dev shell, which sets `CAD_STATE_DIR`, `CAD_CACHE_DIR`,
  `CAD_ENGINE_DIR` and `CAD_LAUNCHER_DIR` to `.cad/` and provides Python, uv and the libraries
  the wheels need. In a shell outside it (no direnv), prefix `nix develop --command`.
- **Build and show a part with `just view projects/<name>/<part>.py`.** It prints each
  model's page (`view <model>: <url>`) and writes the printable files to `out/<name>/`.
  `uv run cad run <script>` works too, as the skill's `cad run`.
- **The MCP server is `cad`** (`.mcp.json`): `cad_show`, `cad_inspect`, `cad_snapshot`,
  `cad_export`, against the repo's own server.
- **Telemetry and update checks stay off** (`flake.nix`, and the choice saved in `.cad/`).

## How a part script is written

- Plain build123d geometry in `build()` (numbers in `params.py`, preview-only geometry such as
  rails and doors in `context.py`).
- `@model` wrappers around it: the printed part, labelled with its name, and where there is
  context geometry an assembly from `cadkit.with_context` (`stopper_in_rail`).
- The script ends with `cadkit.present_model(...)`, which picks the path by `CAD_VIEWER`
  (`src/cadkit/present.py`). Unlike the skill's "runs write nothing", a run here writes
  `out/<project>/<part>.{step,3mf,stl}`, the 3MF/STL in print orientation.
- Where a part is meant to be configured, what may be chosen is declared, not left to editing
  `params.py`: a frozen `Options` dataclass in the project's `options.py` (`cadkit.options`:
  `number` with limits, `choice` on a `Literal`, `check` in `__post_init__`), `build(options)`,
  and a `VARIANTS` dict of the configurations that are built, each with its own `@model` and
  files. `projects/door-handles/` is the example. Only add an option that changes the printed
  part and builds across its whole range.
- No kernel objects at module level (a `Location`, `Color`, shape): numbers there, kernel objects
  inside functions, so a replayed run does not load the kernel.
- `just build <project>` builds without the server (`CAD_VIEWER=none`), as CI does.
- `just site` generates the static site into `site/` (`src/cadkit/site.py`, README "Site"). It
  shows what `present_model` exports and renders each project's `README.md` as its page: a part
  is on the site once its script runs, and the README's first paragraph and `Status: **...**`
  line are the project's card. Part names in backticks in the README set the order of the parts.

## Skills

`uv run scripts/sync_skills.py` copies the skills of the release `uv.lock` pins (`--check`
verifies them, in CI); Renovate runs it on a `cad` bump. Never edit the copies: say what differs
here in this file.
