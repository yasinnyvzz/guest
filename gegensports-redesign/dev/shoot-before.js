const { chromium } = require('playwright');
const out = '/home/user/guest/gegensports-redesign/audit/before';
const pages = {
 home:'/', article:'/nico-paz-kimdir/', scout_report:'/mahmut-sarihasan-diyarbekir-spor-scout-raporu/',
 scout_hub:'/scout', talent_hub:'/genc-yetenek-hub/', league:'/category/super-lig/', home_en:'/en/',
 search:'/?s=stoper', author:'/author/aliucpunar/', ranking_like:'/fm27-yeni-genc-yetenekler-gegensports-puan-tablosu/'
};
const vps = {desktop:{width:1440,height:900}, mobile:{width:390,height:844}};
(async()=>{
 const b = await chromium.launch();
 const report = {};
 for (const [vn,vp] of Object.entries(vps)) {
  const ctx = await b.newContext({viewport:vp, deviceScaleFactor:1, isMobile: vn==='mobile', userAgent: vn==='mobile'?'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148':undefined});
  for (const [n,p] of Object.entries(pages)) {
   const pg = await ctx.newPage();
   try {
    const t0=Date.now();
    const resp = await pg.goto('https://gegensports.com'+p,{waitUntil:'load',timeout:45000});
    await pg.waitForTimeout(2500);
    const m = await pg.evaluate(()=>{
      const txt=document.body.innerText;
      const cs=getComputedStyle(document.body);
      const colors=new Set(); const fonts=new Set(); const sizes=new Set();
      document.querySelectorAll('body *').forEach(e=>{const s=getComputedStyle(e); if(s.backgroundColor!=='rgba(0, 0, 0, 0)')colors.add(s.backgroundColor); fonts.add(s.fontFamily.split(',')[0].trim()); if(e.childNodes.length&&[...e.childNodes].some(c=>c.nodeType===3&&c.textContent.trim()))sizes.add(s.fontSize);});
      return {title:document.title,h1:[...document.querySelectorAll('h1')].map(h=>h.innerText.trim().slice(0,90)),
        bgColors:colors.size, fonts:[...fonts].slice(0,8), fontSizes:sizes.size,
        ozet:/Özet Bulunamad/i.test(txt), navLinks:document.querySelectorAll('header a, nav a').length,
        imgs:document.images.length, scrollW:document.documentElement.scrollWidth, innerW:innerWidth,
        height:document.documentElement.scrollHeight, bodyBg:cs.backgroundColor, bodyFont:cs.fontFamily.slice(0,60),
        scripts:document.scripts.length, h2:document.querySelectorAll('h2').length, zero:(txt.match(/\b0\.0\b/g)||[]).length};
    });
    m.status=resp.status(); m.ms=Date.now()-t0;
    report[vn+'_'+n]=m;
    await pg.screenshot({path:`${out}/${vn}-${n}.png`, fullPage:false});
    if(n==='home') await pg.screenshot({path:`${out}/${vn}-${n}-full.png`, fullPage:true});
   } catch(e){ report[vn+'_'+n]={error:String(e).slice(0,120)}; }
   await pg.close();
  }
  await ctx.close();
 }
 require('fs').writeFileSync(out+'/metrics.json',JSON.stringify(report,null,1));
 await b.close();
})();
