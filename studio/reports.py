"""Draft and release documents generated from the same project snapshot."""

import csv
import html
import json
import zipfile
from pathlib import Path

from .contracts import WORKFLOWS, stage_plan

ESC = html.escape


def one_line(value):
    return " ".join(str(value).splitlines()).replace("|", "\\|")


def markdown_text(value):
    return ESC(str(value)).replace("\n", " ").replace("[", "\\[").replace("]", "\\]")


def timeline(state):
    profiles = WORKFLOWS[state["workflow"]][1]
    for index, cut in enumerate(profiles):
        shots = state["shots"] if index == 0 else state["cuts"].get(cut, [])
        cursor = 0
        selected = next((h["title"] for h in state["hooks"] if h["id"] == state["selectedHook"]), "")
        for shot in shots:
            end = cursor + shot["durationMs"]
            title = (
                selected
                if index == 0 and shot["beat"] == "hook" and cursor == 0 and selected
                else shot["title"]
            )
            yield (
                cut,
                shot["id"],
                f"{cursor / 1000:.3f}",
                f"{end / 1000:.3f}",
                shot["beat"],
                title,
                shot["caption"],
                shot["action"],
                shot["audio"],
                shot["asset"],
                shot["reference"],
                shot["evidence"],
            )
            cursor = end


def sections(state):
    brief = state["brief"]
    label = "Fictional demo" if state["demo"] else "Client project"
    approval = state["approval"]
    status = (
        ("Demo approval test" if state["demo"] else "Human approved")
        if approval
        else "Draft • approval pending"
    )
    intro = [f"{label} · project {state['id']} · revision {state['revision']}", status]
    if approval:
        intro.append(
            f"Reviewer {approval['reviewer']} · approved revision {approval['revision']} · SHA-256 binding {approval['binding']}"
        )
    yield "Status", intro
    yield (
        "Brief and assumptions",
        [
            f"{key} — {brief[key]}"
            for key in (
                "brand",
                "product",
                "audience",
                "market",
                "objective",
                "facts",
                "offer",
                "offerEnd",
                "cta",
                "assumptions",
                "brandAssets",
                "launchPlan",
            )
            if brief[key]
        ],
    )
    labels = {
        "strategy": "Audience and positioning",
        "concept": "Selected concept and discarded alternatives",
        "script": "Script and copy",
        "visual": "Styleframes and continuity",
        "shots": "Director’s shot plan",
        "motion": "Motion plan",
        "capture": "Creator-shot handoff",
        "edit": "Edit and sound plan",
        "qa": "QA role evidence",
        "performance": "Observed analysis",
    }
    for stage in stage_plan(state["workflow"], state["brief"], state["metrics"]):
        key = stage["id"]
        if art := state["artifacts"].get(key):
            yield labels[key], [art["summary"], *art["items"]]
    yield (
        "Hook variants",
        [
            f"{h['id']} {'(selected)' if state['selectedHook'] == h['id'] else ''} — {h['title']} · tests {h['variable']}"
            for h in state["hooks"]
        ],
    )
    yield (
        "Timed storyboard and script",
        [
            f"{cut} {shot} · {start}–{end}s · {beat} · {title} / {caption} · {action}"
            for cut, shot, start, end, beat, title, caption, action, *_ in timeline(state)
        ],
    )
    yield (
        "Sound and action",
        [f"{shot['id']} — {shot['audio']}" for shot in state["shots"] if shot["audio"]]
        + [
            f"{t['asset']} at {t['atMs']} ms, trim {t['trimMs']} ms, hold {t['durationMs']} ms, "
            f"gain {t['gain']}, fades {t['fadeInMs']} / {t['fadeOutMs']} ms"
            for t in state["tracks"]
        ],
    )
    yield "Measurement plan", [brief["measurement"]] if brief["measurement"] else []
    if state["metrics"]:
        yield (
            "Observed results",
            [f"{m['name']} — {m['value']} ({m['sample']} observations)" for m in state["metrics"]],
        )
    yield (
        "Skill and artifact provenance",
        [
            f"{item['role']} · {', '.join(item['skills']) or 'operator capture'} · {item['artifact']} · "
            + (
                f"{art['provider']} · {art['id']}"
                if (art := state["artifacts"].get(item["id"]))
                else "pending"
            )
            for item in stage_plan(state["workflow"], state["brief"], state["metrics"])
        ],
    )
    yield "Review findings", [f"{note['time']:.3f}s — {note['text']}" for note in state["findings"]]
    if state["review"]:
        review = state["review"]
        yield (
            "Independent review",
            [
                f"{review['reviewer']} · {review['verdict']}",
                review["notes"],
                *[f"{key} — {value}/10" for key, value in review["scores"].items()],
            ],
        )
    if state["render"]:
        yield (
            "Technical evidence",
            [f"Verified · {state['render']['verified']}", json.dumps(state["render"]["stats"])],
        )


