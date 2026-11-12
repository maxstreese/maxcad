"""The static site: every project on a page, its parts shown in 3D.

    python -m cadkit.site <exports> <site>

`<exports>` is a folder the part scripts exported into (CAD_OUT_DIR, as
`just site` sets it): per part a GLB to show, 3MF and STEP to download and a
<name>.json saying what it is (src/cadkit/present.py writes them). Only what
those JSON files name is published. The text of a project's page is its
README.md.

Out comes plain HTML: an index with one card per project, and a page per
project with a viewer per part (the part alone or among its context
geometry), its variants and options where it has them, and the downloads.
The viewer is <model-viewer>, copied in from MODEL_VIEWER_JS (the flake pins
it), so the pages load nothing from another server. Every URL is relative:
the site works under any path.
"""

import html
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any

from markdown_it import MarkdownIt

REPO_ROOT = Path(__file__).resolve().parents[2]
ASSETS = Path(__file__).parent / "site_assets"
REPO_URL = "https://github.com/maxstreese/maxcad"
SITE_TITLE = "maxcad"
SITE_INTRO = (
    "Personal CAD models for 3D printing, written as Python code. Every part here is built "
    "from its source on each change, with a 3MF to print and a STEP to measure or modify."
)
DOWNLOADS = {"3mf": ("3MF", "to print"), "step": ("STEP", "to modify")}


def main(exports: Path, site: Path) -> None:
    viewer = os.environ.get("MODEL_VIEWER_JS")
    if not viewer or not Path(viewer).is_file():
        raise SystemExit("MODEL_VIEWER_JS does not point at model-viewer's script: run in the flake's dev shell")
    projects = load(exports)
    if not projects:
        raise SystemExit(f"no parts in {exports}: build the projects with CAD_OUT_DIR set to it first")

    if site.exists():
        shutil.rmtree(site)
    site.mkdir(parents=True)
    shutil.copy(viewer, site / "model-viewer.min.js")
    for asset in ASSETS.iterdir():
        shutil.copy(asset, site / asset.name)

    cards = []
    for name, parts in projects.items():
        readme = Readme(REPO_ROOT / "projects" / name / "README.md")
        parts = in_readme_order(parts, readme.text)
        (site / name).mkdir()
        for variants in parts.values():
            for variant in variants:
                for file in published(variant).values():
                    shutil.copy(exports / name / file, site / name / file)
        (site / name / "index.html").write_text(project_page(name, readme, parts, exports / name))
        cards.append(card(name, readme, parts))
    (site / "index.html").write_text(index_page(cards))
    print(f"site: {len(projects)} projects, {sum(len(p) for p in projects.values())} parts -> {site}/")


# --- What was exported --------------------------------------------------------


def load(exports: Path) -> dict[str, dict[str, list[dict[str, Any]]]]:
    """{project: {part: [its variants, the one named like the part first]}}."""
    projects: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for file in sorted(exports.glob("*/*.json")):
        about = json.loads(file.read_text())
        projects.setdefault(about["project"], {}).setdefault(about["variant_of"], []).append(about)
    for parts in projects.values():
        for part, variants in parts.items():
            variants.sort(key=lambda v: (v["name"] != part, v["name"]))
    return projects


def in_readme_order(parts: dict[str, list], readme: str) -> dict[str, list]:
    """The parts in the order the README first names them (as `name`), the
    rest after them by name."""

    def position(part: str) -> tuple[int, str]:
        found = readme.find(f"`{part}`")
        return (found if found >= 0 else len(readme), part)

    return {part: parts[part] for part in sorted(parts, key=position)}


def published(variant: dict[str, Any]) -> dict[str, str]:
    """The files of a variant that go onto the site, by kind."""
    kinds = ("glb", "in_context_glb", *DOWNLOADS)
    return {kind: variant["files"][kind] for kind in kinds if kind in variant["files"]}


# --- README -------------------------------------------------------------------


