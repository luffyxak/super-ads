"""Original fictional Quiet Hours campaign and explicitly labelled fixture handoffs."""

import base64
import subprocess
import sys
import tempfile
from pathlib import Path

from .contracts import ROOT
from .store import public

BRIEF = {
    "brand": "HUSH",
    "product": "Desk Mat",
    "audience": "People who share a room while working from home",
    "market": "English-speaking social audience",
    "objective": "Build curiosity for the fictional HUSH desk mat",
    "facts": "A cobalt illustrated felt desk mat with a warm ivory HU monogram",
    "proof": "Original product illustration. The reaction is fiction and carries no measured acoustic claim.",
    "cta": "See the desk mat",
    "rights": "Original artwork, motion, and synthetic desk foley. No identifiable people.",
    "measurement": "Hypothesis: direct accusation earns a stronger three-second hold. Compare first-three-second hold for the two hook variants with otherwise identical delivery.",
    "festival": "none",
    "footage": False,
    "brandAssets": "Cobalt mat, ivory HU monogram, coral citation ink",
    "assumptions": "Fictional campaign. No client, real product, price, sale terms, or performance observations.",
}
HOOKS = [
    {"id": "eviction", "title": "EVICT THE KEYS?", "variable": "opening accusation wording"},
    {"id": "security", "title": "WHO CALLED SECURITY?", "variable": "opening accusation wording"},
]
HANDOFFS = {
    "strategy": (
        "Quiet for shared desks. Make an oversized grievance feel familiar.",
        [
            "Audience: people sharing a room at work or at home.",
            "Enemy: the desk that becomes a drum.",
            "Proof: the illustrated mat is visible in the product beat. No measured acoustic claim.",
        ],
    ),
    "concept": (
        "Select Eviction Notice for a recognizable prop, simple escalation, and immediate reversal.",
        [
            "Eviction Notice: a citation for a noisy set of keys. Meme frame: ALLOWED.",
            "Silent Cinema: discard because reading successive title cards costs the reveal.",
            "Workplace Hearing: discard because a cast of witnesses crowds the product.",
        ],
    ),
    "script": (
        "The citation comes first. Keys are allowed after the illustrated mat arrives.",
        [
            "0.0s EVICT THE KEYS?",
            "2.4s One desk. Too much drama.",
            "4.8s Enter the HUSH desk mat.",
            "8.0s Case dismissed.",
            "12.0s See the desk mat",
        ],
    ),
    "visual": (
        "Overhead paper editorial. Keep cobalt product, coral ink, and ivory paper consistent.",
        [
            "Styleframe 1: coral citation and keyring.",
            "Styleframe 2: cobalt mat and legible ivory product label.",
            "Styleframe 3: approved stamp with the original key-drop motion.",
        ],
    ),
    "shots": (
        "Five overhead beats. Preserve the physical relationship between the keys and mat.",
        [
            "Static opening on the citation.",
            "Slide the clipboard into the scene.",
            "Hold the packshot in the product beat.",
            "Bring in the source clip for the stamp.",
            "Settle on the CTA.",
        ],
    ),
    "motion": (
        "Kinetic typography and restrained paper motion. Movement follows the imaginary paperwork.",
        [
            "Keep the first frame readable.",
            "Make the stamp the single visual reversal.",
            "Use a steady closing hold.",
        ],
    ),
    "edit": (
        "Hold the accusation for 2.4 seconds and leave three seconds for the closing invitation.",
        [
            "Design vertical first, then reframe square and landscape.",
            "Mix original desk percussion on its own track.",
            "Burn sound-off captions and export SRT.",
        ],
    ),
}
PICTURES = (
    (
        "citation",
        2400,
        "hook",
        "EVICT THE KEYS?",
        "The keys are on notice.",
        "Overhead citation with a key already in view.",
        "A sharp key tick.",
    ),
    (
        "notice",
        2400,
        "setup",
        "NOISE COMPLAINT",
        "One desk. Too much drama.",
        "Clipboard edges into view like a formal complaint.",
        "Dry ticks.",
    ),
    (
        "mat",
        3200,
        "twist",
        "THE HUSH DESK MAT",
        "Enter the HUSH desk mat.",
        "Hold the approved cobalt product artwork.",
        "Soft pulse.",
    ),
    (
        "stamp",
        4000,
        "payoff",
        "ALLOWED",
        "Case dismissed.",
        "Keys land before the approval stamp takes over.",
        "A pause, then a stamp.",
    ),
    (
        "invitation",
        3000,
        "cta",
        "See the desk mat",
        "See the desk mat",
        "Closing shot. Hold the single invitation.",
        "Foley resolves.",
    ),
)
STYLES = ("citation", "clipboard", "packshot", "stamp", "end")
ASSETS = {
    "packshot.png": "packshot",
    "planning-reference.png": "reference",
    "key-drop.mp4": "clip",
    "desk-score.wav": "music",
}


