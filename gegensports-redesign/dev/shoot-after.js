const { chromium } = require('playwright');
const out='/home/user/guest/gegensports-redesign/audit/after';
const pages={home:'/',article:'/nico-paz-kimdir/',scout_center:'/gegen-scout/',dossier:'/dossier/emirhan-acar-firatvarol-11-11-2026/',rankings:'/test-gegen-rankings-stoper/',team_league:'/category/super-lig/',home_en:'/en/',search:'/?s=stoper',news:'/haberler/',dossier_index:'/dossier/'};
const vps={'1440':[1440,900],'1280':[1280,800],'768':[768,1024],'390':[390,844],'360':[360,740]};
(async()=>{const b=await chromium.launch();const rep={};
for(const [vn,[w,h]] of Object.entries(vps)){const ctx=await b.newContext({viewport:{width:w,height:h},deviceScaleFactor:1,isMobile:w<500});
 for(const [n,p] of Object.entries(pages)){const pg=await ctx.newPage();
  try{await pg.goto('http://localhost:8080'+p,{waitUntil:'load',timeout:60000});await pg.waitForTimeout(800);
   const m=await pg.evaluate(()=>({overflowX:document.documentElement.scrollWidth>innerWidth,sw:document.documentElement.scrollWidth,h1:document.querySelectorAll('h1').length,title:document.title,h:document.documentElement.scrollHeight,
     small:[...document.querySelectorAll('a,button')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&r.height<32&&getComputedStyle(e).display!=='inline'&&!e.closest('.prose')&&!e.closest('.breadcrumbs')}).length,
     bad:/özet bulunamad|undefined|\(\)/i.test(document.body.innerText)}));
   rep[vn+'_'+n]=m;await pg.screenshot({path:out+'/'+vn+'-'+n+'.png'});
   if(vn==='1440'||vn==='390')await pg.screenshot({path:out+'/'+vn+'-'+n+'-full.png',fullPage:true});
  }catch(e){rep[vn+'_'+n]={error:String(e).slice(0,100)}}await pg.close();}
 await ctx.close();}
require('fs').writeFileSync(out+'/metrics.json',JSON.stringify(rep,null,1));await b.close();})();
