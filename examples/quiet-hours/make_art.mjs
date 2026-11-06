import {existsSync, readFileSync} from "node:fs";
import {join} from "node:path";
import {chromium} from "playwright";

const [root, manifest] = process.argv.slice(2);
const systemChrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const configured = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE;
const executablePath = configured || (
  !existsSync(chromium.executablePath()) && existsSync(systemChrome) ? systemChrome : undefined
);
const browser = await chromium.launch({headless: true, executablePath});
try {
  const page = await browser.newPage({viewport: {width: 760, height: 560}});
  for (const [name, svg] of Object.entries(JSON.parse(readFileSync(manifest, "utf8")))) {
    await page.setContent(`<!doctype html><style>html,body{margin:0}svg{display:block}</style>${svg}`);
    await page.screenshot({path: join(root, name), omitBackground: true});
  }
} finally {
  await browser.close();
}
