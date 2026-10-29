const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 675 } });
  await p.goto('file://' + process.cwd() + '/_src/kapak.html');
  await p.screenshot({ path: 'yayin/kaan-29-ekim-kapak.png' });
  await b.close();
})();
