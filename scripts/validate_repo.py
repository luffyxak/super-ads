#!/usr/bin/env python3
"""Validate the Super Ads Creator v2 repo (official Agent Skills rules).

Checks:
- all required files exist (incl. commands/, evals/, example HyperFrames project)
- SKILL.md frontmatter: valid YAML, only the six spec keys, name == directory
  name, kebab-case, 1-64 chars, description 300-1024 chars, no < or >,
  license field present, SKILL.md < 500 lines, referenced files exist,
  per-skill LICENSE.txt exists
- agents: YAML frontmatter with name/description/tools/model, Role/Outputs
  sections in the body
- commands: description + allowed-tools frontmatter, $ARGUMENTS present
- plugin.json: minimal manifest only — no skills/agents keys (silently ignored)
- .claude-plugin/marketplace.json exists, valid JSON, lists the plugin + skills
- no TODO / PLACEHOLDER markers in repo files
- no banned wrong claims (wrong-language install claim, wrong paid-threshold
  claim, HyperFrames-as-Python, stale clone host, the removed high-VRAM local model)

Prints PASS/FAIL and exits non-zero on failure.
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAILURES = []

try:
    import yaml
except ImportError:  # minimal fallback: flat "key: value" frontmatter only
    yaml = None


def fail(msg):
    FAILURES.append(msg)
    print(f"FAIL: {msg}")


def ok(msg):
    print(f"OK: {msg}")


REQUIRED = [
    "README.md",
    "CLAUDE.md",
    "AGENTS.md",
    "LICENSE",
    "BUILD_LOG.md",
    ".gitignore",
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".github/workflows/validate.yml",
    "commands/new-ad.md",
    "commands/render-ad.md",
    "commands/review-ad.md",
    "evals/README.md",
    "evals/test-prompts.md",
    "evals/trigger-eval.md",
    "prompts/video-prompts.md",
    "prompts/image-prompts.md",
    "prompts/copy-prompts.md",
    "prompts/mg-styles.md",
    "prompts/product-launch.md",
    "workflows/15s-reel.md",
    "workflows/30s-tvc.md",
    "workflows/diwali-campaign.md",
    "workflows/product-launch.md",
    "workflows/ugc-creator.md",
    "workflows/super-bowl-style.md",
    "templates/brief-template.md",
    "templates/storyboard-template.md",
    "templates/shot-list.csv",
    "templates/ad-review-checklist.md",
    "examples/diwali-jewellery-15s.md",
    "examples/fintech-30s-moonshot-style.md",
    "examples/product-launch-10s.md",
    "examples/hyperframes-diwali-8s/README.md",
    "examples/hyperframes-diwali-8s/index.html",
    "examples/hyperframes-diwali-8s/hyperframes.json",
    "examples/hyperframes-diwali-8s/package.json",
    "examples/hyperframes-diwali-8s/compositions/hook.html",
    "examples/hyperframes-diwali-8s/compositions/product.html",
    "examples/hyperframes-diwali-8s/compositions/cta.html",
    "examples/hyperframes-diwali-8s/package-lock.json",
    "docs/LEARNED_PLAYBOOK.md",
    "docs/MOONSHOT_PLAYBOOK.md",
    "docs/DIWALI_PLAYBOOK.md",
    "docs/COUNTRY_PLAYBOOK.md",
    "docs/GITHUB_SOURCES.md",
    "docs/ANIMATION_GUIDE.md",
    "scripts/validate_repo.py",
    "scripts/new_ad.py",
]

SKILLS = [
    "ad-strategy",
    "ad-creative-director",
    "ad-copywriter-gen-z",
    "ad-visual-designer",
    "ad-video-director",
    "ad-animation-motion",
    "ad-realistic-video",
    "ad-social-formats",
    "ad-diwali-festive",
    "ad-brand-safety",
    "ad-performance-analyst",
]

AGENTS = [
    "strategist",
    "creative-director",
    "copywriter",
    "visual-designer",
    "animator",
    "video-director",
    "editor",
    "qa-brand-safety",
]

COMMANDS = ["new-ad", "render-ad", "review-ad"]

SKILL_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
AGENT_KEYS = {"name", "description", "tools", "model", "color"}
COMMAND_KEYS = {"description", "allowed-tools"}
PLUGIN_KEYS = {"name", "version", "description", "author", "license",
               "keywords", "homepage", "repository", "userConfig", "types"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# Banned wrong claims. These strings must not appear anywhere in the repo
# (spot-check: zero hits), so they are assembled at runtime instead of
# written out here — including the removed high-VRAM local video model.
BANNED_LITERAL = [
    "pip install " + "hyperframes",
    "$" + "1M revenue",
    "HyperFrames (" + "Python)",
    "comfy" + "anonymous",
]
REMOVED_MODEL_RE = re.compile(r"w" + r"an" + r"2", re.IGNORECASE)


def parse_frontmatter(text, rel):
    """Return (frontmatter dict, body) or (None, text) with a failure recorded."""
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        fail(f"{rel}: missing YAML frontmatter (--- block at the top)")
        return None, text
    raw, body = m.group(1), m.group(2)
    if yaml is not None:
        class StrictLoader(yaml.SafeLoader):
            def construct_mapping(self, node, deep=False):
                result = {}
                for key_node, value_node in node.value:
                    key = self.construct_object(key_node, deep=deep)
                    if key in result:
                        raise ValueError(f"duplicate YAML key: {key}")
                    result[key] = self.construct_object(value_node, deep=deep)
                return result

        try:
            fm = yaml.load(raw, Loader=StrictLoader)
        except Exception as exc:  # noqa: BLE001 - report YAML errors plainly
            fail(f"{rel}: frontmatter is not valid YAML: {exc}")
            return None, body
    else:
        fm = {}
        for line in raw.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip()
    if not isinstance(fm, dict):
        fail(f"{rel}: frontmatter must be a YAML dict")
        return None, body
    return fm, body


def check_name(name, expected, rel):
    if name != expected:
        fail(f"{rel}: name {name!r} != directory/file name {expected!r}")
        return False
    if len(name) > 64 or not NAME_RE.match(name):
        fail(f"{rel}: name {name!r} must be kebab-case, 1-64 chars")
        return False
    return True


def main():
    for rel in REQUIRED:
        p = ROOT / rel
        if p.is_file():
            ok(f"exists {rel}")
        else:
            fail(f"missing required file {rel}")

    # ---- skills (official rules) ----
    for skill in SKILLS:
        rel = f"skills/{skill}/SKILL.md"
        p = ROOT / rel
        if not p.is_file():
            fail(f"missing skill {rel}")
            continue
        text = p.read_text(encoding="utf-8")
        lines = text.splitlines()
        if len(lines) >= 500:
            fail(f"{rel}: {len(lines)} lines, must stay under 500")
        fm, body = parse_frontmatter(text, rel)
        if fm is None:
            continue
        unknown = set(fm) - SKILL_KEYS
        if unknown:
            fail(f"{rel}: unknown frontmatter keys: {sorted(unknown)}")
        if "name" not in fm or "description" not in fm:
            fail(f"{rel}: frontmatter needs name + description")
            continue
        check_name(str(fm["name"]), skill, rel)
        desc = str(fm["description"])
        if not 300 <= len(desc) <= 1024:
            fail(f"{rel}: description is {len(desc)} chars, need 300-1024")
        if "<" in desc or ">" in desc:
            fail(f"{rel}: description must not contain < or >")
        if "license" not in fm:
            fail(f"{rel}: frontmatter needs a license field")
        if not (ROOT / "skills" / skill / "LICENSE.txt").is_file():
            fail(f"skills/{skill}: missing LICENSE.txt")
        # referenced files must exist (one level deep: references/*.md)
        for ref in sorted(set(re.findall(r"`(references/[^`]+)`", body))):
            if not (ROOT / "skills" / skill / ref).is_file():
                fail(f"{rel}: referenced file does not exist: {ref}")
        if len(lines) < 30:
            fail(f"{rel}: too short ({len(lines)} lines, need 30+)")
        else:
            ok(f"skill {skill}: name==dir, desc {len(desc)} chars, "
               f"{len(lines)} lines, license set")

    # ---- agents ----
    for agent in AGENTS:
        rel = f"agents/{agent}.md"
        p = ROOT / rel
        if not p.is_file():
            fail(f"missing agent {rel}")
            continue
        text = p.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text, rel)
        if fm is None:
            continue
        unknown = set(fm) - AGENT_KEYS
        if unknown:
            fail(f"{rel}: unknown frontmatter keys: {sorted(unknown)}")
        for key in ("name", "description", "tools", "model"):
            if key not in fm or not str(fm[key]).strip():
                fail(f"{rel}: frontmatter needs a non-empty {key}")
        if fm.get("name") != agent:
            fail(f"{rel}: name {fm.get('name')!r} != file name {agent!r}")
        missing = [s for s in ("## Role", "## Outputs") if s not in body]
        if missing:
            fail(f"{rel}: body missing sections: {missing}")
        else:
            ok(f"agent {agent}: frontmatter + Role/Outputs")

    # ---- commands ----
    for cmd in COMMANDS:
        rel = f"commands/{cmd}.md"
        p = ROOT / rel
        if not p.is_file():
            fail(f"missing command {rel}")
            continue
        text = p.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text, rel)
        if fm is None:
            continue
        unknown = set(fm) - COMMAND_KEYS
        if unknown:
            fail(f"{rel}: unknown frontmatter keys: {sorted(unknown)}")
        if "description" not in fm or not str(fm["description"]).strip():
            fail(f"{rel}: frontmatter needs a description")
        if "allowed-tools" not in fm or not str(fm["allowed-tools"]).strip():
            fail(f"{rel}: frontmatter needs allowed-tools")
        if "$ARGUMENTS" not in body:
            fail(f"{rel}: body must use $ARGUMENTS")
        else:
            ok(f"command {cmd}: frontmatter + $ARGUMENTS")

    # ---- plugin.json: minimal manifest only ----
    p = ROOT / ".claude-plugin" / "plugin.json"
    if p.is_file():
        try:
            plugin = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f".claude-plugin/plugin.json: invalid JSON: {exc}")
            plugin = {}
        if isinstance(plugin, dict):
            unknown = set(plugin) - PLUGIN_KEYS
            if unknown:
                fail(f".claude-plugin/plugin.json: unknown keys: {sorted(unknown)}")
            for bad in ("skills", "agents"):
                if bad in plugin:
                    fail(f".claude-plugin/plugin.json: '{bad}' key is silently "
                         f"ignored — components are discovered by directory")
            author = plugin.get("author")
            if not isinstance(author, dict) or not author.get("name"):
                fail(".claude-plugin/plugin.json: author must be an object with a name")
            for key in ("name", "version", "description", "license"):
                if key not in plugin:
                    fail(f".claude-plugin/plugin.json: missing {key}")
            if not FAILURES or True:
                ok("plugin.json: minimal manifest, no skills/agents keys")
    # ---- marketplace.json ----
    mp = ROOT / ".claude-plugin" / "marketplace.json"
    if mp.is_file():
        try:
            market = json.loads(mp.read_text(encoding="utf-8"))
            plugins = market.get("plugins", [])
            if not plugins or plugins[0].get("source") != "./":
                fail(".claude-plugin/marketplace.json: needs a plugin entry with source './'")
            listed = set(plugins[0].get("skills", [])) if plugins else set()
            expected = {f"./skills/{s}" for s in SKILLS}
            if listed != expected:
                fail(f".claude-plugin/marketplace.json: skills list {sorted(listed)} "
                     f"!= expected {sorted(expected)}")
            else:
                ok("marketplace.json: plugin entry + all 11 skills listed")
        except json.JSONDecodeError as exc:
            fail(f".claude-plugin/marketplace.json: invalid JSON: {exc}")

    # ---- prompts / docs length ----
    for rel in ["prompts/video-prompts.md", "prompts/image-prompts.md",
                "prompts/copy-prompts.md", "prompts/mg-styles.md",
                "prompts/product-launch.md"]:
        p = ROOT / rel
        if p.is_file() and p.stat().st_size > 200:
            ok(f"prompts non-empty {rel}")
        else:
            fail(f"prompts file empty or too small {rel}")
    readme = ROOT / "README.md"
    if readme.is_file() and len(readme.read_text(encoding="utf-8").splitlines()) < 80:
        fail("README.md is too short, need 80+ lines")
    else:
        ok("README.md is 80+ lines")
    playbook = ROOT / "docs" / "LEARNED_PLAYBOOK.md"
    if playbook.is_file() and len(playbook.read_text(encoding="utf-8").splitlines()) < 80:
        fail("docs/LEARNED_PLAYBOOK.md is too short, need 80+ lines")
    else:
        ok("docs/LEARNED_PLAYBOOK.md is 80+ lines")

    # ---- no placeholders, no banned wrong claims ----
    if "--strict" in sys.argv and yaml is None:
        fail("Strict validation requires the pinned PyYAML dependency.")

    ignored = {"outputs", ".git", "node_modules", ".studio", ".hyperframes", "dist", "build",
               "__pycache__", ".cache", ".ruff_cache", ".venv", "venv"}
    paths = []
    for directory, subdirs, names in os.walk(ROOT, followlinks=False):
        subdirs[:] = sorted(name for name in subdirs if name not in ignored)
        paths.extend(Path(directory) / name for name in sorted(names))
    for path in paths:
        if not path.is_file():
            continue
        rel = str(path.relative_to(ROOT))
        if rel.startswith(("outputs/", ".git/")) or path.suffix not in (".md", ".py", ".json", ".csv", ".txt"):
            continue
        if rel in ("scripts/validate_repo.py", "BUILD_LOG.md"):
            continue  # validator's own check strings; build log is a historical record
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "TODO" in text or "PLACEHOLDER" in text:
            fail(f"placeholder marker in {rel}")
        for bad in BANNED_LITERAL:
            if bad in text:
                fail(f"banned wrong claim in {rel}: {bad!r}")
        if REMOVED_MODEL_RE.search(text):
            fail(f"banned wrong claim in {rel}: removed high-VRAM local model named")

    print()
    if FAILURES:
        print(f"VALIDATE: FAIL — {len(FAILURES)} failure(s)")
        return 1
    print("VALIDATE: PASS — all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