class Readme:
    """A project's README.md: its title (the first heading), its summary (the
    first paragraph, as plain text), its status (the bold words after
    "Status:", if any) and the rest as HTML."""

    def __init__(self, path: Path) -> None:
        self.text = path.read_text()
        md = MarkdownIt("commonmark").enable("table")
        tokens = md.parse(self.text)
        self.title = path.parent.name
        if tokens and tokens[0].type == "heading_open" and tokens[0].tag == "h1":
            self.title = _plain(tokens[1])
            tokens = tokens[3:]
        first = next((t for t in tokens if t.type == "inline"), None)
        self.summary = _plain(first) if first is not None and tokens[0].type == "paragraph_open" else ""
        status = re.search(r"^Status:\s*\*\*(.+?)\*\*", self.text, re.MULTILINE)
        self.status = status.group(1) if status else ""
        body = md.renderer.render(tokens, md.options, {})
        # A wide table scrolls inside its own box, not the page.
        self.html = body.replace("<table>", '<div class="scroll"><table>').replace("</table>", "</table></div>")


def _plain(inline: Any) -> str:
    """An inline token's text, without its markup."""
    pieces = []
    for child in inline.children or []:
        if child.type in ("text", "code_inline"):
            pieces.append(child.content)
        elif child.type in ("softbreak", "hardbreak"):
            pieces.append(" ")
    return "".join(pieces)


# --- Pages --------------------------------------------------------------------


