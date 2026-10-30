const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport:{width:1080,height:1350} });
await p.goto('file://' + process.cwd() + '/seri-uzun.html'); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(700);
const n=['1-kapak', '2-alinti', '3-alinti', '4-alinti', '5-alinti', '6-alinti', '7-alinti', '8-alinti', '9-uygulama']; for (let i=0;i<n.length;i++) await (await p.$('#s'+(i+1))).screenshot({path:'seri-uzun/'+n[i]+'.png'}); await b.close(); })();