"""Fonts vendored with the repo, so engraved text comes out the same on every machine.

Without a font_path, build123d's Text asks OpenCascade for "Arial", which falls
back to whatever sans font the host has (DejaVu Sans on NixOS, FreeSans on
Ubuntu), changing the letters and their width.

JetBrainsMono-Regular.ttf: JetBrains Mono 2.304, the upstream release
(github.com/JetBrains/JetBrainsMono), under the SIL Open Font License 1.1
(JetBrainsMono-OFL.txt, which has to stay next to it).
"""

from pathlib import Path


def _vendored(name: str) -> str:
    # Text falls back to a host font, silently, when font_path does not exist.
    path = Path(__file__).with_name(name)
    if not path.is_file():
        raise FileNotFoundError(f"vendored font missing: {path}")
    return str(path)  # a plain string, not a kernel object: safe at module level


MONO = _vendored("JetBrainsMono-Regular.ttf")
