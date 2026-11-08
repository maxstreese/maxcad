# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Vendor text-to-cad's agent skills at the release uv.lock pins.

text-to-cad's Claude Code plugin would bring these skills, but it also runs
its MCP server through uvx, outside uv.lock (README, "text-to-cad"). So the
repo carries the pieces itself: cad-mcp in pyproject.toml, the server in
.mcp.json, and the skills under .claude/skills/, copied unmodified from the
git tag of the release `cad` is locked at. Where the repo differs from a
standard text-to-cad install, CLAUDE.md says so; the copies stay byte for
byte the release's, so syncing them never fights a local edit.

    uv run scripts/sync_skills.py          # copy the skills of uv.lock's release
    uv run scripts/sync_skills.py --check  # exit 1 unless they match it (CI)

`.claude/skills/text-to-cad.json` records the release and a hash of each
skill's files. --check needs no network.

Renovate runs the sync after a bump of `cad` (renovate.jsonc), so its PR
carries the matching skills.
"""

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO / ".claude" / "skills"
LOCK = SKILLS_DIR / "text-to-cad.json"
SOURCE = "earthtojake/text-to-cad"
# The skills this repo uses. The release also has engineering-drawing, pcb,
# robot-simulation and sendcutsend.
SKILLS = ["cad", "print3d"]
# Released together and speaking one contract; cad-server requires cad at its
# own release, cad-mcp declares nothing, so this is where a split shows.
PACKAGES = ["cad", "cad-server", "cad-mcp"]


def locked_release() -> str:
    """The release uv.lock pins, the same for every text-to-cad package."""
    lock = tomllib.loads((REPO / "uv.lock").read_text())
    versions = {p["name"]: p["version"] for p in lock["package"] if p["name"] in PACKAGES}
    missing = sorted(set(PACKAGES) - set(versions))
    if missing:
        sys.exit(f"uv.lock has no {', '.join(missing)}")
    if len(set(versions.values())) != 1:
        sys.exit(f"text-to-cad packages at different releases in uv.lock: {versions}")
    return versions["cad"]


def tree_hash(folder: Path) -> str:
    """sha256 over every file's relative path and bytes, in path order."""
    digest = hashlib.sha256()
    for path in sorted(p for p in folder.rglob("*") if p.is_file()):
        digest.update(path.relative_to(folder).as_posix().encode() + b"\0")
        digest.update(path.read_bytes() + b"\0")
    return digest.hexdigest()


def sync(release: str) -> None:
    # git, not urllib: uv's standalone Python finds no CA bundle on NixOS,
    # and git is there wherever this runs (here, CI, Renovate's container).
    # A shallow clone of the tag with only the skills checked out.
    with tempfile.TemporaryDirectory() as tmp:
        clone = Path(tmp) / "text-to-cad"
        git = ["git", "-c", "advice.detachedHead=false"]
        subprocess.run(
            [*git, "clone", "--quiet", "--depth", "1", "--filter=blob:none", "--sparse",
             "--branch", f"v{release}", f"https://github.com/{SOURCE}.git", str(clone)],
            check=True,
        )
        subprocess.run([*git, "-C", str(clone), "sparse-checkout", "set",
                        *(f"skills/{skill}" for skill in SKILLS)], check=True)
        hashes = {}
        for skill in SKILLS:
            source = clone / "skills" / skill
            if not source.is_dir():
                sys.exit(f"{SOURCE} v{release} has no skills/{skill}")
            target = SKILLS_DIR / skill
            shutil.rmtree(target, ignore_errors=True)
            shutil.copytree(source, target)
            hashes[skill] = tree_hash(target)
    LOCK.write_text(json.dumps({"source": SOURCE, "release": release, "skills": hashes}, indent=2) + "\n")
    print(f"skills {', '.join(SKILLS)} at {SOURCE} v{release}")


def check(release: str) -> None:
    if not LOCK.exists():
        sys.exit(f"{LOCK.relative_to(REPO)} is missing: run `uv run scripts/sync_skills.py`")
    lock = json.loads(LOCK.read_text())
    problems = []
    if lock.get("release") != release:
        problems.append(f"skills are from v{lock.get('release')}, uv.lock pins v{release}")
    if sorted(lock.get("skills", {})) != sorted(SKILLS):
        problems.append(f"skills recorded {sorted(lock.get('skills', {}))}, expected {sorted(SKILLS)}")
    for skill, recorded in lock.get("skills", {}).items():
        folder = SKILLS_DIR / skill
        if not folder.is_dir() or tree_hash(folder) != recorded:
            problems.append(f"{skill} differs from the copy of v{lock.get('release')}")
    if problems:
        sys.exit("\n".join(problems) + "\nrun `uv run scripts/sync_skills.py`")
    print(f"skills match {SOURCE} v{release}")


if __name__ == "__main__":
    release = locked_release()
    check(release) if "--check" in sys.argv[1:] else sync(release)
