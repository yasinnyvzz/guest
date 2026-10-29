const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  await p.goto('file://' + process.cwd() + '/seri.html');
  await p.waitForTimeout(600);
  const names = ['1-kapak','2-kravat','3-sarki','4-uyari','5-sonraki-ucus'];
  for (let i = 0; i < 5; i++) await (await p.$('#s' + (i + 1))).screenshot({ path: 'seri/' + names[i] + '.png' });
  await b.close();
})();
