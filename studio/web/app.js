const byId = (id) => document.getElementById(id);
const viewRoot = byId("view");
const projectSelect = byId("projects");
const nav = [...document.querySelectorAll("[data-view]")];
const viewLabels = { brief: "Brief & brand", storyboard: "Storyboard & timeline", review: "Review", delivery: "Delivery" };
const aspects = { "9x16": "9:16 · Vertical", "1x1": "1:1 · Square", "16x9": "16:9 · Landscape" };
const workflows = {
  "15s-reel": "15-second reel", "30s-tvc": "30-second TVC",
  "diwali-campaign": "Diwali campaign", "product-launch": "Product launch",
  "ugc-creator": "UGC creator", "super-bowl-style": "Super Bowl-style",
};
const beats = ["hook", "setup", "twist", "payoff", "cta"];
const styles = ["citation", "clipboard", "packshot", "stamp", "end"];
const assetRoles = ["reference", "packshot", "background", "cutout", "clip", "voice", "music", "foley", "logo"];
const audioRoles = ["voice", "music", "foley"];
const rubric = {
  hook: "Hook", clarity: "Clarity", pacing: "Pacing", craft: "Craft",
  brandFit: "Brand fit", rewatchability: "Rewatchability",
};
const busyStatuses = new Set(["running", "cancelling"]);
const briefFields = [
  ["brand", "Brand"], ["product", "Product"], ["audience", "Audience"],
  ["market", "Market & language"], ["objective", "Objective"], ["festival", "Festival / event"],
  ["facts", "Product facts", true], ["claim", "Main claim or story beat", true],
  ["proof", "Claim evidence", true], ["offer", "Offer & terms", true], ["cta", "Call to action"],
  ["offerEnd", "Offer end date", false, "date"],
  ["rights", "Rights & consent", true], ["brandAssets", "Continuity notes", true],
  ["consent", "Likeness or creator consent", true], ["disclosure", "Disclosure placement", true],
  ["measurement", "Measurement criteria", true], ["launchPlan", "Launch calendar", true],
  ["assumptions", "Assumptions", true],
];
const riskFlags = [
  ["real-likeness", "Real likeness or voice"], ["endorsement", "Real endorsement"],
  ["face-swap", "Face swap"], ["review-gating", "Review gating"],
  ["dark-pattern", "Dark pattern"], ["misleading-claim", "Misleading claim"],
];

let project;
let projects = [];
let activeView = "storyboard";
let shotId;
let briefDraft;
let storyboardDraft;
let dirtyBrief = false;
let dirtyStoryboard = false;
let previewTime = 0;
let previewHook = "";
let previewAspect = "9x16";
let reviewAspect = "9x16";
let selectedCut = "";
let reviewedCut = "";
let showSafeZones = false;
let showCaptions = true;
let pollTimer;
let pending = false;
let fieldId = 0;

function element(tag, props = {}, ...children) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(props)) {
    if (value === undefined || value === null) continue;
    if (key.startsWith("on")) node.addEventListener(key.slice(2), value);
    else if (["className", "value", "checked", "disabled", "hidden", "required", "open", "muted", "controls", "playsInline"].includes(key)) node[key] = value;
    else node.setAttribute(key, value);
  }
  for (const child of children.flat(Infinity)) {
    if (child instanceof Node) node.append(child);
    else if (child !== undefined && child !== null && child !== false) node.append(String(child));
  }
  return node;
}
const div = (className, ...children) => element("div", { className }, ...children);
const text = (value, className = "") => element("p", { className }, value);
const heading = (title, action) => div("section-heading", element("h2", {}, title), action);
const chip = (label, mood = "") => element("span", { className: `chip ${mood}` }, label);
const panel = (...children) => element("section", { className: "panel stack" }, ...children);
const button = (label, onClick, opts = {}) => element("button", {
  type: opts.type || "button", className: `button ${opts.kind || "secondary"}`,
  onclick: onClick, disabled: opts.disabled || false,
}, label);

function input(value = "", props = {}) {
  return element("input", { ...props, value });
}
function select(options, value, props = {}) {
  const result = element("select", props, options.map(([id, label]) => element("option", { value: id }, label)));
  result.value = value;
  return result;
}
function field(label, node, wide = false) {
  node.id = node.id || `control-${++fieldId}`;
  return div(wide ? "field wide" : "field", element("label", { for: node.id }, label), node);
}
function multiline(value, props = {}) {
  const area = element("textarea", { rows: 2, ...props });
  area.value = value || "";
  return area;
}
function check(label, checked, change) {
  return element("label", { className: "check" }, input("", {
    type: "checkbox", checked, onchange: (event) => change(event.target.checked),
  }), label);
}
function list(cls, children) {
  return element("ul", { className: cls }, children);
}
function link(label, href, cls = "", download = false) {
  return element("a", { href, className: cls, download: download ? "" : undefined }, label);
}
function detail(label, ...children) {
  return element("details", { className: "details divider" }, element("summary", {}, label), ...children);
}
const projectPath = (tail = "") => `/api/projects/${encodeURIComponent(project.id)}${tail}`;
const assetURL = (asset) => projectPath(`/assets/${encodeURIComponent(asset)}`);
const fileURL = (file) => projectPath(`/files/${encodeURIComponent(file)}`);
const seconds = (ms) => (ms / 1000).toFixed(3);
const number = (node) => node.valueAsNumber || 0;
const asItems = (value) => Array.isArray(value) ? value : [];
const asFiles = (value) => asItems(value?.files).map((item) => typeof item === "string" ? item : item.name).filter(Boolean);
const stageName = (name) => ({ qa: "QA", cta: "CTA", "qa-brand-safety": "QA / Brand Safety" })[name] ||
  String(name || "").replaceAll("-", " ").replace(/^./, (char) => char.toUpperCase());
