const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport:{width:1080,height:1440} });
await p.goto('file://' + process.cwd() + '/seri.html'); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(800);
const n=['01-kapak', '02-olcutler', '03-15-11', '04-10-6', '05-redback', '06-lynx-kf41', '07-m2a4-bradley', '08-tulpar-s', '09-zirve', '10-uygulama']; for (let i=0;i<n.length;i++) await (await p.$('#s'+(i+1))).screenshot({path:'seri/'+n[i]+'.png'}); await b.close(); })();