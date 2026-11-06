---
name: faster-whisper
description: faster-whisper ile ses/video dosyasını yazıya dökme (transkripsiyon), kelime bazlı zaman damgası, SRT/VTT altyazı ve Remotion/Hyperframes için caption JSON üretirken kullan. Türkçe dahil çok dilli. Kaynak - github.com/SYSTRAN/faster-whisper.
---

# faster-whisper

CTranslate2 tabanlı Whisper; orijinalinden ~4 kat hızlı, daha az bellek.

## Kurulum

```bash
pip install faster-whisper
```
Video girdisinde önce sesi ayıkla: `ffmpeg -i in.mp4 -vn -ac 1 -ar 16000 audio.wav` (bkz. `ffmpeg` skill'i).

## Model ve cihaz seçimi

| Durum | Model | Ayar |
|---|---|---|
| GPU var | `large-v3` veya `turbo` | `device="cuda", compute_type="float16"` |
| Sadece CPU, kalite | `large-v3` | `device="cpu", compute_type="int8"` (yavaş) |
| Sadece CPU, hız | `small` / `medium` | `device="cpu", compute_type="int8"` |

Türkçe için en az `medium` kullan; `small` özel isimlerde (ASELSAN, HÜRJET, KAAN gibi) çok hata yapar. Bu tür terimleri `initial_prompt` ile ver.

## Temel kullanım

```python
from faster_whisper import WhisperModel

model = WhisperModel("large-v3", device="cpu", compute_type="int8")
segments, info = model.transcribe(
    "audio.wav",
    language="tr",            # biliniyorsa ver; otomatik tespit de var
    beam_size=5,
    vad_filter=True,          # sessizlikleri atlar, halüsinasyonu azaltır
    word_timestamps=True,     # kelime bazlı zamanlama (altyazı animasyonu için)
    initial_prompt="ASELSAN, Baykar, HÜRJET, KAAN, SSB",
)
print(info.language, info.language_probability)
for s in segments:            # segments bir generator; döngü transkripsiyonu başlatır
    print(f"[{s.start:.2f} -> {s.end:.2f}] {s.text}")
```

Uzun dosyalarda GPU varsa `BatchedInferencePipeline(model=model).transcribe(..., batch_size=16)` kullan.

## SRT üretme

```python
def ts(t):
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{int(h):02}:{int(m):02}:{int(s):02},{int((s % 1) * 1000):03}"

with open("out.srt", "w", encoding="utf-8") as f:
    for i, s in enumerate(segments, 1):
        f.write(f"{i}\n{ts(s.start)} --> {ts(s.end)}\n{s.text.strip()}\n\n")
```

## Remotion caption formatı

Remotion `@remotion/captions` şu diziyi bekler (bkz. `remotion-captions` skill'i):

```python
import json
caps = [{"text": " " + w.word.strip(), "startMs": int(w.start*1000), "endMs": int(w.end*1000),
         "timestampMs": int(w.start*1000), "confidence": w.probability}
        for s in segments for w in (s.words or [])]
json.dump(caps, open("captions.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
```

## Doğrulama

Çıktıyı okuyup özel isimleri, sayıları ve kısaltmaları kontrol et; Whisper'ın yanlış yazdıklarını elle düzelt ve kullanıcıya hangi düzeltmeleri yaptığını söyle. İlk çalıştırmada model Hugging Face'ten iner (large-v3 ~3 GB).
