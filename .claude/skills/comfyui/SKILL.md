---
name: comfyui
description: ComfyUI ile görsel/video üretimi (Stable Diffusion, Flux, Wan, LTX vb.) - workflow çalıştırma, API ile otomasyon, toplu görsel üretme, img2img, upscale; ComfyUI sunucusuna HTTP/WebSocket üzerinden istek gönderirken kullan. Kaynak - github.com/Comfy-Org/ComfyUI.
---

# ComfyUI

Düğüm tabanlı difüzyon arayüzü ve sunucusu. Varsayılan adres `http://127.0.0.1:8188`.

## Kurulum

```bash
pip install comfy-cli
comfy install                 # ComfyUI'ı kurar
comfy launch -- --listen 127.0.0.1 --port 8188    # GPU yoksa: --cpu (çok yavaş)
comfy model download --url <huggingface/civitai url> --relative-path models/checkpoints
```
Modeller: `models/checkpoints`, `models/loras`, `models/vae`, `models/diffusion_models`, `models/text_encoders`.

## API ile çalıştırma

1. Arayüzde workflow'u kur, **Workflow > Export (API)** ile `workflow_api.json` kaydet (normal export değil, API formatı: düğüm id -> `{class_type, inputs}`).
2. Python'dan parametreleri değiştirip kuyruğa gönder:

```python
import json, uuid, time, urllib.request, urllib.parse

HOST = "http://127.0.0.1:8188"
wf = json.load(open("workflow_api.json"))
# Düğüm id'lerini dosyadan bul: CLIPTextEncode (prompt), KSampler (seed), EmptyLatentImage (boyut)
wf["6"]["inputs"]["text"] = "cinematic photo of a jet trainer aircraft over Ankara, golden hour"
wf["3"]["inputs"]["seed"] = 42

body = json.dumps({"prompt": wf, "client_id": str(uuid.uuid4())}).encode()
pid = json.load(urllib.request.urlopen(urllib.request.Request(f"{HOST}/prompt", body, {"Content-Type": "application/json"})))["prompt_id"]

while True:                                   # basit bekleme; canlı ilerleme için ws://HOST/ws?clientId=...
    hist = json.load(urllib.request.urlopen(f"{HOST}/history/{pid}"))
    if pid in hist: break
    time.sleep(1)

for node in hist[pid]["outputs"].values():
    for img in node.get("images", []):
        q = urllib.parse.urlencode({"filename": img["filename"], "subfolder": img["subfolder"], "type": img["type"]})
        open(img["filename"], "wb").write(urllib.request.urlopen(f"{HOST}/view?{q}").read())
```

Diğer uç noktalar: `POST /upload/image` (img2img girdisi), `GET /object_info` (düğüm şemaları), `GET /queue`, `POST /interrupt`.

## Kurallar

- Önce `GET /system_stats` ile sunucunun ayakta olduğunu kontrol et; yoksa kullanıcıya nasıl başlatacağını söyle (bulut oturumunda GPU yok, ComfyUI genelde kullanıcının kendi makinesinde çalışır).
- `prompt` yanıtında `node_errors` doluysa eksik model/düğüm vardır; hata metnini kullanıcıya ilet.
- Toplu üretimde seed'i kaydet ki sonuç tekrarlanabilsin.
- Gerçek kişilerin sahte görüntülerini ve marka/logoları taklit eden görseller üretme.