const primaryCut = () => project.primaryCut || Object.keys(project.profiles || {})[0];
const cutOptions = () => {
  const profiles = project.profiles || {};
  const ids = Object.keys(profiles).filter((id) => id !== primaryCut());
  return [primaryCut(), ...ids].filter(Boolean).map((id) => [id, `${stageName(id)} · ${profiles[id]}s`]);
};
const currentShots = (draft) => selectedCut === primaryCut() ? draft.shots : draft.cuts?.[selectedCut] || [];

async function request(path, body) {
  const options = body === undefined ? {} : {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
  };
  const response = await fetch(path, options);
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || `Request failed (${response.status})`);
  return payload;
}

function setMessage(message = "", error = "") {
  byId("status").textContent = message;
  byId("error").textContent = error;
  byId("error").hidden = !error;
}
function updateRail() {
  projectSelect.replaceChildren(element("option", { value: "" }, "Choose a campaign"),
    ...projects.map((entry) => element("option", { value: entry.id }, entry.brief?.brand ? `${entry.brief.brand} · ${entry.id}` : entry.id)));
  projectSelect.value = project?.id || "";
  projectSelect.disabled = projects.length === 0;
  for (const item of nav) {
    item.disabled = !project;
    if (item.dataset.view === activeView && project) item.setAttribute("aria-current", "page");
    else item.removeAttribute("aria-current");
  }
  byId("rail-state").replaceChildren(...(project ? [
    element("div", { className: "eyebrow" }, "Production state"),
    div("row", chip(`R${String(project.revision).padStart(2, "0")}`), project.demo && chip("Fictional fixture", "good")),
    text(project.nextStage ? `Up next · ${stageName(project.nextStage)}` : "Workflow handoffs complete", "small"),
  ] : [text("Private by default", "eyebrow"), text("Campaign data stays in local storage on this machine.", "small")]));
}

function syncState(next, { resetBrief = false, resetStoryboard = false } = {}) {
  const switching = project?.id !== next.id;
  project = next;
  if (switching || !dirtyBrief || resetBrief) {
    briefDraft = structuredClone(project.brief || {});
    dirtyBrief = false;
  }
  if (switching || !dirtyStoryboard || resetStoryboard) {
    storyboardDraft = structuredClone({
      shots: asItems(project.shots), hooks: asItems(project.hooks),
      selectedHook: project.selectedHook || "", tracks: asItems(project.tracks), cuts: project.cuts || {},
    });
    dirtyStoryboard = false;
  }
  if (switching) {
    selectedCut = primaryCut();
    reviewedCut = primaryCut();
    shotId = undefined;
    previewTime = 0;
    previewHook = project.selectedHook || "";
  }
  if (!currentShots(storyboardDraft).some((shot) => shot.id === shotId)) shotId = currentShots(storyboardDraft)[0]?.id;
  if (!storyboardDraft.hooks.some((hook) => hook.id === previewHook)) previewHook = storyboardDraft.selectedHook;
  const item = { id: project.id, brief: project.brief, revision: project.revision };
  projects = projects.some((entry) => entry.id === project.id)
    ? projects.map((entry) => entry.id === project.id ? item : entry) : [...projects, item];
  localStorage.setItem("super-ads-project", project.id);
  renderWorkspace();
  schedulePoll();
}

async function mutate(action, body, success, reset = {}) {
  if (!project || pending) return;
  const target = project.id;
  setMessage("Saving to the local workspace…");
  pending = true;
  try {
    const next = await request(projectPath(`/${action}`), { revision: project.revision, ...body });
    if (project?.id === target) {
      syncState(next, reset);
      setMessage(success);
    }
  } catch (error) {
    if (project?.id === target) setMessage("", error.message);
  } finally {
    pending = false;
  }
}

function schedulePoll() {
  clearTimeout(pollTimer);
  if (!busyStatuses.has(project?.attempt?.status)) return;
  const target = project.id;
  pollTimer = setTimeout(async () => {
    if (pending) {
      schedulePoll();
      return;
    }
    try {
      const next = await request(projectPath());
      if (project?.id !== target) return;
      if (busyStatuses.has(next.attempt?.status)) {
        project = next;
        schedulePoll();
        return;
      }
      syncState(next);
      setMessage(next.attempt?.status === "succeeded" ? "Render finished. Review the output." : "",
        next.attempt?.status === "succeeded" ? "" : `Render ${next.attempt?.status || "stopped"}. ${next.attempt?.message || ""}`);
    } catch (error) {
      setMessage("", error.message);
      if (project?.id === target) schedulePoll();
    }
  }, 1250);
}

function openView(view, moveFocus = true) {
  if (!project) return;
  activeView = view;
  setMessage();
  renderWorkspace();
  if (moveFocus) byId("page-title")?.focus({ preventScroll: true });
}
function pageHeader(view, label, subtitle, actions = []) {
  return div("page-head", div("head-copy",
    text(`${project.brief?.brand || project.id} / ${workflows[project.workflow] || project.workflow}`, "eyebrow"),
    element("h1", { id: "page-title", tabindex: "-1" }, viewLabels[view]),
    text(subtitle),
  ), div("row", project.demo && chip("Fictional fixture", "good"), label, actions));
}
function issues() {
  const values = asItems(project.issues);
  return values.length ? div("notice", element("strong", {}, "Needs attention"),
    list("", values.map((issue) => element("li", {}, typeof issue === "string" ? issue : issue.message || issue.code || "Check the brief")))) : null;
}

