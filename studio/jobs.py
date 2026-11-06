"""Adapter between durable attempts and trusted local media rendering."""

from shutil import rmtree

from .contracts import RATIOS, WORKFLOWS, ContractError, require
from .media_import import sha_file
from .render import RenderError, render_campaign, render_hook
from .store import picture_revision


def render_job(store, state, hook=None):
    project, attempt = state["id"], state["attempt"]["id"]
    workspace = None

    def cancelled():
        return store.get(project, raw=True)["attempt"]["status"] == "cancelling"

    try:
        workspace = store.path(project, "renders", attempt)
        destination = workspace / "delivery"
        assets = store.path(project, "assets")
        cache = store.path(project, "cache")
        workspace.mkdir(parents=True, exist_ok=False)

        if hook:
            require(any(item["id"] == hook for item in state["hooks"]), "Unknown hook.")
            result = render_hook(state, assets, destination, cache, hook, cancelled=cancelled)
            kind = "hook"
        else:
            result = render_campaign(state, assets, destination, cache, cancelled=cancelled)
            files = result["files"]
            require(
                result["verified"] and all(f"master-{ratio}.mp4" in files for ratio in RATIOS),
                "Every required ratio must pass media verification.",
            )
            for cut in list(WORKFLOWS[state["workflow"]][1])[1:]:
                extra = {**state, "shots": state["cuts"][cut], "hooks": [], "selectedHook": "", "tracks": []}
                secondary = destination / cut
                cut_result = render_campaign(extra, assets, secondary, cache, cancelled=cancelled)
                require(cut_result["verified"], "A secondary cut failed media verification.")
                for filename in cut_result["files"]:
                    name = f"{cut}-{filename}"
                    (secondary / filename).replace(destination / name)
                    files.append(name)
                rmtree(secondary)
            kind = "render"
        record = {
            "files": result["files"],
            "verified": result.get("verified", True),
            "stats": result.get("stats", {}),
            "input": picture_revision(state),
            "folder": f"renders/{attempt}/delivery",
            "hashes": {name: sha_file(destination / name) for name in result["files"]},
        }
        if hook:
            record["hook"] = hook
        finished = store.finish(project, attempt, "succeeded", **{kind: record})
        if finished["attempt"]["status"] == "cancelled":
            rmtree(workspace, ignore_errors=True)
        return finished
    except Exception as exc:
        if workspace is not None:
            rmtree(workspace, ignore_errors=True)
        message = (
            str(exc)
            if isinstance(exc, (ContractError, RenderError))
            else f"Render failed ({type(exc).__name__}). Check local renderer prerequisites and logs."
        )
        return store.finish(project, attempt, "failed", message=message)
