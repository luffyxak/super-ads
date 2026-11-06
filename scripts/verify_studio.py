"""Run the keyless repository release suite."""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def call(*args):
    print("+", *args, flush=True)
    subprocess.run(args, cwd=ROOT, check=True)


def version(command, arguments, regex, minimum):
    path = shutil.which(command)
    if not path:
        raise RuntimeError(f"Install {command} before verification.")
    output = subprocess.check_output([path, *arguments], text=True).splitlines()[0]
    match = re.search(regex, output)
    if not match or int(match.group(1)) < minimum:
        raise RuntimeError(f"{command} must be version {minimum} or newer.")
    print(output, flush=True)


def doctor(core=False, ci=False):
    if sys.version_info < (3, 11):
        raise RuntimeError("Python 3.11 or newer is required.")
    print(sys.version.splitlines()[0], flush=True)
    version("node", ["--version"], r"v(\d+)", 22)
    if not core:
        for name in ("ffmpeg", "ffprobe"):
            version(name, ["-version"], r"version (\d+)", 6 if ci else 7)
        if not (ROOT / "node_modules/hyperframes/bin/hyperframes.mjs").is_file():
            raise RuntimeError("Run npm ci and npx playwright install chromium.")
        call("node", "node_modules/hyperframes/bin/hyperframes.mjs", "--version")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doctor", action="store_true")
    parser.add_argument("--core", action="store_true", help="Skip real Chromium integration")
    parser.add_argument(
        "--ci", action="store_true", help="Allow the Ubuntu 24.04 system FFmpeg for smoke checks"
    )
    args = parser.parse_args()
    doctor(args.core, args.ci)
    if args.doctor:
        return
    call(sys.executable, "scripts/validate_repo.py", "--strict")
    call("ruff", "check", "studio", "tests", "examples/quiet-hours", "evals", "scripts/verify_studio.py")
    call(
        "ruff",
        "format",
        "--check",
        "studio",
        "tests",
        "examples/quiet-hours",
        "evals",
        "scripts/verify_studio.py",
    )
    call(sys.executable, "-m", "compileall", "-q", "studio", "scripts", "examples/quiet-hours", "evals")
    call("node", "--check", "studio/web/app.js")
    call("node", "--check", "tests/browser.mjs")
    call(sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v")
    call(sys.executable, "-m", "evals.run")
    if not args.core:
        call("node", "tests/browser.mjs")
    print("Super Ads Studio verification passed.", flush=True)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, subprocess.CalledProcessError) as error:
        sys.exit(str(error))