function briefView() {
  const form = element("form", { className: "panel stack", onsubmit: (event) => {
    event.preventDefault();
    mutate("brief", { brief: briefDraft }, "Brief saved", { resetBrief: true });
  } }, heading("Campaign brief", chip(`Revision ${project.revision}`)),
  div("form-grid", briefFields.map(([key, label, long, type]) => {
    const props = { oninput: (event) => { briefDraft[key] = event.target.value; dirtyBrief = true; } };
    return field(label, long ? multiline(briefDraft[key], props) : input(briefDraft[key] ?? "", { ...props, type }), long);
  })),
  check("Uses realistic or supplied footage", !!briefDraft.footage, (value) => {
    briefDraft.footage = value;
    dirtyBrief = true;
  }),
  detail("Review creative risk flags", div("form-grid", riskFlags.map(([key, label]) => check(label,
    asItems(briefDraft.riskFlags).includes(key), (enabled) => {
      briefDraft.riskFlags = asItems(briefDraft.riskFlags).filter((flag) => flag !== key);
      if (enabled) briefDraft.riskFlags.push(key);
      dirtyBrief = true;
    })))),
  div("row", button("Save brief", null, { kind: "primary", type: "submit" }),
    text("Upstream edits can invalidate handoffs and approvals.", "small muted")));
  return [pageHeader("brief", null, "Set the story, proof, rights, and measurement before production."),
    div("workspace-columns", form, div("stack",
      panel(heading("Brand continuity"), text("Keep approved product artwork and references under distinct roles. Use asset IDs in shots and keep proof attached to the approved brief revision.", "small muted"),
        issues(), assetLibrary()), handoffs()))];
}

function assetLibrary() {
  const assets = asItems(project.assets);
  const fields = {
    file: input("", { type: "file", required: true, accept: "image/png,image/jpeg,image/webp,video/mp4,audio/wav,audio/mpeg,audio/mp4" }),
    role: select(assetRoles.map((role) => [role, stageName(role)]), "reference"),
    rights: multiline("", { required: true, placeholder: "Original artwork, contract reference, or licence terms" }),
    source: input("", { required: true, placeholder: "Creator or source record" }),
    disclosure: input("", { placeholder: "Required watermark or disclosure" }),
    consent: input("", { placeholder: "Written permission reference, if applicable" }),
  };
  const form = element("form", { className: "stack", onsubmit: async (event) => {
    event.preventDefault();
    const file = fields.file.files[0];
    if (!file) return;
    if (file.size > 16 * 1024 * 1024) {
      setMessage("", "Choose an asset no larger than 16 MiB.");
      return;
    }
    const id = project.id;
    try {
      const data = await new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(String(reader.result).split(",", 2)[1]);
        reader.onerror = () => reject(new Error("Could not read the selected file."));
        reader.readAsDataURL(file);
      });
      if (project.id !== id) return;
      await mutate("import", {
        name: file.name, role: fields.role.value, rights: fields.rights.value,
        source: fields.source.value, disclosure: fields.disclosure.value, consent: fields.consent.value, data,
      }, "Asset imported");
    } catch (error) {
      setMessage("", error.message);
    }
  } }, div("form-grid",
    field("Asset file", fields.file, true), field("Asset role", fields.role), field("Source / provenance", fields.source),
    field("Rights record", fields.rights, true), field("Disclosure", fields.disclosure), field("Consent record", fields.consent),
  ), div("row", button("Import asset", null, { type: "submit" }), text("Local file · 16 MiB maximum", "small muted")));
  return div("stack",
    assets.length ? list("asset-list", assets.map((asset) => element("li", { className: "asset-row" },
      div("row", element("strong", {}, asset.name), chip(stageName(asset.role))),
      text(asset.rights || "Rights record missing", "small muted"),
      asset.disclosure && text(asset.disclosure, "small muted"),
    ))) : text("No imported assets yet.", "small muted"),
    detail("Import an asset", form),
  );
}

function handoffs() {
  const stages = asItems(project.stages);
  const artifacts = project.artifacts || {};
  const next = stages.find((stage) => stage.id === project.nextStage);
  const summary = multiline("", { maxlength: "2400", placeholder: "A concise, reviewable handoff" });
  const items = multiline("", { maxlength: "6000", placeholder: "One entry per line" });
  const editForm = next && element("form", { className: "stack divider", onsubmit: (event) => {
    event.preventDefault();
    mutate("stage", { output: { summary: summary.value, items: items.value.split("\n").map((line) => line.trim()).filter(Boolean) } }, "Handoff committed");
  } }, text(`Next · ${stageName(next.role || next.id)}`, "eyebrow"),
    field("Handoff summary", summary), field("Handoff items", items),
    div("row", button("Commit handoff", null, { kind: "primary", type: "submit" })),
  );
  return panel(heading("Workflow handoffs", chip(`${Object.keys(artifacts).length}/${stages.length}`)),
    list("handoffs", stages.map((stage) => {
      const artifact = artifacts[stage.id];
      const contents = artifact?.output || artifact;
      return element("li", { className: "handoff-row" },
        div("row", element("strong", {}, stageName(stage.role || stage.id)), chip(artifact ? "Saved" : next?.id === stage.id ? "Next" : "Waiting", artifact ? "good" : "")),
        text(asItems(stage.skills).join(" · "), "small muted"),
        contents?.summary && detail(stageName(stage.artifact || "Handoff"),
          text(contents.summary, "small"), list("artifact-list", asItems(contents.items).map((item) => element("li", { className: "small" }, item)))),
      );
    })), editForm || text("The current revision has all workflow handoffs.", "small muted"),
    project.demo && next && next.id !== "qa" && div("row",
      button("Restore fixture handoffs", () => mutate("fixture", {}, "Fictional handoffs restored"))));
}

