"""Executable contracts for the six authored workflows."""

import hashlib
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RATIOS = {"9x16": (1080, 1920), "1x1": (1080, 1080), "16x9": (1920, 1080)}
BRIEF_FIELDS = (
    "brand",
    "product",
    "audience",
    "market",
    "objective",
    "facts",
    "claim",
    "proof",
    "offer",
    "offerEnd",
    "cta",
    "rights",
    "measurement",
    "festival",
    "brandAssets",
    "assumptions",
    "launchPlan",
    "consent",
    "disclosure",
)
ROLES = {
    "strategy": ("strategist", "ad-strategy", "positioning"),
    "concept": ("creative-director", "ad-creative-director", "concept-board"),
    "script": ("copywriter", "ad-copywriter-gen-z", "timed-script"),
    "visual": ("visual-designer", "ad-visual-designer", "look-sheet"),
    "shots": ("video-director", "ad-video-director", "shot-list"),
    "motion": ("animator", "ad-animation-motion", "motion-plan"),
    "capture": ("creator", None, "creator-footage"),
    "edit": ("editor", "ad-social-formats", "edit-plan"),
    "qa": ("qa-brand-safety", "ad-brand-safety", "qa-checklist"),
    "performance": ("operator", "ad-performance-analyst", "observed-analysis"),
}
STANDARD = ("strategy", "concept", "script", "visual", "shots", "motion", "edit", "qa")
WORKFLOWS = {
    "15s-reel": (STANDARD, {"reel": 15}),
    "30s-tvc": (STANDARD, {"hero": 30}),
    "diwali-campaign": (STANDARD, {"hero": 30, "reel-a": 15, "reel-b": 15}),
    "product-launch": (STANDARD, {"reveal": 15, "teaser": 6}),
    "ugc-creator": (
        ("strategy", "concept", "script", "capture", "edit", "qa"),
        {f"creator-{n}": 15 for n in range(1, 6)},
    ),
    "super-bowl-style": (STANDARD, {"hero": 30, "cutdown": 15, "teaser": 6}),
}
ASSET_ROLES = {
    "reference",
    "packshot",
    "background",
    "cutout",
    "clip",
    "voice",
    "music",
    "foley",
    "logo",
}
SCORES = ("hook", "clarity", "pacing", "craft", "brandFit", "rewatchability")
BEATS = {"hook", "setup", "twist", "payoff", "cta"}
STYLES = {"citation", "clipboard", "packshot", "stamp", "end"}
MOTIONS = {"still", "push", "float"}


class ContractError(ValueError):
    """An actionable error safe to show to the local operator."""


def require(condition, message):
    if not condition:
        raise ContractError(message)


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def project_id(value):
    require(
        isinstance(value, str) and re.fullmatch(r"[a-z0-9][a-z0-9-]{0,62}", value),
        "Use a lowercase project ID with letters, numbers and hyphens (1–63 characters).",
    )
    return value


def safe_name(value):
    require(
        isinstance(value, str)
        and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,119}", value)
        and ".." not in value
        and not value.endswith("."),
        "Use a safe plain filename.",
    )
    return value


def string(value, label, limit=2500, required=False):
    require(
        isinstance(value, str)
        and len(value) <= limit
        and not any(ord(c) < 32 and c not in "\n\t" for c in value)
        and not any(0xD800 <= ord(c) <= 0xDFFF for c in value),
        f"{label} must be text up to {limit} characters.",
    )
    value = value.strip()
    require(value or not required, f"{label} is required.")
    return value


def integer(value, label, minimum, maximum):
    require(type(value) is int and minimum <= value <= maximum, f"{label} must be {minimum}–{maximum}.")
    return value


def fields(value, allowed, label):
    require(isinstance(value, dict) and set(value) <= set(allowed), f"{label} contains unsupported fields.")
    return value


def list_of(value, limit, label):
    require(isinstance(value, list) and len(value) <= limit, f"{label} accepts up to {limit} entries.")
    return value


