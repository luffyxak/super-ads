import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { createHash } from "node:crypto";
import { access, mkdtemp, mkdir, readFile, rm } from "node:fs/promises";
import { createServer } from "node:net";
import { tmpdir } from "node:os";
import { resolve } from "node:path";
import { setTimeout as delay } from "node:timers/promises";
import { chromium } from "playwright";

const macChrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const executablePath = process.env.STUDIO_TEST_CHROME
  || await access(macChrome).then(() => macChrome, () => undefined);
const output = resolve(process.env.STUDIO_BROWSER_EVIDENCE || "outputs/browser-evidence");
const data = await mkdtemp(resolve(tmpdir(), "super-ads-browser-"));
const remote = process.env.STUDIO_TEST_URL;
const reviewURL = process.env.STUDIO_REVIEW_URL;
let server;
let browser;

async function localURL() {
  const socket = createServer();
  const port = await new Promise((accept, reject) => {
    socket.once("error", reject);
    socket.listen(0, "127.0.0.1", () => accept(socket.address().port));
  });
  await new Promise((accept) => socket.close(accept));
  server = spawn(process.env.STUDIO_TEST_PYTHON || "python3", [
    "-m", "studio", "--data", data, "serve", "--port", String(port),
  ], { stdio: ["ignore", "inherit", "inherit"] });
  const url = `http://127.0.0.1:${port}`;
  for (let n = 0; n < 100; n++) {
    const ready = await fetch(`${url}/api/projects`).then(r => r.ok, () => false);
    if (ready) return url;
    if (server.exitCode !== null) break;
    await delay(100);
  }
  throw new Error("Studio server never became ready");
}

