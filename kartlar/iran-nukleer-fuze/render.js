const {chromium}=require('playwright');
(async()=>{
 const b=await chromium.launch(); const pg=await b.newPage({viewport:{width:1080,height:1350}});
 await pg.goto('file://'+__dirname+'/seri.html'); await pg.waitForTimeout(800);
 const names=['1-kapak','2-iki-program','3-uranyum','4-fuze-sayisi','5-menzil','6-baslik','7-ozet','8-uygulama'];
 for(let i=1;i<=8;i++) await pg.locator('#s'+i).screenshot({path:__dirname+'/'+names[i-1]+'.png'});
 await b.close();
})();