function conceptBoard() {
  const stage = asItems(project.stages).find((entry) => entry.role === "creative-director" || entry.id === "concept");
  const artifact = (project.artifacts || {})[stage?.id];
  const contents = artifact?.output || artifact;
  return panel(heading("Concept board", contents && chip("Handoff", "good")),
    contents ? [text(contents.summary, "small"), list("artifact-list", asItems(contents.items).map((item) => element("li", { className: "small" }, item)))]
      : text("Commit the Creative Director handoff to record the selected concept and discarded alternatives.", "small muted"));
}

function starts(shots) {
  let time = 0;
  return shots.map((shot) => {
    const start = time;
    time += shot.durationMs;
    return start;
  });
}
function totalDuration(shots) {
  return shots.reduce((sum, shot) => sum + shot.durationMs, 0);
}
function safeOverlay() {
  return div("safe-overlay", element("span", { "aria-hidden": "true" }, "SAFE"));
}
function storyboardMonitor() {
  const savedShots = asItems(currentShots(project));
  const draftShots = currentShots(storyboardDraft);
  const isPrimary = selectedCut === primaryCut();
  const draftStarts = starts(draftShots);
  const savedStarts = starts(savedShots);
  const maxMs = Math.max(0, totalDuration(savedShots) - 1);
  previewTime = Math.min(previewTime, maxMs);
  const frame = savedShots.length ? element("iframe", {
    title: "Storyboard preview", sandbox: "allow-scripts",
  }) : null;
  const timestamp = input(seconds(previewTime), { type: "number", min: "0", max: seconds(maxMs), step: ".001" });
  const readout = element("span", { className: "transport-time" });
  const slider = input(previewTime, {
    type: "range", min: "0", max: String(maxMs), step: "1", "aria-label": "Timeline scrubber", disabled: !frame,
  });
  const overlay = safeOverlay();
  overlay.hidden = !showSafeZones;
  const picture = div(`picture ratio-${previewAspect}`, frame, overlay);
  function seek(ms) {
    previewTime = Math.max(0, Math.min(Math.round(ms), maxMs));
    timestamp.value = seconds(previewTime);
    slider.value = previewTime;
    readout.textContent = `${seconds(previewTime)} / ${seconds(totalDuration(savedShots))} s`;
    if (frame) frame.src = projectPath(`/preview?${new URLSearchParams({
      time: seconds(previewTime), format: previewAspect, hook: isPrimary ? previewHook : "",
      captions: showCaptions ? "1" : "0", ...(isPrimary ? {} : { cut: selectedCut }),
    })}`);
  }
  let seekTimer;
  slider.addEventListener("input", () => {
    const time = number(slider);
    timestamp.value = seconds(time);
    readout.textContent = `${seconds(time)} / ${seconds(totalDuration(savedShots))} s`;
    clearTimeout(seekTimer);
    seekTimer = setTimeout(() => { if (frame?.isConnected) seek(time); }, 100);
  });
  seek(previewTime);
  const seekForm = element("form", { className: "transport", onsubmit: (event) => {
    event.preventDefault();
    seek(number(timestamp) * 1000);
  } }, slider, div("row",
    field("Timestamp (seconds)", timestamp), button("Seek", null, { type: "submit", disabled: !frame }),
    check("Show safe zones", showSafeZones, (value) => { showSafeZones = value; overlay.hidden = !value; }),
    check("Show captions", showCaptions, (value) => { showCaptions = value; seek(previewTime); }), readout));
  const shotStrip = div("timeline", draftShots.map((shot, index) => {
    return element("button", {
      type: "button", className: "shot-card", "aria-pressed": String(shot.id === shotId),
      onclick: () => {
        shotId = shot.id;
        const savedIndex = savedShots.findIndex((saved) => saved.id === shot.id);
        if (savedIndex >= 0) previewTime = savedStarts[savedIndex];
        renderWorkspace();
        viewRoot.querySelector('.shot-card[aria-pressed="true"]')?.focus({ preventScroll: true });
      },
    }, element("small", {}, `${String(index + 1).padStart(2, "0")} · ${seconds(draftStarts[index]).slice(0, -2)}s`),
    element("span", {}, shot.title || "Untitled shot"), element("small", {}, stageName(shot.beat)));
  }));
  return element("section", { className: "panel monitor", "aria-label": "Storyboard monitor" },
    div("section-heading monitor-head",
      div("row", text("Production monitor", "eyebrow"), chip("Saved scene")),
      div("row",
        cutOptions().length > 1 && select(cutOptions(), selectedCut, { "aria-label": "Timeline cut", onchange: (event) => {
          selectedCut = event.target.value;
          shotId = currentShots(storyboardDraft)[0]?.id;
          previewTime = 0;
          renderWorkspace();
          viewRoot.querySelector('[aria-label="Timeline cut"]')?.focus({ preventScroll: true });
        } }),
        select(Object.entries(aspects), previewAspect, { "aria-label": "Preview aspect ratio", onchange: (event) => {
          previewAspect = event.target.value;
          picture.className = `picture ratio-${previewAspect}`;
          seek(previewTime);
        } }),
        isPrimary && select([["", "Selected hook"], ...asItems(project.hooks).map((hook) => [hook.id, hook.title])], previewHook,
          { "aria-label": "Preview hook", onchange: (event) => { previewHook = event.target.value; seek(previewTime); } }),
      )),
    div("stage", frame ? picture : text("Save a shot to open a scene preview.", "empty-stage")),
    seekForm,
    div("timeline-wrap", heading("Shot strip", chip(`${draftShots.length} shots`)), draftShots.length ? shotStrip : text("Add the first shot in the inspector.", "small muted")),
  );
}

