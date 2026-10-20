// 验证 samples 版样书：图片是否加载成功 + 首屏截图
const { chromium } = require('playwright-core');
const path = require('path');
const fs = require('fs');

const EXE = 'C:/Users/12144/AppData/Local/ms-playwright/chromium-1234/chrome-win64/chrome.exe';
const BASE = 'D:/Workspace/clean-workspace/outputs/huiben-master-v2/samples';
const OUT = path.join(BASE, '_verify');
if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });

const BOOKS = ['moonlight', 'red-riding-hood', 'ink-drop'];

(async () => {
  const browser = await chromium.launch({ executablePath: EXE });
  const page = await browser.newPage({ viewport: { width: 1100, height: 780 } });
  let bad = 0;
  for (const slug of BOOKS) {
    const file = path.join(BASE, slug, 'index.html');
    await page.goto('file:///' + file.replace(/\\/g, '/'), { waitUntil: 'load' });
    await page.waitForTimeout(1500);
    const info = await page.evaluate(() => {
      const imgs = Array.from(document.images);
      return {
        total: imgs.length,
        broken: imgs.filter(i => !i.complete || i.naturalWidth === 0).length,
        title: document.title || '',
      };
    });
    console.log(`${slug}: 图片 ${info.total} 张，失效 ${info.broken} 张`);
    if (info.broken) bad++;
    await page.screenshot({ path: path.join(OUT, slug + '.png') });
  }
  await browser.close();
  console.log(bad ? 'FAIL' : 'ALL OK');
})();