def page(title: str, body: str, root: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<link rel="stylesheet" href="{root}style.css">
<script type="module" src="{root}model-viewer.min.js"></script>
</head>
<body>
<div class="wrap">
{body}
<footer>Built from the code at <a href="{REPO_URL}">{e(REPO_URL.removeprefix("https://"))}</a>.</footer>
</div>
<script type="module" src="{root}site.js"></script>
</body>
</html>
"""


def index_page(cards: list[str]) -> str:
    body = f"""<header class="top">
<h1>{e(SITE_TITLE)}</h1>
<p>{e(SITE_INTRO)}</p>
</header>
<main class="cards">
{"".join(cards)}</main>"""
    return page(SITE_TITLE, body, "")


def card(project: str, readme: Readme, parts: dict[str, list]) -> str:
    first = next(iter(parts.values()))[0]
    count = f"{len(parts)} part{'s' if len(parts) != 1 else ''}"
    status = f" · {e(readme.status)}" if readme.status else ""
    return f"""<article class="card">
{viewer(f"{project}/{first['files']['glb']}", f"3D model of {first['name']}", controls=False)}
<h2><a href="{e(project)}/">{e(readme.title)}</a></h2>
<p class="summary">{e(readme.summary)}</p>
<p class="meta">{count}{status}</p>
</article>
"""


def project_page(project: str, readme: Readme, parts: dict[str, list], files: Path) -> str:
    status = f'<span class="badge">{e(readme.status)}</span>' if readme.status else ""
    body = f"""<header class="top">
<a class="back" href="../">&larr; All projects</a>
<h1>{e(readme.title)}{status}</h1>
</header>
<main>
<section class="parts">
{"".join(part_card(part, variants, files) for part, variants in parts.items())}</section>
<section class="readme">
{readme.html}</section>
<p><a href="{REPO_URL}/tree/main/projects/{e(project)}">Source of this project</a></p>
</main>"""
    return page(f"{readme.title} · {SITE_TITLE}", body, "../")


def part_card(part: str, variants: list[dict[str, Any]], files: Path) -> str:
    """One part: its viewer, the switches, its facts and downloads. The first
    variant is written into the markup; site.js swaps in the others from the
    JSON at the end."""
    shown = [for_page(v, files) for v in variants]
    first = shown[0]

    controls = []
    if first["context"]:
        controls.append(
            '<div class="seg" role="group" aria-label="What to show">'
            '<button type="button" data-view="part" aria-pressed="true">Part</button>'
            '<button type="button" data-view="context" aria-pressed="false">In context</button></div>'
        )
    if len(shown) > 1:
        choices = "".join(f"<option>{e(v['name'])}</option>" for v in shown)
        controls.append(f"<label>Variant <select>{choices}</select></label>")
    controls_html = f'<div class="controls">{"".join(controls)}</div>\n' if controls else ""

    downloads = "".join(
        f'<a href="{e(first["files"][kind]["href"])}" download data-kind="{kind}">{label} '
        f'<span>{note}</span> <small>{first["files"][kind]["size"]}</small></a>'
        for kind, (label, note) in DOWNLOADS.items()
    )
    # "</" must not end the script element early.
    data = json.dumps(shown).replace("</", "<\\/")
    return f"""<article class="part" id="{e(part)}">
<h2><code>{e(part)}</code></h2>
{viewer(first["glb"], f"3D model of {first['name']}", controls=True)}
{controls_html}<p class="facts"><span data-f="size">{first["size"]}</span> · <span data-f="volume">{first["volume"]}</span></p>
<p class="downloads">{downloads}</p>
{options_table(variants[0]["options"], first["options"])}<script type="application/json">{data}</script>
</article>
"""


def for_page(variant: dict[str, Any], files: Path) -> dict[str, Any]:
    """A variant as site.js needs it: every text already as it is shown."""
    x, y, z = variant["size_mm"]
    return {
        "name": variant["name"],
        "glb": variant["files"]["glb"],
        "context": variant["files"].get("in_context_glb"),
        "size": f"{number(x)} × {number(y)} × {number(z)} mm",
        "volume": f"{number(variant['volume_cm3'])} cm³",
        "files": {
            kind: {"href": variant["files"][kind], "size": file_size(files / variant["files"][kind])}
            for kind in DOWNLOADS
        },
        "options": {o["name"]: option_value(o) for o in variant["options"] or []},
    }


def options_table(options: list[dict[str, Any]] | None, values: dict[str, str]) -> str:
    if not options:
        return ""
    rows = []
    for o in options:
        if "choices" in o:
            limits = ", ".join(e(str(c)) for c in o["choices"])
        else:
            limits = f"{number(o['low'])} to {number(o['high'])} {e(o['unit'])}"
        rows.append(
            f'<tr><td><code>{e(o["name"])}</code><div class="doc">{e(o["doc"])}</div></td>'
            f'<td data-opt="{e(o["name"])}">{e(values[o["name"]])}</td><td>{limits}</td></tr>'
        )
    return f"""<div class="options">
<h3>Options</h3>
<div class="scroll"><table>
<thead><tr><th>Option</th><th>This variant</th><th>Can be</th></tr></thead>
<tbody>{"".join(rows)}</tbody>
</table></div>
</div>
"""


def viewer(src: str, alt: str, *, controls: bool) -> str:
    """A <model-viewer>. The GLB is y up with the part's z as up, so the
    camera looks from the front right, slightly from above."""
    interactive = ' camera-controls touch-action="pan-y"' if controls else ' loading="lazy"'
    return (
        f'<model-viewer src="{e(src)}" alt="{e(alt)}"{interactive} interaction-prompt="none" '
        'camera-orbit="35deg 62deg auto" environment-image="neutral" shadow-intensity="0.6"></model-viewer>'
    )


# --- Formatting ---------------------------------------------------------------


def e(text: str) -> str:
    return html.escape(text, quote=True)


def number(value: float) -> str:
    """At most one decimal, none when it is zero: 96, 67, 31.5."""
    return f"{value:.1f}".removesuffix(".0")


def option_value(option: dict[str, Any]) -> str:
    if "choices" in option:
        return str(option["value"])
    return f"{number(option['value'])} {option['unit']}"


def file_size(path: Path) -> str:
    size = path.stat().st_size
    return f"{size / 1024:.0f} KB" if size < 1024 * 1024 else f"{size / 1024 / 1024:.1f} MB"


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    main(Path(sys.argv[1]), Path(sys.argv[2]))
