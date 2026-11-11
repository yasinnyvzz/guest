const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const out={};
for(const [n,u] of [['before_home','https://gegensports.com/'],['before_article','https://gegensports.com/nico-paz-kimdir/'],['after_home','http://localhost:8080/'],['after_article','http://localhost:8080/nico-paz-kimdir/']]){
 const ctx=await b.newContext({viewport:{width:390,height:844},isMobile:true});const pg=await ctx.newPage();let reqs=0,bytes=0,js=0,css=0;
 pg.on('response',async r=>{reqs++;try{const l=+(r.headers()['content-length']||0);bytes+=l;const t=r.headers()['content-type']||'';if(t.includes('javascript'))js++;if(t.includes('css'))css++}catch{}});
 await pg.addInitScript(()=>{window.__cls=0;window.__lcp=0;new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)window.__cls+=e.value}).observe({type:'layout-shift',buffered:true});new PerformanceObserver(l=>{const e=l.getEntries();window.__lcp=e[e.length-1].startTime}).observe({type:'largest-contentful-paint',buffered:true})});
 await pg.goto(u,{waitUntil:'networkidle',timeout:90000}).catch(()=>{});await pg.waitForTimeout(1500);
 const m=await pg.evaluate(()=>({lcp:Math.round(window.__lcp),cls:+window.__cls.toFixed(3),scripts:document.scripts.length,dom:document.getElementsByTagName('*').length}));
 out[n]={...m,requests:reqs,jsFiles:js,cssFiles:css,declaredKB:Math.round(bytes/1024)};await ctx.close()}
console.log(JSON.stringify(out,null,1));await b.close()})();
