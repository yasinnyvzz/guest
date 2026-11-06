import math, sys
from PIL import Image, ImageDraw, ImageFont
S=2  # supersample
W,H=1600*S,1600*S
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; REG="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
GOLD,N1,N2,WHITE,GRID,STEEL,STEEL2,GROOVE=(201,162,74),(11,22,42),(22,36,60),(240,244,252),(24,38,62),(120,134,156),(78,92,116),(214,180,98)
im=Image.new("RGB",(W,H),N1); d=ImageDraw.Draw(im)
for y in range(H):
    k=y/H; d.line([(0,y),(W,y)],fill=tuple(int(N1[i]+(N2[i]-N1[i])*k) for i in range(3)))
for x in range(0,W,80*S): d.line([(x,0),(x,H)],fill=GRID)
for y in range(0,H,80*S): d.line([(0,y),(W,y)],fill=GRID)
d.rectangle([0,0,W,12*S],fill=GOLD)
f=lambda p,s: ImageFont.truetype(p,s*S)
d.text((W/2,120*S),"SAVUNMA SÖZLÜĞÜ",font=f(BOLD,30),fill=GOLD,anchor="mm")
d.rectangle([W/2-60*S,150*S,W/2+60*S,155*S],fill=GOLD)
d.text((W/2,240*S),"HATVE",font=f(BOLD,110),fill=WHITE,anchor="mm")
d.text((W/2,340*S),"Merminin namlu içinde bir tam tur",font=f(REG,40),fill=WHITE,anchor="mm")
d.text((W/2,392*S),"dönerek katettiği yol",font=f(REG,40),fill=WHITE,anchor="mm")
# barrel side cutaway
x0,x1,cy,r=110*S,1490*S,700*S,110*S
d.rounded_rectangle([x0,cy-r-34*S,x1,cy+r+34*S],radius=20*S,fill=STEEL2)
d.rectangle([x0,cy-r,x1,cy+r],fill=(30,44,70))
P=520*S  # pitch length in px
xs=x0+150*S
# helical grooves (projected), back half dim, front half bright
for g in range(4):
    ph=g*math.pi/2
    pts=[]
    for x in range(x0,x1,2*S):
        a=2*math.pi*(x-xs)/P+ph
        pts.append((x,cy+r*math.sin(a),math.cos(a)))
    for i in range(len(pts)-1):
        (xa,ya,za),(xb,yb,zb)=pts[i],pts[i+1]
        if za>0: d.line([(xa,ya),(xb,yb)],fill=GROOVE,width=7*S)
        else: d.line([(xa,ya),(xb,yb)],fill=(70,84,110),width=4*S)
# bullet at left
bx=x0+40*S
d.rectangle([bx,cy-70*S,bx+120*S,cy+70*S],fill=(184,115,51))
d.pieslice([bx+40*S,cy-70*S,bx+200*S,cy+70*S],-90,90,fill=(184,115,51))
d.line([(bx+20*S,cy-70*S),(bx+20*S,cy+70*S)],fill=(150,90,40),width=4*S)
# highlight one groove start/end markers & dimension
gx0=xs+P*0.25; gx1=gx0+P
for gx in (gx0,gx1):
    d.ellipse([gx-14*S,cy+r-14*S,gx+14*S,cy+r+14*S],fill=WHITE,outline=GOLD,width=4*S)
    d.line([(gx,cy+r+40*S),(gx,cy+r+150*S)],fill=GOLD,width=4*S)
ay=cy+r+110*S
d.line([(gx0,ay),(gx1,ay)],fill=GOLD,width=5*S)
for gx,s in ((gx0,1),(gx1,-1)):
    d.polygon([(gx,ay),(gx+s*30*S,ay-15*S),(gx+s*30*S,ay+15*S)],fill=GOLD)
d.text(((gx0+gx1)/2,ay+70*S),"HATVE = 1 TAM TUR (360°)",font=f(BOLD,36),fill=GOLD,anchor="mm")
d.text((x0+10*S,cy-r-70*S),"Namlu (yandan kesit) — yiv ve setler sarmal açılır",font=f(REG,30),fill=WHITE,anchor="ls")
# muzzle end view
ex,ey,R=420*S,1220*S,150*S
d.ellipse([ex-R-30*S,ey-R-30*S,ex+R+30*S,ey+R+30*S],fill=STEEL2)
d.ellipse([ex-R,ey-R,ex+R,ey+R],fill=(30,44,70))
for k in range(4):
    a0=k*90-15; d.pieslice([ex-R,ey-R,ex+R,ey+R],a0,a0+30,fill=GROOVE)
d.ellipse([ex-R+26*S,ey-R+26*S,ex+R-26*S,ey+R-26*S],fill=(30,44,70))
d.arc([ex-R-60*S,ey-R-60*S,ex+R+60*S,ey+R+60*S],200,330,fill=WHITE,width=6*S)
a=math.radians(330); tx,ty=ex+(R+60*S)*math.cos(a),ey+(R+60*S)*math.sin(a)
d.polygon([(tx+18*S,ty+12*S),(tx-22*S,ty-4*S),(tx+4*S,ty-30*S)],fill=WHITE)
d.text((ex,ey+R+80*S),"Namlu ağzı: 4 yiv",font=f(REG,30),fill=WHITE,anchor="mm")
# example box
bx0,by0=700*S,1080*S
d.rounded_rectangle([bx0,by0,1490*S,1380*S],radius=18*S,outline=GOLD,width=4*S,fill=(16,28,50))
lines=[("ÖRNEK",BOLD,30,GOLD),("Hatve 1:7\" (178 mm)",BOLD,40,WHITE),("Mermi namluda her 7 inçte",REG,30,WHITE),("bir tam tur döner.",REG,30,WHITE),("Kısa hatve = daha hızlı dönüş",REG,30,(190,200,220))]
y=by0+50*S
for t,fp,s,c in lines:
    d.text((bx0+40*S,y),t,font=f(fp,s),fill=c,anchor="lm"); y+=s*S*1.55
d.text((W/2,1530*S),"ENVANTER MEDYA",font=f(BOLD,30),fill=GOLD,anchor="mm")
im=im.resize((1600,1600),Image.LANCZOS)
im.save(sys.argv[1],quality=90)