def brief_data(value):
    fields(value, (*BRIEF_FIELDS, "footage", "riskFlags"), "Brief")
    footage = value.get("footage", False)
    require(type(footage) is bool, "Footage must be true or false.")
    flags = list_of(value.get("riskFlags", []), 8, "Risk flags")
    require(
        all(
            isinstance(flag, str)
            and flag
            in {
                "real-likeness",
                "endorsement",
                "face-swap",
                "review-gating",
                "dark-pattern",
                "misleading-claim",
            }
            for flag in flags
        ),
        "Unknown risk flag.",
    )
    return {
        **{key: string(value.get(key, ""), key) for key in BRIEF_FIELDS},
        "footage": footage,
        "riskFlags": sorted(set(flags)),
    }


def stage_plan(workflow, brief, metrics):
    require(isinstance(workflow, str) and workflow in WORKFLOWS, "Choose one of the six workflows.")
    order = list(WORKFLOWS[workflow][0])
    if metrics:
        order.append("performance")
    result = []
    for stage in order:
        role, skill, artifact = ROLES[stage]
        skills = [skill] if skill else []
        festival = brief.get("festival", "").strip().lower()
        if stage == "strategy" and (workflow == "diwali-campaign" or festival not in ("", "none")):
            skills.append("ad-diwali-festive")
        if stage == "motion" and brief.get("footage"):
            skills.append("ad-realistic-video")
        result.append({"id": stage, "role": role, "skills": skills, "artifact": artifact})
    return result


def stage_output(value, stage=None):
    fields(value, ("summary", "items"), "Stage output")
    items = [string(item, "Stage item", 750, True) for item in list_of(value.get("items"), 12, "Stage items")]
    require(items, "Provide at least one stage item.")
    if stage == "concept":
        require(len(items) >= 3, "Record three concepts with a selection rationale in the summary.")
    return {"summary": string(value.get("summary"), "Stage summary", 2500, True), "items": items}