function markStoryboard() {
  dirtyStoryboard = true;
  const indicator = byId("edit-indicator");
  if (indicator) indicator.textContent = "Unsaved edits";
}
function saveStoryboard() {
  mutate("storyboard", storyboardDraft, "Storyboard saved", { resetStoryboard: true });
}
function storyboardEditor() {
  const shots = currentShots(storyboardDraft);
  const isPrimary = selectedCut === primaryCut();
  const shot = shots.find((item) => item.id === shotId);
  const assets = asItems(project.assets);
  const options = (roles) => [["", "None"], ...assets.filter((asset) => roles.includes(asset.role)).map((asset) => [asset.id, `${asset.name} · ${stageName(asset.role)}`])];
  function editShot(key, value) {
    shot[key] = value;
    markStoryboard();
  }
  function addShot() {
    const id = `shot-${crypto.randomUUID().slice(0, 8)}`;
    if (!isPrimary) storyboardDraft.cuts[selectedCut] = shots;
    shots.push({ id, durationMs: 3000, beat: shots.length ? "setup" : "hook", title: "New shot", caption: "",
      action: "", audio: "", asset: "", reference: "", trimMs: 0, style: "citation", motion: "still", evidence: "" });
    shotId = id;
    markStoryboard();
    renderWorkspace();
  }
  function moveShot(offset) {
    const index = shots.indexOf(shot);
    const other = index + offset;
    if (other < 0 || other >= shots.length) return;
    [shots[index], shots[other]] = [shots[other], shots[index]];
    markStoryboard();
    renderWorkspace();
  }
  const shotText = (key, long = false) => {
    const props = { oninput: (event) => editShot(key, event.target.value) };
    return long ? multiline(shot[key], props) : input(shot[key], props);
  };
  const shotNumber = (key, min) => input(shot[key], { type: "number", min, step: "1", oninput: (event) => editShot(key, number(event.target)) });
  const shotChoice = (key, choices) => select(choices, shot[key], { onchange: (event) => { editShot(key, event.target.value); if (key === "reference") renderWorkspace(); } });
  const liveShot = currentShots(project).find((item) => item.id === shotId);
  const ref = assets.find((item) => item.id === shot?.reference && item.role === "reference");
  return panel(
    heading("Shot inspector", chip(shot?.id || "No shot")),
    shot ? [
      div("form-grid",
        field("Shot title", shotText("title"), true),
        field("Beat", shotChoice("beat", beats.map((beat) => [beat, stageName(beat)]))),
        field("Duration (ms)", shotNumber("durationMs", 300)),
        field("Caption", shotText("caption", true), true),
        field("Picture treatment", shotChoice("style", styles.map((style) => [style, stageName(style)]))),
        field("Flat motion", shotChoice("motion", [["still", "Still"], ["push", "Push"], ["float", "Float"]])),
        field("Clip trim (ms)", shotNumber("trimMs", 0)),
        field("Render asset", shotChoice("asset", options(["packshot", "background", "cutout", "clip", "logo"])), true),
        field("Planning reference", shotChoice("reference", options(["reference"])), true),
        field("Action / camera", shotText("action", true), true),
        field("Sound cue", shotText("audio")),
        field("Evidence ID or note", shotText("evidence")),
      ),
      ref && div("stack", div("row", chip("Planning only"), text(ref.name, "small muted")),
        element("img", { className: "reference-media", src: assetURL(ref.id), alt: ref.name, loading: "lazy" })),
      div("row editor-actions",
        button("Move earlier", () => moveShot(-1), { disabled: shots.indexOf(shot) < 1 }),
        button("Move later", () => moveShot(1), { disabled: shots.indexOf(shot) >= shots.length - 1 }),
        button("Remove shot", () => {
          shots.splice(shots.indexOf(shot), 1);
          shotId = shots[0]?.id;
          markStoryboard();
          renderWorkspace();
        })),
    ] : text("Create a shot to start the timeline.", "small muted"),
    div("row divider editor-actions",
      button("Add shot", addShot),
      button("Save storyboard", saveStoryboard, { kind: "primary" })),
    div("row", text(dirtyStoryboard ? "Unsaved edits" : "Preview reads the saved revision.", "small muted"), div("eyebrow", element("span", { id: "edit-indicator" })),
      liveShot && link("Export shot reference", projectPath(`/reference?${new URLSearchParams({
        shot: shotId, ...(isPrimary ? {} : { cut: selectedCut }),
      })}`), "small", true)),
  );
}

