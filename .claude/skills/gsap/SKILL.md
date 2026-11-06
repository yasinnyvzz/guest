---
name: gsap
description: GSAP (GreenSock) ile web animasyonu - timeline, ScrollTrigger, SplitText, MorphSVG, DrawSVG, Flip, metin ve SVG animasyonları; HTML sayfaları, landing page'ler ve Hyperframes kompozisyonları için hareket tasarımı yaparken kullan. Kaynak - github.com/greensock/GSAP.
---

# GSAP

Tüm GSAP eklentileri (SplitText, MorphSVG, ScrollSmoother, DrawSVG dahil) artık ücretsiz ve `gsap` npm paketinde.

## Kurulum

```bash
npm install gsap
```
```js
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { SplitText } from "gsap/SplitText";
gsap.registerPlugin(ScrollTrigger, SplitText);
```
CDN (tek HTML dosyası için): `https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js` ve `.../dist/ScrollTrigger.min.js`. Versiyonu sabitle.

## Temel kalıplar

```js
gsap.to(".kutu", { x: 200, rotation: 90, duration: 1, ease: "power3.out" });
gsap.from(".kart", { y: 40, opacity: 0, stagger: 0.08, duration: 0.6, ease: "power2.out" });
gsap.fromTo(".bar", { scaleX: 0 }, { scaleX: 1, transformOrigin: "left", duration: 0.8 });

// Timeline: sıralı sahne
const tl = gsap.timeline({ defaults: { ease: "power3.out", duration: 0.6 } });
tl.from(".baslik", { y: 60, opacity: 0 })
  .from(".alt", { y: 20, opacity: 0 }, "-=0.3")     // öncekiyle 0.3 sn çakışsın
  .to(".logo", { scale: 1.1, yoyo: true, repeat: 1 }, "<"); // öncekiyle aynı anda

// Kelime kelime metin
const split = SplitText.create(".manset", { type: "words,chars" });
gsap.from(split.chars, { yPercent: 100, opacity: 0, stagger: 0.02 });

// Scroll ile
gsap.to(".panel", { xPercent: -100, scrollTrigger: { trigger: ".wrap", start: "top top", end: "+=1000", scrub: true, pin: true } });
```

## Kurallar

- `transform` ve `opacity` animasyon et (x, y, scale, rotation); `top/left/width` animasyonu takılma yapar.
- Easing: girişler `power3.out`/`expo.out`, çıkışlar `power2.in`; doğrusal (`none`) sadece sürekli döngülerde.
- React'te `@gsap/react` paketindeki `useGSAP()` hook'unu kullan (otomatik temizlik).
- `prefers-reduced-motion` için `gsap.matchMedia()` ile azaltılmış sürüm sun.
- Video render'ı (Hyperframes) için timeline'ı `paused: true` oluştur; zamanı render motoru kontrol eder (bkz. `hyperframes` skill'i). Remotion'da GSAP yerine `interpolate`/`spring` tercih et (bkz. `remotion-best-practices`).

Belgeler: https://gsap.com/docs/v3/
