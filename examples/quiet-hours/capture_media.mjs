import {existsSync, readFileSync, writeFileSync} from "node:fs";
import {chromium} from "playwright";

const input = JSON.parse(readFileSync(process.argv[2], "utf8"));
const systemChrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const executablePath = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE || (
  !existsSync(chromium.executablePath()) && existsSync(systemChrome) ? systemChrome : undefined
);
const browser = await chromium.launch({
  headless: true,
  executablePath,
  args: ["--autoplay-policy=no-user-gesture-required"],
});
const observations = [];
try {
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.route("**/*", route => (
    route.request().url().startsWith(input.origin + "/") ? route.continue() : route.abort()
  ));
  for (const frame of input.frames) {
    await page.setViewportSize({width: frame.width, height: frame.height});
    const response = await page.goto(input.origin + frame.route);
    if (!response?.ok()) throw new Error("Preview request failed");
    await page.evaluate(() => document.fonts.ready);
    const media = page.locator("video");
    if (await media.count()) {
      await page.waitForFunction(() => {
        const video = document.querySelector("video");
        return video.readyState >= 2 && !video.seeking && video.videoWidth > 0;
      }, undefined, {timeout: 7000});
    }
    await page.screenshot({path: frame.file});
  }
  for (const clip of input.clips) {
    const response = await page.goto(input.origin + clip.route);
    if (!response?.ok()) throw new Error("Export video request failed");
    const result = await page.locator("video").evaluate(async video => {
      async function seek(time) {
        const ready = new Promise(resolve => video.addEventListener("seeked", resolve, {once: true}));
        video.currentTime = time;
        await ready;
        return video.currentTime;
      }
      if (video.readyState < 1) {
        await new Promise(resolve => video.addEventListener("loadedmetadata", resolve, {once: true}));
      }
      const middle = await seek(video.duration / 2);
      await seek(0);
      video.playbackRate = 2;
      video.muted = false;
      const ended = new Promise(resolve => video.addEventListener("ended", resolve, {once: true}));
      await video.play();
      await ended;
      const playedWithSoundEnabled = !video.muted && video.ended;
      await seek(0);
      video.muted = true;
      const mutedEnded = new Promise(resolve => video.addEventListener("ended", resolve, {once: true}));
      await video.play();
      await mutedEnded;
      return {
        duration: video.duration,
        midpointSeek: middle,
        playedWithSoundEnabled,
        playedMuted: video.muted && video.ended,
      };
    }, null, {timeout: 25000});
    observations.push({format: clip.format, ...result});
  }
  writeFileSync(input.result, JSON.stringify(observations));
} finally {
  await browser.close();
}
