const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  await p.goto('file://' + process.cwd() + '/kaan-29-ekim.html');
  await p.waitForTimeout(500);
  await p.screenshot({ path: 'kaan-29-ekim.png' });
  await b.close();
})();
