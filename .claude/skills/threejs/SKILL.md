---
name: threejs
description: three.js ile tarayıcıda 3D sahne, model (GLB/GLTF) gösterme, 3D ürün/uçak/araç görselleştirme, parçacık efekti, shader ve WebGL animasyonu yaparken kullan; React'te @react-three/fiber, Remotion'da @remotion/three ile. Kaynak - github.com/mrdoob/three.js.
---

# three.js

## Kurulum

```bash
npm install three
```
Tek HTML dosyasında import map kullan (versiyonu sabitle):
```html
<script type="importmap">
{ "imports": {
  "three": "https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js",
  "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/"
} }
</script>
```

## Asgari sahne

```js
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.setSize(innerWidth, innerHeight);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment()).texture;  // gerçekçi yansıma

const camera = new THREE.PerspectiveCamera(45, innerWidth / innerHeight, 0.1, 1000);
camera.position.set(3, 2, 5);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

new GLTFLoader().load("model.glb", (g) => {
  const box = new THREE.Box3().setFromObject(g.scene);
  g.scene.position.sub(box.getCenter(new THREE.Vector3()));   // modeli ortala
  scene.add(g.scene);
});

addEventListener("resize", () => {
  camera.aspect = innerWidth / innerHeight; camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
});
renderer.setAnimationLoop(() => { controls.update(); renderer.render(scene, camera); });
```

## Kurallar

- Model yoksa: Blender'da üret ve GLB dışa aktar (bkz. `blender` skill'i), ya da basit geometrilerle kur. Gerçek ürün modellerini telifli kaynaklardan kopyalama.
- Büyük GLB'leri `gltf-transform optimize in.glb out.glb --compress draco` ile küçült; `DRACOLoader` ekle.
- Renk yönetimi: dokular `texture.colorSpace = THREE.SRGBColorSpace`.
- Geometri/materyal/dokuları kullanılmayınca `dispose()` et.
- Video için: Remotion'da `@remotion/three` (`<ThreeCanvas>`) kullan, zamanı `useCurrentFrame()`'den al, `setAnimationLoop` kullanma (bkz. `remotion-best-practices`).
- Sonucu tarayıcıda açıp ekran görüntüsüyle kontrol et (Playwright veya `chrome-devtools` skill'i).

Belgeler: https://threejs.org/docs/ — örnekler: https://threejs.org/examples/