def load_demo(store, identifier="quiet-hours", with_assets=True):
    result = store.create(identifier, "15s-reel", BRIEF, demo=True)
    media = {}
    generator = ROOT / "examples" / "quiet-hours" / "make_assets.py"
    if with_assets and generator.is_file():
        with tempfile.TemporaryDirectory(prefix="super-ads-fixture-") as folder:
            try:
                subprocess.run(
                    [sys.executable, str(generator), folder], check=True, timeout=90, capture_output=True
                )
            except (OSError, subprocess.SubprocessError):
                # An editable fixture still opens before media prerequisites are installed.
                folder = None
            if folder:
                for filename, role in ASSETS.items():
                    path = Path(folder) / filename
                    if path.is_file():
                        result = store.change(
                            identifier,
                            result["revision"],
                            "import",
                            {
                                "name": filename,
                                "role": role,
                                "rights": "Original Quiet Hours demo asset, MIT.",
                                "source": "Local reproducible Quiet Hours fixture generator.",
                                "disclosure": "Original synthetic or illustrated demo material.",
                                "consent": "",
                                "data": base64.b64encode(path.read_bytes()).decode(),
                            },
                        )
                        media[role] = result["assets"][-1]["id"]
    shots = [
        {
            "id": shot_id,
            "durationMs": duration,
            "beat": beat,
            "title": title,
            "caption": caption,
            "action": action,
            "audio": sound,
            "style": style,
            "motion": {"notice": "float", "mat": "push"}.get(shot_id, "still"),
            "asset": media.get("packshot", "")
            if shot_id in {"mat", "invitation"}
            else media.get("clip", "")
            if shot_id == "stamp"
            else "",
            "reference": media.get("reference", "") if shot_id == "stamp" else "",
            "evidence": "Fictional comic scene, no quantitative claim.",
        }
        for (shot_id, duration, beat, title, caption, action, sound), style in zip(
            PICTURES, STYLES, strict=True
        )
    ]
    tracks = (
        [
            {
                "asset": media["music"],
                "atMs": 0,
                "durationMs": 15000,
                "gain": 0.8,
                "fadeInMs": 30,
                "fadeOutMs": 300,
            }
        ]
        if "music" in media
        else []
    )
    result = store.change(
        identifier,
        result["revision"],
        "storyboard",
        {"shots": shots, "hooks": HOOKS, "selectedHook": "eviction", "tracks": tracks},
    )
    return fixture_handoffs(store, identifier, result["revision"])


def fixture_handoffs(store, identifier, revision):
    from .contracts import require

    with store.connection(write=True) as db:
        state = store._load(db, identifier)
        require(state["demo"], "Fixture handoffs are available only on fictional demo projects.")
        require(revision == state["revision"], "Revision changed. Reload and retry.")
        require(
            not state["attempt"] or state["attempt"]["status"] not in {"running", "cancelling"},
            "A project operation is already running.",
        )
        while (stage := store._next(state)) and stage["id"] in HANDOFFS:
            summary, items = HANDOFFS[stage["id"]]
            store._stage(state, {"summary": summary, "items": items}, "quiet-hours-fixture")
            store._commit(db, state)
        return public(state)
