# Everything runs inside the flake's dev shell (direnv enters it on cd, or
# `nix develop`), which provides Python, uv and the libraries the wheels need,
# and points text-to-cad at .cad/.

# List recipes
default:
    @just --list

# Install the Python packages from uv.lock into .venv and register text-to-cad's server in .cad/
setup:
    uv sync
    # The background server goes by the choice saved in the state folder, not
    # by CAD_TELEMETRY, and a fresh state folder defaults to sending.
    uv run cad telemetry off
    # The library only ever starts a registered server; this registers the one
    # in .venv (and writes .cad/bin/cad). The first `view` starts it.
    uv run cad doctor --no-server -y

# Build one part, show it in text-to-cad's CAD Viewer (CAD_VIEWER=yacv for Yet Another CAD Viewer) and export it
view part:
    # yacv only: wait up to 2 min for a browser tab
    YACV_GRACEFUL_SECS_CONNECT=120 uv run python {{part}}

# Export every part of a project (STEP, 3MF, STL) to out/<project>/ without a viewer or server
build project:
    #!/usr/bin/env bash
    set -euo pipefail
    for f in projects/{{project}}/*.py; do
        case "$(basename "$f")" in params.py|context.py|options.py) ;; *) CAD_VIEWER=none uv run python "$f";; esac
    done

# Build every project and generate the static site into site/ (what GitHub Pages serves)
site:
    #!/usr/bin/env bash
    set -euo pipefail
    # The exports go to a folder of their own, not out/: the site publishes
    # exactly what this build wrote, never a file left over from an earlier one.
    exports=$(mktemp -d)
    trap 'rm -rf "$exports"' EXIT
    CAD_OUT_DIR="$exports" just build-all
    uv run python -m cadkit.site "$exports" site

# Serve site/ at http://localhost:8000 (run `just site` first)
site-serve:
    python -m http.server --directory site 8000

# Copy text-to-cad's agent skills of the release uv.lock pins into .claude/skills/
skills:
    uv run scripts/sync_skills.py

# Validate the Renovate configs and the workflows
lint:
    renovate-config-validator --strict renovate.jsonc
    renovate-config-validator --strict .github/renovate-global.jsonc
    actionlint

# Export every project, so a new one is covered without anyone adding it
build-all:
    #!/usr/bin/env bash
    set -euo pipefail
    for dir in projects/*/; do just build "$(basename "$dir")"; done

# What CI runs: lint, the locked install, the vendored skills, every project built and the site made of it
ci: lint
    uv sync --locked
    uv run scripts/sync_skills.py --check
    just site
