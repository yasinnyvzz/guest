const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport:{width:1080,height:1350} });
await p.goto('file://' + process.cwd() + '/seri.html'); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(700);
const n=['1-kapak', '2-cobra', '3-atak', '4-rakamlar', '5-yerlilik', '6-kullanicilar', '7-cobra-emekli-mi', '8-uygulama']; for (let i=0;i<n.length;i++) await (await p.$('#s'+(i+1))).screenshot({path:'seri/'+n[i]+'.png'}); await b.close(); })();