async function exerciseStudio(url) {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  page.setDefaultTimeout(8000);
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  const failedRequests = [];
  page.on("requestfailed", async (request) => failedRequests.push([request.url(), request.failure()?.errorText, await request.allHeaders()]));

  await page.goto(url);
  assert.match(await page.title(), /Super Ads Studio/);
  await page.keyboard.press("Tab");
  assert.equal(await page.evaluate(() => document.activeElement.textContent), "Skip to workspace");
  await page.keyboard.press("Enter");
  assert.equal(await page.evaluate(() => document.activeElement.id), "workspace");

  await page.getByRole("button", { name: "Load fictional campaign" }).first().click();
  await page.getByRole("heading", { name: "Storyboard & timeline" }).waitFor();
  await page.getByRole("main").getByText("Fictional fixture", { exact: true }).waitFor();
  const projectId = await page.getByLabel("Campaign", { exact: true }).inputValue();
  assert.ok(projectId);
  const state = () => page.request.get(`${url}/api/projects/${projectId}`).then(r => r.json());
  const initial = await state();
  assert.ok(initial.shots.length >= 2);
  await page.getByRole("heading", { name: "Concept board" }).waitFor();
  await page.getByLabel("Preview hook").selectOption(initial.hooks[1].id);
  await page.getByLabel("Timestamp (seconds)").fill("1.200");
  await page.getByRole("button", { name: "Seek", exact: true }).click();
  const preview = page.getByTitle("Storyboard preview", { exact: true });
  const previewURL = new URL(await preview.getAttribute("src"), url);
  assert.equal(Number(previewURL.searchParams.get("time")), 1.2);
  assert.equal(previewURL.searchParams.get("hook"), initial.hooks[1].id);
  assert.ok((await page.request.get(previewURL.href)).ok());
  await preview.contentFrame().locator("body").waitFor();
  await page.getByLabel("Show safe zones").check();
  assert.equal(await page.locator(".safe-overlay").isVisible(), true);
  await page.screenshot({ path: resolve(output, "storyboard-desktop.png") });

  const externalShot = initial.shots.find((shot) => shot.reference);
  assert.ok(externalShot);
  await page.getByRole("button", { name: new RegExp(externalShot.title, "i") }).click();
  await page.getByText("Planning only", { exact: true }).waitFor();
  const importedClip = preview.contentFrame().locator("video");
  await importedClip.waitFor({ state: "attached" });
  const clipFrame = page.frames().find((frame) => frame.url().includes("time=8.000"));
  assert.ok(clipFrame);
  try {
    await clipFrame.waitForFunction(() => document.querySelector("video")?.readyState >= 2, null, { timeout: 5000 });
  } catch (error) {
    console.error("Storyboard clip failed to decode", failedRequests);
    throw error;
  }
  const reference = page.waitForEvent("download");
  await page.getByRole("link", { name: "Export shot reference" }).click();
  const referenceDownload = await reference;
  const handoff = await readFile(await referenceDownload.path(), "utf8");
  assert.match(handoff, /<!doctype html>/i);
  assert.ok(handoff.includes("data:image/"), "Shot handoff embeds the planning reference");
  const localReference = initial.assets.find((asset) => asset.id === externalShot.reference);
  const localBytes = await page.request.get(`${url}/api/projects/${projectId}/assets/${localReference.id}`);
  assert.ok(localBytes.ok());
  await page.getByText("Import an asset", { exact: true }).click();
  await page.getByLabel("Asset file").setInputFiles({
    name: "browser-import-reference.png", mimeType: "image/png", buffer: await localBytes.body(),
  });
  await page.getByLabel("Source / provenance").fill("Original local fictional demo artwork");
  await page.getByLabel("Rights record").fill("Original Quiet Hours demo asset, MIT.");
  await page.getByRole("button", { name: "Import asset" }).click();
  await page.getByText("Asset imported", { exact: true }).waitFor();
  assert.ok((await state()).assets.some((asset) => asset.name === "browser-import-reference.png"));
  const packshot = initial.assets.find((asset) => asset.role === "packshot");
  const packshotShot = initial.shots.find((shot) => shot.asset === packshot.id);
  await page.getByRole("button", { name: new RegExp(packshotShot.title, "i") }).click();
  const placedImage = preview.contentFrame().locator("img.placed-image");
  await placedImage.waitFor();
  assert.ok(await placedImage.evaluate((image) => image.complete && image.naturalWidth > 0), "Packshot decoded in the iframe");

  await page.locator(".shot-card").first().click();
  await page.getByLabel("Shot title").fill("Retake the opening");
  await page.getByLabel("Caption", { exact: true }).fill("An eviction notice for keys.");
  await page.getByRole("button", { name: "Save storyboard" }).click();
  await page.getByText("Storyboard saved", { exact: true }).waitFor();
  assert.equal((await state()).shots[0].title, "Retake the opening");
  assert.equal((await state()).shots[0].caption, "An eviction notice for keys.");

  await page.getByRole("button", { name: "Brief & brand" }).click();
  await page.getByLabel("Audience", { exact: true }).fill("");
  await page.getByRole("button", { name: "Save brief" }).click();
  await page.getByText("Brief saved", { exact: true }).waitFor();
  await page.getByRole("button", { name: "Storyboard", exact: true }).click();
  await page.getByRole("button", { name: "Commit handoff" }).click();
  await page.getByRole("alert").waitFor();
  await page.getByRole("button", { name: "Brief & brand" }).click();
  await page.getByLabel("Audience", { exact: true }).fill("Independent studio reviewers");
  await page.getByRole("button", { name: "Save brief" }).click();
  await page.getByText("Brief saved", { exact: true }).waitFor();
  await page.reload();
  await page.getByRole("button", { name: "Brief & brand" }).click();
  assert.equal(await page.getByLabel("Audience", { exact: true }).inputValue(), "Independent studio reviewers");
  await page.getByRole("button", { name: "Storyboard", exact: true }).click();
  await page.getByLabel("Handoff summary").fill("Make a small desk grievance feel larger than life.");
  await page.getByLabel("Handoff items").fill("Show the illustrated desk mat as the story turns.");
  await page.getByRole("button", { name: "Commit handoff" }).click();
  await page.getByText("Handoff committed", { exact: true }).waitFor();
  assert.equal((await state()).nextStage, "concept");

  await page.getByRole("button", { name: "Review", exact: true }).click();
  await page.getByLabel("Finding time (seconds)").fill("1.2");
  await page.getByLabel("Finding note").fill("Hold the opening long enough to read.");
  await page.getByRole("button", { name: "Add finding" }).click();
  await page.getByText("Hold the opening long enough to read.", { exact: true }).waitFor();
  await page.getByRole("button", { name: "Delivery", exact: true }).click();
  assert.equal(await page.getByRole("button", { name: "Build verified bundle" }).isDisabled(), true);
  await page.getByRole("button", { name: "Generate draft report" }).click();
  const reportLink = page.getByRole("link", { name: "super-ads-report.html" });
  await reportLink.waitFor();
  const report = page.waitForEvent("download");
  await reportLink.click();
  const reportDownload = await report;
  assert.match(await readFile(await reportDownload.path(), "utf8"), /Super Ads Report/i);

  await page.setViewportSize({ width: 390, height: 844 });
  await page.getByRole("button", { name: "Storyboard", exact: true }).click();
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
  await page.screenshot({ path: resolve(output, "storyboard-mobile.png") });
  assert.deepEqual(errors, []);
  console.log("PASS browser: keyboard, fixture, concept, seek, safe zones, visible clip and packshot, reference download, import, retake, missing input recovery, reload, manual handoff, feedback, draft download, blocked delivery, mobile");
}