function hookEditor() {
  const hooks = storyboardDraft.hooks;
  return detail(`Hook variants · ${hooks.length}/3`, div("stack",
    text("Choose a single opening variable. The approved product, offer, and proof stay shared across variants.", "small muted"),
    hooks.map((hook) => div("form-grid",
      field("Hook title", input(hook.title, { oninput: (event) => { hook.title = event.target.value; markStoryboard(); } }), true),
      field("Variable tested", input(hook.variable, { oninput: (event) => { hook.variable = event.target.value; markStoryboard(); } })),
      div("row", button("Remove hook", () => {
        hooks.splice(hooks.indexOf(hook), 1);
        if (storyboardDraft.selectedHook === hook.id) storyboardDraft.selectedHook = hooks[0]?.id || "";
        markStoryboard();
        renderWorkspace();
      })))),
    field("Selected hook", select([["", "Use shot title"], ...hooks.map((hook) => [hook.id, hook.title])], storyboardDraft.selectedHook, {
      onchange: (event) => { storyboardDraft.selectedHook = event.target.value; markStoryboard(); },
    })),
    div("row", button("Add hook", () => {
      const id = `hook-${crypto.randomUUID().slice(0, 8)}`;
      hooks.push({ id, title: "New opening", variable: hooks[0]?.variable || "Opening line" });
      if (!storyboardDraft.selectedHook) storyboardDraft.selectedHook = id;
      markStoryboard();
      renderWorkspace();
    }, { disabled: hooks.length >= 3 }), button("Save variants", saveStoryboard)),
    ...asItems(project.hooks).map((hook) => {
      const record = project.hookPreviews?.[hook.id];
      return div("row",
        button(`Render hook test · ${hook.title}`, () => mutate("hook", { hook: hook.id }, "Hook preview queued"),
          { disabled: busyStatuses.has(project.attempt?.status) }),
        ...asFiles(record).filter((file) => file.endsWith(".mp4")).map((file) => link("Watch hook test", fileURL(file), "small")),
      );
    }),
  ));
}

function audioEditor() {
  const tracks = storyboardDraft.tracks;
  const audioAssets = asItems(project.assets).filter((asset) => audioRoles.includes(asset.role));
  const trackFields = [
    ["atMs", "Placement (ms)", 0, 1], ["trimMs", "Trim in (ms)", 0, 1], ["durationMs", "Duration (ms)", 1, 1],
    ["gain", "Gain multiplier", 0, .05], ["fadeInMs", "Fade in (ms)", 0, 1], ["fadeOutMs", "Fade out (ms)", 0, 1],
  ];
  return detail(`Audio placement · ${tracks.length} cues`, div("stack",
    text("Import a voice, music, or foley file, then place it on the campaign timeline.", "small muted"),
    tracks.map((track) => div("form-grid",
      field("Audio source", select(audioAssets.map((asset) => [asset.id, asset.name]), track.asset, {
        onchange: (event) => { track.asset = event.target.value; markStoryboard(); },
      }), true),
      trackFields.map(([key, label, min, step]) => field(label, input(track[key], {
        type: "number", min, step, oninput: (event) => { track[key] = number(event.target); markStoryboard(); },
      }))),
      button("Remove cue", () => { tracks.splice(tracks.indexOf(track), 1); markStoryboard(); renderWorkspace(); }),
    )),
    div("row", button("Add audio cue", () => {
      tracks.push({ asset: audioAssets[0].id, atMs: 0, trimMs: 0, durationMs: 1000, gain: 1, fadeInMs: 0, fadeOutMs: 0 });
      markStoryboard();
      renderWorkspace();
    }, { disabled: !audioAssets.length }), button("Save audio placement", saveStoryboard)),
  ));
}

function renderAction() {
  const attempt = project.attempt;
  if (busyStatuses.has(attempt?.status)) {
    return [chip(stageName(attempt.status), "warning"),
      button("Cancel render", () => mutate("cancel", {}, "Cancellation requested"), { disabled: attempt.status === "cancelling" })];
  }
  return button("Render cuts", () => mutate("render", {}, "Render queued"), {
    kind: "primary", disabled: !asItems(project.shots).length,
  });
}

function storyboardView() {
  const label = project.render?.verified ? chip("Media verified", "good") : chip("Working cut");
  return [pageHeader("storyboard", label, "Build the sequence, preview the hook, and retake individual shots.", renderAction()),
    div("workspace-columns", div("stack",
      storyboardMonitor(), conceptBoard(), panel(heading("Production controls"), hookEditor(), audioEditor()), handoffs()),
      div("stack", storyboardEditor(), panel(heading("Assets"), assetLibrary()))),
  ];
}

function actualCut(format) {
  const name = `master-${format}.mp4`;
  const file = reviewedCut === primaryCut() ? name : `${reviewedCut}-${name}`;
  return asFiles(project.render).includes(file) ? file : null;
}

