---
name: chatterbox-tts
description: Chatterbox (Resemble AI) ile metinden sese (TTS), seslendirme/voiceover, ses klonlama ve Türkçe dahil 23 dilde konuşma üretirken kullan. Reels, video anlatımı ve Remotion/Hyperframes projelerine ses hazırlama. Kaynak - github.com/resemble-ai/chatterbox.
---

# Chatterbox TTS

Açık kaynak (MIT) TTS modelleri. Python 3.10+, PyTorch.

```bash
pip install chatterbox-tts
```

## Model seçimi

| İhtiyaç | Sınıf | Not |
|---|---|---|
| Türkçe ve diğer diller | `ChatterboxMultilingualTTS` (`t3_model="v3"`) | `language_id="tr"` |
| İngilizce, hızlı, `[chuckle]` gibi etiketler | `ChatterboxTurboTTS` | referans ses klibi gerekir |
| CPU'da hafif | `ChatterboxTurboTTS.from_pretrained(nano=True)` | |
| İngilizce klasik | `ChatterboxTTS` | `exaggeration`, `cfg_weight` ayarı |

## Türkçe seslendirme

```python
import torch, torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
model = ChatterboxMultilingualTTS.from_pretrained(device=device, t3_model="v3")

text = "HÜRJET, Türkiye'nin ilk jet eğitim ve hafif taarruz uçağıdır."
wav = model.generate(text, language_id="tr")                       # varsayılan ses
# wav = model.generate(text, language_id="tr", audio_prompt_path="ref_10sn.wav")  # ses klonlama
ta.save("voiceover.wav", wav, model.sr)
```

## İyi sonuç için

- Uzun metni cümle/paragraf parçalarına böl, her parçayı ayrı üret, sonra `ffmpeg` concat ile birleştir. Tek seferde çok uzun metin tonu bozar.
- Kısaltmaları ve sayıları yazıyla ver ("SSB" yerine gerekiyorsa "Es Es Be", "2027" yerine "iki bin yirmi yedi") ve sonucu dinleyerek/transkribe ederek kontrol et (`faster-whisper` ile geri çevirip metinle karşılaştır).
- Ses klonlama için 7-15 sn, temiz, tek konuşmacılı WAV referans kullan.
- Daha dramatik anlatım: `exaggeration=0.7, cfg_weight=0.3`; nötr anlatım varsayılanlar.
- Sosyal medya için ses seviyesini `ffmpeg -af loudnorm=I=-14:TP=-1.5` ile normalize et.

## Etik

Sadece kullanıcının kendi sesini veya açık izni olan sesleri klonla. Gerçek bir kişiyi taklit eden, yanıltıcı ses üretme. Üretilen dosyalar Resemble'ın PerTh filigranını taşır.