async function verifyPlayback(url) {
  const id = process.env.STUDIO_REVIEW_PROJECT || "quiet-hours";
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  await page.addInitScript((projectId) => localStorage.setItem("super-ads-project", projectId), id);
  await page.goto(url);
  const response = await page.request.get(new URL(`/api/projects/${id}`, url).href);
  assert.ok(response.ok());
  const state = await response.json();
  assert.equal(state.render?.verified, true);
  await page.getByRole("button", { name: "Review", exact: true }).click();
  const results = [];
  for (const [aspect, width, height] of [["9x16", 1080, 1920], ["1x1", 1080, 1080], ["16x9", 1920, 1080]]) {
    await page.getByLabel("Review aspect ratio").selectOption(aspect);
    const player = page.getByLabel("Rendered cut");
    await player.waitFor();
    await page.waitForFunction(() => document.querySelector("video")?.readyState >= 2);
    const media = await player.evaluate(async (video) => {
      const seek = new Promise((done) => video.addEventListener("seeked", done, { once: true }));
      video.currentTime = 12.4;
      await seek;
      const at = video.currentTime;
      await video.play();
      return { width: video.videoWidth, height: video.videoHeight, duration: video.duration, at, muted: video.muted };
    });
    assert.equal(media.width, width);
    assert.equal(media.height, height);
    assert.ok(Math.abs(media.duration - 15) < 0.05);
    assert.ok(Math.abs(media.at - 12.4) < 0.05);
    assert.equal(media.muted, true);
    await page.waitForFunction(() => document.querySelector("video")?.currentTime > 12.5);
    await page.getByLabel("Mute playback").uncheck();
    assert.equal(await player.evaluate((video) => video.muted), false);
    const unmutedStart = await player.evaluate((video) => video.currentTime);
    await page.waitForFunction((time) => document.querySelector("video")?.currentTime > time + 0.1, unmutedStart);
    await player.evaluate((video) => video.pause());
    await page.getByLabel("Show safe zones").check();
    await page.screenshot({ path: resolve(output, `review-${aspect}.png`) });
    const download = page.waitForEvent("download");
    await page.getByRole("link", { name: "Download current cut" }).click();
    const file = await download;
    assert.equal(file.suggestedFilename(), `master-${aspect}.mp4`);
    const hash = createHash("sha256").update(await readFile(await file.path())).digest("hex");
    assert.equal(hash, state.render.hashes[file.suggestedFilename()]);
    results.push({ aspect, ...media, playedMuted: true, playedUnmuted: true, sha256: hash });
  }
  console.log(JSON.stringify({ project: id, revision: state.revision, browserMedia: results }, null, 2));
}

try {
  await mkdir(output, { recursive: true });
  const url = reviewURL || remote || await localURL();
  browser = await chromium.launch({ headless: true, executablePath });
  if (reviewURL) await verifyPlayback(url);
  else await exerciseStudio(url);
} finally {
  if (browser) await browser.close();
  if (server && server.exitCode === null) {
    server.kill();
    await new Promise((done) => server.once("exit", done));
  }
  await rm(data, { force: true, recursive: true });
}
