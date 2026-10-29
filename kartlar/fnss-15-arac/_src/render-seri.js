const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  await p.goto('file://' + process.cwd() + '/seri.html');
  await p.waitForTimeout(800);
  const names = ['1-kapak','2-pars','3-yeni-nesil-tekerlekli','4-paletli','5-kaplan','6-amfibi-istihkam','7-uygulama'];
  for (let i = 0; i < names.length; i++) await (await p.$('#s' + (i + 1))).screenshot({ path: 'seri/' + names[i] + '.png' });
  await b.close();
})();