function reviewMonitor() {
  const current = actualCut(reviewAspect);
  const renderFiles = asFiles(project.render);
  const video = current && element("video", {
    src: fileURL(current), controls: true, muted: true, playsInline: true, preload: "metadata", "aria-label": "Rendered cut",
  });
  const isPrimary = reviewedCut === primaryCut();
  const preview = !video && asItems(isPrimary ? project.shots : project.cuts?.[reviewedCut]).length && element("iframe", {
    src: projectPath(`/preview?${new URLSearchParams({
      time: "0", format: reviewAspect, ...(isPrimary ? {} : { cut: reviewedCut }),
    })}`),
    title: "First saved frame", sandbox: "allow-scripts",
  });
  const overlay = safeOverlay();
  overlay.hidden = !showSafeZones;
  const evidence = renderFiles.filter((name) => /\.(?:png|jpe?g|webp)$/i.test(name));
  return div("stack",
    element("section", { className: "panel monitor review-monitor" },
      div("section-heading monitor-head", div("row", text("Review monitor", "eyebrow"),
        chip(current ? "Actual export" : "Scene preview", current ? "good" : "")),
      div("row", cutOptions().length > 1 && select(cutOptions(), reviewedCut, {
        "aria-label": "Review cut", onchange: (event) => { reviewedCut = event.target.value; renderWorkspace(); },
      }), select(Object.entries(aspects), reviewAspect, {
        "aria-label": "Review aspect ratio", onchange: (event) => { reviewAspect = event.target.value; renderWorkspace(); },
      }))),
      div("stage", video || preview ? div(`picture ratio-${reviewAspect}`, video || preview, overlay)
        : text("Render a campaign to open the review monitor.", "empty-stage")),
      div("transport",
        div("row", check("Show safe zones", showSafeZones, (value) => { showSafeZones = value; overlay.hidden = !value; }),
          video && check("Mute playback", true, (value) => { video.muted = value; }),
          video && link("Download current cut", fileURL(current), "small", true)),
        text(current ? "Rendered captions are burned in. Start muted and listen again to check the mix."
          : "Draft scene only. Complete a render to review playback and decoded frames.", "small muted"),
      )),
    panel(heading("Visual evidence"),
      evidence.length ? evidence.map((file) => div("stack",
        element("img", { src: fileURL(file), className: "audit-image", alt: `Decoded evidence from ${file}`, loading: "lazy" }),
        link(file, fileURL(file), "small", true),
      )) : text("Contact sheets and frame strips appear after media verification.", "small muted")),
  );
}

function reviewForm() {
  const review = project.review;
  const who = input("", { required: true, maxlength: "100", autocomplete: "off" });
  const verdict = select([["changes", "Needs changes"], ["pass", "Pass"]], "changes");
  const notes = multiline("", { required: true, maxlength: "2000", placeholder: "What did you observe on the current cuts?" });
  const scores = Object.entries(rubric).map(([key, label]) => [key, label, input("", { type: "number", min: "1", max: "10", step: "1" })]);
  const form = element("form", { className: "stack", onsubmit: (event) => {
    event.preventDefault();
    mutate("review", {
      reviewer: who.value, verdict: verdict.value, notes: notes.value,
      scores: Object.fromEntries(scores.filter(([, , node]) => node.value !== "").map(([key, , node]) => [key, number(node)])),
    }, "Review recorded");
  } }, div("form-grid", field("Creative reviewer", who), field("Verdict", verdict), field("Review notes", notes, true)),
  text("A pass requires 7 or higher in each category.", "small muted"),
  div("rubric", scores.map(([, label, node]) => field(label, node))),
  div("row", button("Record creative review", null, { type: "submit", disabled: !project.render?.verified || !project.artifacts?.qa })));
  const approver = input("", { required: true, maxlength: "100", autocomplete: "off" });
  const approvalForm = element("form", { className: "stack divider", onsubmit: (event) => {
    event.preventDefault();
    mutate("approve", { reviewer: approver.value }, "Human approval recorded");
  } }, heading("Human approval"),
  text("Approval is separate from the creative review and binds to the current revision and export hashes.", "small muted"),
  project.approval && chip(project.approval.reviewer ? `Approved by ${project.approval.reviewer}` : "Approved revision", "good"),
  field("Human approver", approver),
  div("row", button("Approve current exports", null, { kind: "primary", type: "submit", disabled: review?.verdict !== "pass" })));
  return panel(heading("Creative review", review ? chip(review.verdict === "pass" ? "Pass" : "Needs changes", review.verdict === "pass" ? "good" : "warning") : chip("Pending")),
    issues(),
    review && div("notice", element("strong", {}, review.reviewer), text(review.notes, "small"),
      review.scores && text(Object.entries(review.scores).map(([name, score]) => `${rubric[name] || name} ${score}`).join(" · "), "small")),
    form, approvalForm,
  );
}

function findingPanel() {
  const time = input("0", { type: "number", min: "0", step: ".001", required: true });
  const note = multiline("", { required: true, maxlength: "1000" });
  const findings = asItems(project.findings);
  const form = element("form", { className: "stack", onsubmit: (event) => {
    event.preventDefault();
    mutate("finding", { time: number(time), text: note.value }, "Finding added");
  } }, div("form-grid", field("Finding time (seconds)", time), field("Finding note", note, true)),
  div("row", button("Add finding", null, { type: "submit" })));
  return panel(heading("Timecoded findings", chip(`${findings.length}`)),
    findings.length ? list("findings", findings.map((finding) => element("li", { className: "finding-row" },
      chip(`${Number(finding.time ?? finding.timeMs / 1000).toFixed(3)} s`), text(finding.text || finding.note, "small"))))
      : text("Record specific observations while watching the cuts.", "small muted"),
    form,
  );
}

function reviewView() {
  return [pageHeader("review", chip(`Review revision ${project.revision}`),
    "Watch the three cuts, inspect proof and safe zones, and record independent findings.", renderAction()),
  div("workspace-columns review-columns", reviewMonitor(), div("stack", reviewForm(), findingPanel()))];
}

function fileList(files, state) {
  return files.length ? list("file-list", files.map((name) => element("li", { className: "file-row" },
    div("row", link(name, fileURL(name), "", true), chip(state)),
  ))) : text("No files generated for this revision.", "small muted");
}