def storyboard(state, value):
    fields(value, ("shots", "hooks", "selectedHook", "tracks", "cuts"), "Storyboard")
    assets = {asset["id"]: asset for asset in state["assets"]}
    profiles = WORKFLOWS[state["workflow"]][1]
    primary = next(iter(profiles))

    def asset_id(raw, label, allowed):
        identifier = string(raw, label, 80)
        if identifier:
            require(
                identifier in assets and assets[identifier]["role"] in allowed,
                f"{label} uses an asset with the wrong role or an unknown ID.",
            )
        return identifier

    def timeline(raw, label):
        shots = []
        for item in list_of(raw, 24, label):
            fields(
                item,
                (
                    "id",
                    "durationMs",
                    "beat",
                    "title",
                    "caption",
                    "action",
                    "audio",
                    "asset",
                    "reference",
                    "trimMs",
                    "style",
                    "evidence",
                    "motion",
                ),
                "Shot",
            )
            beat = item.get("beat")
            style = item.get("style", "clipboard")
            motion = item.get("motion", "still")
            require(isinstance(beat, str) and beat in BEATS, "Choose an allowed shot beat.")
            require(isinstance(style, str) and style in STYLES, "Choose an allowed visual style.")
            require(isinstance(motion, str) and motion in MOTIONS, "Choose an allowed flat motion.")
            duration = integer(item.get("durationMs"), "Shot duration", 300, 30000)
            picture = asset_id(
                item.get("asset", ""), "Picture", ASSET_ROLES - {"reference", "voice", "music", "foley"}
            )
            trim = integer(item.get("trimMs", 0), "Clip trim", 0, 60000)
            if picture and assets[picture]["role"] == "clip":
                require(
                    trim + duration <= assets[picture]["durationMs"] + 35,
                    "The clip is too short for this trim and shot.",
                )
            else:
                require(trim == 0, "Trim applies to clips.")
            caption = string(item.get("caption", ""), "Caption", 65)
            require(
                len(caption.splitlines()) <= 2 and all(len(line) <= 32 for line in caption.splitlines()),
                "Captions need at most two lines of 32 characters.",
            )
            shots.append(
                {
                    "id": project_id(item.get("id")),
                    "durationMs": duration,
                    "beat": beat,
                    "title": string(item.get("title", ""), "Shot title", 48),
                    "caption": caption,
                    "action": string(item.get("action", ""), "Action", 500),
                    "audio": string(item.get("audio", ""), "Audio cue", 300),
                    "asset": picture,
                    "reference": asset_id(item.get("reference", ""), "Planning reference", {"reference"}),
                    "trimMs": trim,
                    "style": style,
                    "motion": motion,
                    "evidence": string(item.get("evidence", ""), "Evidence", 500),
                }
            )
        require(len({shot["id"] for shot in shots}) == len(shots), "Shot IDs must be unique within the cut.")
        return shots

    shots = timeline(value.get("shots", []), primary)
    hooks = []
    for item in list_of(value.get("hooks", []), 3, "Hooks"):
        fields(item, ("id", "title", "variable"), "Hook")
        hooks.append(
            {
                "id": project_id(item.get("id")),
                "title": string(item.get("title"), "Hook", 48, True),
                "variable": string(item.get("variable"), "Test variable", 120, True),
            }
        )
    selected = string(value.get("selectedHook", ""), "Selected hook", 63)
    require(len({hook["id"] for hook in hooks}) == len(hooks), "Hook IDs must be unique.")
    require(
        not hooks and not selected or any(hook["id"] == selected for hook in hooks),
        "Select an existing hook.",
    )
    require(
        not hooks or len({hook["variable"].casefold() for hook in hooks}) == 1,
        "Hook variants must test the same declared variable.",
    )
    tracks = []
    for item in list_of(value.get("tracks", []), 20, "Audio tracks"):
        fields(
            item, ("asset", "atMs", "trimMs", "durationMs", "gain", "fadeInMs", "fadeOutMs"), "Audio track"
        )
        asset = asset_id(item.get("asset"), "Audio", {"voice", "music", "foley"})
        require(asset, "Select an audio asset.")
        duration = integer(item.get("durationMs"), "Audio duration", 100, 30000)
        trim = integer(item.get("trimMs", 0), "Audio trim", 0, 60000)
        gain = item.get("gain", 1)
        require(type(gain) in (int, float) and 0 <= gain <= 4, "Gain must be between 0 and 4.")
        require(trim + duration <= assets[asset]["durationMs"] + 35, "Audio trim exceeds the asset.")
        at = integer(item.get("atMs"), "Audio placement", 0, profiles[primary] * 1000)
        require(at + duration <= profiles[primary] * 1000, "Audio extends past the primary cut.")
        fade_in = integer(item.get("fadeInMs", 0), "Fade in", 0, duration)
        fade_out = integer(item.get("fadeOutMs", 0), "Fade out", 0, duration)
        require(fade_in + fade_out <= duration, "Audio fades overlap.")
        tracks.append(
            {
                "asset": asset,
                "atMs": at,
                "trimMs": trim,
                "durationMs": duration,
                "gain": gain,
                "fadeInMs": fade_in,
                "fadeOutMs": fade_out,
            }
        )
    cuts = fields(value.get("cuts", state.get("cuts", {})), set(profiles) - {primary}, "Secondary cuts")
    return {
        "shots": shots,
        "hooks": hooks,
        "selectedHook": selected,
        "tracks": tracks,
        "cuts": {key: timeline(items, key) for key, items in cuts.items()},
    }


