{
  description = "maxcad – personal CAD models for 3D printing (build123d, text-to-cad)";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs =
    { nixpkgs, ... }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
      ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f nixpkgs.legacyPackages.${system});

      # The interpreter. Its exact version is the one flake.lock pins;
      # pyproject.toml asks only for 3.14.x, so a nixpkgs bump does not have
      # to wait for it. cadquery-ocp (OpenCascade, under build123d and cad)
      # has no wheels for 3.15 yet (cp311-cp314, 2026-11-08).
      python = pkgs: pkgs.python314;

      # <model-viewer>, the web component the site shows the parts' GLBs with
      # (`just site`). Its npm package, pinned here by version and hash and
      # copied into the site, so a page loads nothing from anyone else's
      # server. To update: the new version in both places of the url, the
      # hash from
      #   nix store prefetch-file --unpack --json <url>
      modelViewer =
        pkgs:
        pkgs.fetchzip {
          url = "https://registry.npmjs.org/@google/model-viewer/-/model-viewer-4.4.0.tgz";
          hash = "sha256-G5D9Obi9WpzzxLZYiHZnbdhAkYjo/Dfv9rZHcpx2SNA=";
        };

      tools =
        pkgs: with pkgs; [
          (python pkgs)
          # Installs the Python packages from uv.lock into .venv.
          uv
          just

          # Dependency updates and CI
          renovate
          actionlint
        ];

      # What the prebuilt wheels in .venv link against (cadquery-ocp,
      # numpy, pillow, ...), found with ldd over every .so in the venv
      # (2026-11-08). The shell provides them, so the repo needs nothing
      # from the system: no nix-ld, no FHS paths.
      libraries =
        pkgs: with pkgs; [
          stdenv.cc.cc.lib # libstdc++
          zlib
          expat
          libx11
          libGL
        ];
    in
    {
      devShells = forAllSystems (pkgs: {
        default = pkgs.mkShell {
          packages = tools pkgs;

          LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath (libraries pkgs);

          # uv uses the interpreter above and never downloads one of its own.
          UV_PYTHON = "${python pkgs}/bin/python3.14";
          UV_PYTHON_DOWNLOADS = "never";

          # text-to-cad (the `cad` library, `cad-server` and `cad-mcp`, all in
          # uv.lock): no usage stats, and no update checks for a release
          # uv.lock pins anyway. The background server reads its telemetry
          # choice from the state folder, where `just setup` saves it.
          CAD_TELEMETRY = "0";
          CAD_UPDATE_CHECK = "0";

          # The site's viewer script (src/cadkit/site.py copies it).
          MODEL_VIEWER_JS = "${modelViewer pkgs}/dist/model-viewer.min.js";

          # Everything else text-to-cad keeps stays in .cad/ (gitignored),
          # not in ~: the registration of the server in .venv, its saved
          # settings, the `cad` launcher, the document cache and the engine's
          # socket. Its defaults are ~/.local/state/cad, ~/.local/bin,
          # ~/.cache/cad and /run/user/<uid>. Anchored on the repository's
          # root, wherever in it the shell was entered.
          shellHook = ''
            root=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
            export CAD_STATE_DIR="$root/.cad/state"
            export CAD_LAUNCHER_DIR="$root/.cad/bin"
            export CAD_CACHE_DIR="$root/.cad/cache"
            export CAD_ENGINE_DIR="$root/.cad/engine"
            unset root
          '';
        };
      });
    };
}
