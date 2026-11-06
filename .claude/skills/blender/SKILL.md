---
name: blender
description: Blender ile 3D modelleme, sahne kurma, materyal, ışık, kamera animasyonu ve render alırken kullan - Python (bpy) betiğiyle arka planda (blender -b) veya Blender MCP (mcp-for-blender) üzerinden canlı Blender'ı kontrol ederek. GLB dışa aktarma (three.js/Remotion için) dahil. Kaynaklar - github.com/blender/blender, github.com/ahujasid/mcp-for-blender.
---

# Blender

İki çalışma yolu var. Hangisinin mümkün olduğuna önce bak.

## Yol 1: Blender MCP (canlı, kullanıcının bilgisayarında)

`mcp__blender__*` araçları listede varsa Blender açık ve bağlıdır:

| Araç | İş |
|---|---|
| `get_addon_status` | Blender/eklenti sürümü, açık kütüphaneler |
| `get_scene_info` | Sahne özeti; değişiklikten önce mutlaka çağır |
| `execute_blender_code` | Canlı Blender'da bpy kodu çalıştır |
| `look` | Sonucu gör: `viewport`, `camera`, `angles` (çoklu açı), `frames` (animasyon şeridi), `rendered`/`wireframe` |
| `search_assets` / `import_asset` | Poly Haven (HDRI, doku, model), Sketchfab, Poly Pizza |
| `generate_3d` | Tripo/Hunyuan3D/Rodin/Meshy ile model üretip içe aktarma (API anahtarı gerekir) |

Eklenti varsayılan olarak telemetri toplar; kullanıcı isterse `disable_telemetry` ile kapat.

Kurulum (kullanıcının kendi makinesinde, bir kez):
```bash
uvx mcp-for-blender setup          # istemcileri bulur, eklentiyi kurar
# veya sadece Claude Code için:
claude mcp add blender uvx mcp-for-blender
```
Sonra Blender'ı aç; eklenti sunucusu (port 9876) Blender açılınca başlar. Aynı anda tek bir MCP istemcisi bağlansın. Bulut oturumunda Blender olmadığından bu yol çalışmaz, Yol 2'ye geç.

## Yol 2: Arka planda bpy betiği

```bash
blender -b -P sahne.py -- --out render.png       # betik çalıştır
blender -b dosya.blend -o //frames/f_#### -F PNG -a   # animasyon render
```
Blender kurulu değilse: Linux'ta `pip install bpy` (Python sürümü Blender'ın istediğiyle aynı olmalı) veya resmi tar.xz paketi.

```python
import bpy, sys, math
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
out = argv[argv.index("--out") + 1] if "--out" in argv else "/tmp/render.png"

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "CYCLES"            # hızlı önizleme: "BLENDER_EEVEE" (4.2-4.5'te "BLENDER_EEVEE_NEXT")
scene.cycles.samples = 64
scene.render.resolution_x, scene.render.resolution_y = 1920, 1080

bpy.ops.mesh.primitive_monkey_add(location=(0, 0, 1))
obj = bpy.context.active_object
bpy.ops.object.shade_smooth()
mat = bpy.data.materials.new("Boya"); mat.use_nodes = True
mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.1, 0.3, 0.8, 1)
obj.data.materials.append(mat)

bpy.ops.mesh.primitive_plane_add(size=20)
bpy.ops.object.light_add(type="SUN", rotation=(math.radians(50), 0, math.radians(30)))
bpy.context.active_object.data.energy = 3
bpy.ops.object.camera_add(location=(0, -6, 2.5), rotation=(math.radians(75), 0, 0))
scene.camera = bpy.context.active_object

# Döner tabla animasyonu
obj.rotation_euler = (0, 0, 0); obj.keyframe_insert("rotation_euler", frame=1)
obj.rotation_euler = (0, 0, math.radians(360)); obj.keyframe_insert("rotation_euler", frame=120)

scene.render.filepath = out
bpy.ops.render.render(write_still=True)
# three.js / Remotion için: bpy.ops.export_scene.gltf(filepath="model.glb", export_format="GLB")
```

## Kurallar

- Değişiklikten önce sahneyi incele (`get_scene_info` veya nesne listesi); kullanıcının sahnesini silme, yeni koleksiyonda çalış.
- Büyük işleri parça parça yap ve her adımda ekran görüntüsü/düşük çözünürlüklü render ile kontrol et.
- Render çıktısını video yapmak için `ffmpeg` skill'ini kullan.
- Gerçek ürünlerin (uçak, araç) birebir kopyalarını telifli modellerden alma; basitleştirilmiş, temsili modeller kur ya da lisansı açık (CC0) varlık kullan.