def brief_issues(state):
    brief = state["brief"]
    issues = []
    missing = [
        key
        for key in (
            "brand",
            "product",
            "audience",
            "market",
            "objective",
            "facts",
            "cta",
            "rights",
            "measurement",
        )
        if not brief[key]
    ]
    if missing:
        issues.append("Brief needs " + ", ".join(missing) + ".")
    if brief["claim"] and not brief["proof"]:
        issues.append("Link the main claim to proof.")
    for flag in brief["riskFlags"]:
        if flag in {"endorsement", "face-swap", "review-gating", "dark-pattern", "misleading-claim"}:
            issues.append(f"Resolve prohibited creative risk: {flag}.")
    if "real-likeness" in brief["riskFlags"] and not brief["consent"]:
        issues.append("Record written likeness or voice permission.")
    if (
        state["workflow"] in {"diwali-campaign", "product-launch", "super-bowl-style"}
        and not brief["launchPlan"]
    ):
        issues.append("Record the launch calendar.")
    if brief["offer"] or state["workflow"] in {"diwali-campaign", "product-launch"}:
        try:
            require(bool(brief["offer"]), "Record the offer.")
            date.fromisoformat(brief["offerEnd"])
        except ValueError:
            issues.append("Record the offer terms and an ISO end date.")
    if state["workflow"] == "ugc-creator" and not (brief["disclosure"] and brief["consent"]):
        issues.append("Record creator consent and placement of the paid-partnership disclosure.")
    return issues


def timeline_issues(state):
    profiles = WORKFLOWS[state["workflow"]][1]
    issues = []
    for index, (key, seconds) in enumerate(profiles.items()):
        shots = state["shots"] if index == 0 else state["cuts"].get(key, [])
        duration = seconds * 1000
        if not shots or sum(shot["durationMs"] for shot in shots) != duration:
            issues.append(f"{key}: shots must total {seconds} seconds.")
            continue
        if shots[0]["beat"] != "hook" or not (shots[0]["title"] or (index == 0 and state["selectedHook"])):
            issues.append(f"{key}: start with a legible hook on frame zero.")
        if shots[0]["durationMs"] < 1000:
            issues.append(f"{key}: hold the first hook for at least one second.")
        cta = [i for i, shot in enumerate(shots) if shot["beat"] == "cta"]
        if cta != [len(shots) - 1] or not shots[-1]["title"]:
            issues.append(f"{key}: end with exactly one CTA shot.")
        elif duration - shots[-1]["durationMs"] < max(duration * 4 // 5, duration - 3000):
            issues.append(f"{key}: CTA starts before the approved window.")
        elif shots[-1]["title"].casefold() != state["brief"]["cta"].casefold():
            issues.append(f"{key}: CTA must match the brief.")
        if any(not shot["caption"] for shot in shots):
            issues.append(f"{key}: add a caption to each shot for sound-off review.")
        if state["workflow"] == "ugc-creator" and not any(shot["asset"] for shot in shots):
            issues.append(f"{key}: attach creator-shot footage.")
    return issues


def rights_issues(state):
    shots = state["shots"] + [shot for cut in state["cuts"].values() for shot in cut]
    used = {shot["asset"] for shot in shots if shot["asset"]} | {track["asset"] for track in state["tracks"]}
    issues = []
    for asset in state["assets"]:
        if asset["id"] not in used:
            continue
        if not (asset["rights"] and asset["source"]):
            issues.append(f"{asset['name']}: record rights and provenance.")
        if asset["role"] == "voice" and not asset["consent"]:
            issues.append(f"{asset['name']}: record voice consent.")
        if (
            "real-likeness" in state["brief"]["riskFlags"]
            and asset["role"] in {"clip", "cutout"}
            and not asset["consent"]
        ):
            issues.append(f"{asset['name']}: record written permission for the depicted person.")
    return issues


def actual_metrics(value):
    result = []
    for item in list_of(value, 12, "Metrics"):
        fields(item, ("name", "sample", "value"), "Metric")
        reading = item.get("value")
        require(type(reading) in (float, int) and 0 <= reading <= 1e12, "Invalid metric value.")
        result.append(
            {
                "name": string(item.get("name"), "Metric name", 100, True),
                "sample": integer(item.get("sample"), "Sample size", 1, 10**9),
                "value": reading,
            }
        )
    return result