def tables(state):
    brief = state["brief"]
    return [
        ("Claim-to-proof", ("Claim", "Proof"), [(brief["claim"] or "No objective claim", brief["proof"])]),
        (
            "Rights register",
            ("Asset", "Role", "Source", "Rights", "Consent", "Disclosure", "SHA-256"),
            [
                (a["name"], a["role"], a["source"], a["rights"], a["consent"], a["disclosure"], a["sha256"])
                for a in state["assets"]
            ],
        ),
        (
            "Shot list",
            (
                "Cut",
                "Shot",
                "Start",
                "End",
                "Beat",
                "Title",
                "Caption",
                "Action",
                "Sound",
                "Picture",
                "Planning",
                "Evidence",
            ),
            list(timeline(state)),
        ),
    ]


def build_report(state, folder, artwork=None):
    folder.mkdir(parents=True, exist_ok=False)
    render = state["render"]
    title = f"Super Ads Report · {state['brief']['brand'] or state['id']}"
    md = [f"# {markdown_text(title)}"]
    content = [f"<h1>{ESC(title)}</h1>"]
    for name, items in sections(state):
        md += [f"\n## {name}", *[f"- {markdown_text(item)}" for item in items]]
        content += [
            f"<section><h2>{ESC(name)}</h2><ul>",
            *[f"<li>{ESC(str(item))}</li>" for item in items],
            "</ul></section>",
        ]
    if artwork:
        content += [f'<figure><img alt="Decoded campaign styleframes" src="{artwork}"></figure>']
    for name, header, rows in tables(state):
        md += [
            f"\n## {name}",
            "| " + " | ".join(header) + " |",
            "| " + " | ".join(["---"] * len(header)) + " |",
        ]
        md += ["| " + " | ".join(one_line(markdown_text(val)) for val in row) + " |" for row in rows]
        content += [
            f"<section><h2>{ESC(name)}</h2><div class='scroll'><table><thead><tr>",
            *[f"<th scope='col'>{ESC(k)}</th>" for k in header],
            "</tr></thead><tbody>",
        ]
        content += ["<tr>" + "".join(f"<td>{ESC(str(x))}</td>" for x in row) + "</tr>" for row in rows]
        content += ["</tbody></table></div></section>"]
    links = [
        "storyboard.md",
        "shot-list.csv",
        "prompts-used.md",
        "render-steps.md",
        "rights-and-consent.md",
        "file-hash-manifest.json",
    ]
    if render:
        links += render["files"]
    for hook in state.get("hookPreviews", {}).values():
        links += hook["files"]
    md += ["\n## Deliverables", *[f"- [{name}]({name})" for name in links]]
    content += [
        "<section><h2>Deliverables</h2><ul>",
        *[f'<li><a href="{name}">{name}</a></li>' for name in links],
        "</ul></section>",
    ]
    html_doc = (
        """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>Super Ads Report</title><style>
*{box-sizing:border-box}body{font:15px/1.55 system-ui;color:#192031;background:#faf7f0;margin:0}
main{max-width:75rem;margin:auto;padding:clamp(1rem,5vw,4rem)}h1{font-size:clamp(2rem,6vw,4.5rem);line-height:1}
h2{font-size:1.18rem;color:#1936a8}section{margin:2rem 0;overflow-wrap:anywhere}
.scroll{overflow:auto}table{border-collapse:collapse;width:100%;font-size:.9rem}th,td{padding:.5rem;border-bottom:1px solid #c9c6be;text-align:left}
img{max-width:100%;height:auto}a{color:#1936a8}
@media print{body{background:white}main{max-width:none;padding:0}h2{break-after:avoid}td{font-size:8pt}a{color:inherit}}
</style><main>"""
        + "\n".join(content)
        + "</main></html>"
    )
    (folder / "super-ads-report.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    (folder / "super-ads-report.html").write_text(html_doc, encoding="utf-8")
    board = ["# Storyboard", *sections_as_md(state, "Timed storyboard and script")]
    (folder / "storyboard.md").write_text("\n".join(board) + "\n", encoding="utf-8")
    with (folder / "shot-list.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        _, header, rows = tables(state)[-1]
        writer.writerow(header)
        writer.writerows(
            [("'" + v if v.startswith(("=", "+", "-", "@", "\t", "\r")) else v) for v in row] for row in rows
        )
    (folder / "prompts-used.md").write_text(
        "# Prompts used\n\n"
        + (
            "Manual and fixture role packets. "
            if state["demo"]
            else "Role packet provenance is in the report. "
        )
        + "Shot directions are recorded in the storyboard.\n\n"
        + "\n".join(f"- {markdown_text(s['id'])} — {markdown_text(s['action'])}" for s in state["shots"])
        + "\n",
        encoding="utf-8",
    )
    (folder / "render-steps.md").write_text(
        "# Reproduce the render\n\nInstall locked dependencies and run the Studio doctor. "
        "Open the saved project, finish the editor handoff, then run "
        f"`python3 -m studio render {state['id']}`. "
        "The renderer lints, checks, snapshots, renders, assembles, and verifies local media.\n",
        encoding="utf-8",
    )
    rights = ["# Rights and consent"]
    rights.append(markdown_text(state["brief"]["rights"]))
    rights.extend(
        f"- {markdown_text(a['name'])} · {markdown_text(a['source'])} · {markdown_text(a['rights'])} · "
        f"{markdown_text(a['consent'])} · {markdown_text(a['disclosure'])}"
        for a in state["assets"]
    )
    (folder / "rights-and-consent.md").write_text("\n".join(rights) + "\n", encoding="utf-8")
    from .media_import import sha_file

    hashes = {item.name: sha_file(item) for item in sorted(folder.iterdir())}
    if render:
        hashes.update(render["hashes"])
    for hook in state.get("hookPreviews", {}).values():
        hashes.update(hook["hashes"])
    (folder / "file-hash-manifest.json").write_text(
        json.dumps({"project": state["id"], "revision": state["revision"], "sha256": hashes}, indent=2)
        + "\n",
        encoding="utf-8",
    )
    return sorted(p.name for p in folder.iterdir())


def sections_as_md(state, section):
    return [
        f"- {markdown_text(item)}" for name, items in sections(state) if name == section for item in items
    ]


def build_release(state, folder, render_dir):
    name = f"{state['id']}-delivery.zip"
    files = build_report({**state, "hookPreviews": {}}, folder)
    with zipfile.ZipFile(folder / name, "x", compression=zipfile.ZIP_DEFLATED) as bundle:
        for filename in files:
            bundle.write(folder / filename, filename)
        for filename in state["render"]["files"]:
            bundle.write(Path(render_dir) / filename, filename)
    return name
