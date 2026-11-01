const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport:{width:1080,height:1440} });
await p.goto('file://' + process.cwd() + '/seri.html'); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(800);
const n=['1-kapak', '2-15-11', '3-10-6', '4-redback', '5-lynx-kf41', '6-m2a4-bradley', '7-tulpar-s', '8-zirve', '9-uygulama']; for (let i=0;i<n.length;i++) await (await p.$('#s'+(i+1))).screenshot({path:'seri/'+n[i]+'.png'}); await b.close(); })();