function deliveryView() {
  const ready = Boolean(project.approval?.kind === "human" && project.review?.verdict === "pass" && project.render?.verified && !project.demo);
  const releaseFile = project.release?.file;
  return [pageHeader("delivery", chip(ready ? "Release gate passed" : "Release gate locked", ready ? "good" : "warning"),
    "Download working reports or package the reviewed and approved exports."),
  div("workspace-columns", div("stack",
    panel(heading("Super Ads Report", chip("Draft")),
      text("Create the report from the current campaign state. Use it to review the treatment, storyboard, evidence, and status.", "small muted"),
      fileList(asFiles(project.report), "Draft"),
      div("row", button("Generate draft report", () => mutate("report", {}, "Draft report generated")))),
    panel(heading("Rendered files", project.render?.verified ? chip("Media verified", "good") : null),
      fileList(asFiles(project.render), project.render?.verified ? "Verified media" : "Draft"),
      div("row", renderAction()))),
  div("stack", panel(heading("Verified bundle"),
    text("The release check requires verified renders, a passing creative review, and human approval for the same revision.", "small muted"),
    issues(),
    releaseFile && fileList([releaseFile], project.demo ? "Fictional QA bundle" : "Verified"),
    div("row", button("Build verified bundle", () => mutate("delivery", {}, "Verified bundle built"), { kind: "primary", disabled: !ready })),
    project.demo && text("The fictional campaign can exercise approvals locally. Its files are demo evidence.", "small muted")),
    metricsPanel()))];
}

function metricsPanel() {
  const metrics = asItems(project.metrics);
  const metricName = input("", { required: true, maxlength: "100" });
  const value = input("", { type: "number", min: "0", step: "any", required: true });
  const sample = input("", { type: "number", min: "1", step: "1", required: true });
  const form = element("form", { className: "stack", onsubmit: (event) => {
    event.preventDefault();
    mutate("metrics", { metrics: [...metrics, { name: metricName.value, value: number(value), sample: number(sample) }] },
      "Observed metric added");
  } }, div("form-grid", field("Metric name", metricName, true), field("Value", value), field("Sample size", sample)),
  div("row", button("Add measured result", null, { type: "submit", disabled: metrics.length >= 12 })));
  return panel(heading("Measured results"),
    metrics.length ? list("findings", metrics.map((metric) => element("li", { className: "finding-row" },
      element("strong", {}, metric.name), text(`${metric.value} · sample ${metric.sample}`, "small muted"))))
      : text("No observed results recorded.", "small muted"),
    !project.demo && project.approval ? form : text("Record results after an approved campaign has real data.", "small muted"));
}

function renderWorkspace() {
  updateRail();
  if (!project) {
    viewRoot.replaceChildren(div("empty-workspace stack",
      text("Super Ads Studio · Local-first", "eyebrow"),
      element("h1", { id: "page-title", tabindex: "-1" }, "Produce the next cut."),
      text("Move a brief through strategy, storyboard, review, and delivery in one workspace. Start a campaign or open Quiet Hours, the fictional sample.", "muted"),
      div("row", button("Load fictional campaign", loadDemo, { kind: "primary" }),
        button("New campaign", () => byId("new-dialog").showModal())),
    ));
    return;
  }
  const views = { brief: briefView, storyboard: storyboardView, review: reviewView, delivery: deliveryView };
  viewRoot.replaceChildren(...views[activeView]());
}

async function loadDemo() {
  if (pending) return;
  pending = true;
  setMessage("Loading the fictional campaign…");
  try {
    const existing = projects.find((entry) => entry.id === "quiet-hours");
    const next = existing ? await request(`/api/projects/${existing.id}`) : await request("/api/demo", { id: "quiet-hours" });
    activeView = "storyboard";
    syncState(next);
    setMessage();
    byId("page-title")?.focus();
  } catch (error) {
    setMessage("", error.message);
  } finally {
    pending = false;
  }
}

projectSelect.addEventListener("change", async () => {
  if (!projectSelect.value) return;
  try {
    syncState(await request(`/api/projects/${encodeURIComponent(projectSelect.value)}`));
    setMessage();
  } catch (error) {
    projectSelect.value = project?.id || "";
    setMessage("", error.message);
  }
});
for (const item of nav) item.addEventListener("click", () => openView(item.dataset.view));
byId("load-demo").addEventListener("click", loadDemo);
byId("new-project").addEventListener("click", () => byId("new-dialog").showModal());
byId("close-dialog").addEventListener("click", () => byId("new-dialog").close());
byId("new-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const errorBox = byId("new-error");
  const submit = form.querySelector('[type="submit"]');
  const { id, brand, product, workflow } = Object.fromEntries(new FormData(form));
  errorBox.hidden = true;
  submit.disabled = true;
  try {
    const next = await request("/api/projects", { id, workflow, brief: { brand, product } });
    activeView = "brief";
    byId("new-dialog").close();
    form.reset();
    syncState(next);
    setMessage("Campaign created");
    byId("page-title")?.focus();
  } catch (error) {
    errorBox.textContent = error.message;
    errorBox.hidden = false;
  } finally {
    submit.disabled = false;
  }
});

async function start() {
  try {
    const result = await request("/api/projects");
    projects = Array.isArray(result) ? result : result.projects;
    const last = localStorage.getItem("super-ads-project");
    const id = projects.find((entry) => entry.id === last)?.id || projects[0]?.id;
    if (id) syncState(await request(`/api/projects/${encodeURIComponent(id)}`));
    else renderWorkspace();
  } catch (error) {
    setMessage("", error.message);
    renderWorkspace();
  }
}
start();
