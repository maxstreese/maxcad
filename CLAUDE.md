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
  registered, run `mise run setup`.
- **The `cad` command is `uv run cad …`** (`uv run cad status`, `uv run cad model snapshot <id>
  out.png`, …), from the repo, where mise sets `CAD_STATE_DIR`, `CAD_CACHE_DIR`,
  `CAD_ENGINE_DIR` and `CAD_LAUNCHER_DIR` to `.cad/`. In a shell without mise's hook, prefix
  `mise exec --`.
- **Build and show a part with `mise run view projects/<name>/<part>.py`.** It prints each
  model's page (`view <model>: <url>`) and writes the printable files to `out/<name>/`.
  `uv run cad run <script>` works too, as the skill's `cad run`.
- **The MCP server is `cad`** (`.mcp.json`): `cad_show`, `cad_inspect`, `cad_snapshot`,
  `cad_export`, against the repo's own server.
- **Telemetry and update checks stay off** (`mise.toml`, and the choice saved in `.cad/`).

## How a part script is written

- Plain build123d geometry in `build()` (numbers in `params.py`, preview-only geometry such as
  rails and doors in `context.py`).
- `@model` wrappers around it: the printed part, labelled with its name, and where there is
  context geometry an assembly from `cadkit.with_context` (`stopper_in_rail`).
- The script ends with `cadkit.present_model(...)`, which picks the path by `CAD_VIEWER`
  (`src/cadkit/present.py`). Unlike the skill's "runs write nothing", a run here writes
  `out/<project>/<part>.{step,3mf,stl}`, the 3MF/STL in print orientation.
- No kernel objects at module level (a `Location`, `Color`, shape): numbers there, kernel objects
  inside functions, so a replayed run does not load the kernel.
- `mise run build <project>` builds without the server (`CAD_VIEWER=none`), as CI does.

## Skills

`uv run scripts/sync_skills.py` copies the skills of the release `uv.lock` pins (`--check`
verifies them, in CI); Renovate runs it on a `cad` bump. Never edit the copies: say what differs
here in this file.
