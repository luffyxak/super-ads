"""Command line entry point for Super Ads Studio."""

import argparse
import json
import shutil
import sys
from pathlib import Path

from .contracts import ROOT, WORKFLOWS, ContractError, require
from .demo import fixture_handoffs, load_demo
from .jobs import render_job
from .provider import run_provider
from .server import serve
from .store import Store, public


def parser():
    cli = argparse.ArgumentParser(prog="python3 -m studio", description="Local-first Super Ads Studio")
    cli.add_argument("--data", type=Path, default=ROOT / ".studio", help="Local project database and assets")
    commands = cli.add_subparsers(dest="command", required=True)
    command = commands.add_parser("serve")
    command.add_argument("--port", type=int, default=8765)
    command = commands.add_parser("demo")
    command.add_argument("--id", default="quiet-hours")
    command.add_argument("--no-assets", action="store_true")
    command = commands.add_parser("create")
    command.add_argument("id")
    command.add_argument("workflow", choices=WORKFLOWS)
    command.add_argument("brief", type=Path, help="JSON brief")
    for name in (
        "show",
        "history",
        "fixture",
        "render",
        "hook",
        "report",
        "delivery",
        "act",
        "agent",
        "materialize",
    ):
        command = commands.add_parser(name)
        command.add_argument("id")
        if name == "hook":
            command.add_argument("hook")
        if name == "act":
            command.add_argument("action")
            command.add_argument("payload", type=Path, help="JSON action data")
        if name == "agent":
            command.add_argument("--model", default="gpt-4.1-mini")
            command.add_argument("--allow-provider", action="store_true")
        if name == "materialize":
            command.add_argument("--output", type=Path, default=ROOT / "outputs")
    return cli


def read_json(path):
    require(path.is_file() and path.stat().st_size <= 23 * 1024 * 1024, "Provide a bounded JSON file.")
    return json.loads(path.read_text(encoding="utf-8"))


def run(args):
    store = Store(args.data)
    action = args.command
    if action == "serve":
        return serve(store, args.port)
    if action == "demo":
        return load_demo(store, args.id, with_assets=not args.no_assets)
    if action == "create":
        return store.create(args.id, args.workflow, read_json(args.brief))
    if action == "history":
        return store.history(args.id)
    state = store.get(args.id, raw=True)
    revision = state["revision"]
    if action == "show":
        return public(state)
    if action == "fixture":
        return fixture_handoffs(store, args.id, revision)
    if action in ("render", "hook"):
        if action == "hook":
            require(any(h["id"] == args.hook for h in state["hooks"]), "Select a valid hook variant.")
        return render_job(store, store.reserve(args.id, revision, action), getattr(args, "hook", None))
    if action in ("report", "delivery"):
        return store.build_files(args.id, revision, release=action == "delivery")
    if action == "act":
        return store.change(args.id, revision, args.action, read_json(args.payload))
    if action == "agent":
        return run_provider(store, args.id, revision, args.model, args.allow_provider)
    if action == "materialize":
        destination = args.output / args.id
        require(
            not destination.exists() and not destination.is_symlink(), "Choose an unused output directory."
        )
        names = set()
        for info in [state["report"], state["render"], state["release"], *state["hookPreviews"].values()]:
            if info:
                names.update(info.get("files", [info.get("file")]))
        require(names, "Generate a report or render before copying deliverables.")
        source = {name: store.file_path(state, name) for name in names}
        destination.mkdir(parents=True)
        for name, file in source.items():
            shutil.copyfile(file, destination / name)
        return {"directory": str(destination), "files": sorted(names)}
    raise ContractError("Unknown command.")


def main():
    try:
        result = run(parser().parse_args())
        if result is not None:
            print(json.dumps(result, ensure_ascii=False, indent=2))
            if (
                isinstance(result, dict)
                and result.get("attempt")
                and result["attempt"]["status"]
                in {"failed", "ambiguous", "interrupted", "cancelled", "rate-limited"}
            ):
                return 1
    except (ContractError, OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
