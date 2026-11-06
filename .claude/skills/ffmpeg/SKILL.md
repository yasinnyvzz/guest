---
name: ffmpeg
description: FFmpeg ile video/ses dönüştürme, kesme, birleştirme, ölçekleme, altyazı gömme, ses ayıklama, GIF/kare çıkarma ve sosyal medya formatlarına (9:16 Reels, 1:1, 16:9) hazırlama işlerinde kullan. Kaynak - github.com/FFmpeg/FFmpeg.
---

# FFmpeg

Komut satırından her türlü medya işini yapan araç. Önce `ffmpeg -version` ile kurulu mu bak; yoksa `apt-get install -y ffmpeg` (Linux) veya `brew install ffmpeg` (macOS).

## Çalışma kuralları

- Önce kaynağı incele: `ffprobe -v error -show_entries format=duration:stream=index,codec_type,codec_name,width,height,r_frame_rate,sample_rate -of json girdi.mp4`
- Orijinal dosyanın üzerine asla yazma; çıktıyı yeni bir dosyaya ver. `-y` sadece kendi ürettiğin çıktılar için.
- Yeniden kodlamaya gerek yoksa `-c copy` kullan (hızlı, kayıpsız). Hassas kesim gerekiyorsa yeniden kodla.
- Uyumlu MP4 varsayılanı: `-c:v libx264 -pix_fmt yuv420p -crf 20 -preset medium -c:a aac -b:a 192k -movflags +faststart`
- Bittiğinde çıktıyı `ffprobe` ile doğrula (süre, çözünürlük, ses akışı var mı).

## Sık tarifler

```bash
# Kesme (hızlı, keyframe'e oturur)
ffmpeg -ss 00:00:05 -to 00:00:20 -i in.mp4 -c copy out.mp4
# Kesme (kare hassas)
ffmpeg -ss 00:00:05 -to 00:00:20 -i in.mp4 -c:v libx264 -crf 18 -c:a aac out.mp4

# 16:9 -> 9:16 Reels (bulanık arka plan + ortada video)
ffmpeg -i in.mp4 -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20:5[bg];[0:v]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2" -c:v libx264 -pix_fmt yuv420p -crf 20 -c:a copy reels.mp4

# Ölçek / fps
ffmpeg -i in.mp4 -vf "scale=1920:-2,fps=30" -c:v libx264 -crf 20 -c:a copy out.mp4

# Ses ayıkla (Whisper için 16 kHz mono WAV)
ffmpeg -i in.mp4 -vn -ac 1 -ar 16000 audio.wav

# Sesi değiştir / müzik ekle (müzik -14 dB, video süresi kadar)
ffmpeg -i video.mp4 -i music.mp3 -filter_complex "[1:a]volume=-14dB[m];[0:a][m]amix=inputs=2:duration=first[a]" -map 0:v -map "[a]" -c:v copy -c:a aac out.mp4

# Ses normalizasyonu (sosyal medya -14 LUFS)
ffmpeg -i in.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:v copy out.mp4

# SRT altyazıyı videoya göm (yakılmış)
ffmpeg -i in.mp4 -vf "subtitles=sub.srt:force_style='FontName=Inter,FontSize=18,Outline=2'" -c:a copy out.mp4

# Aynı codec'teki dosyaları birleştir
printf "file '%s'\n" part1.mp4 part2.mp4 > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy joined.mp4

# Görsel dizisinden video
ffmpeg -framerate 30 -i frames/%05d.png -c:v libx264 -pix_fmt yuv420p out.mp4

# Kare çıkar (saniyede 1) / tek kapak karesi
ffmpeg -i in.mp4 -vf fps=1 frames/%04d.png
ffmpeg -ss 3 -i in.mp4 -frames:v 1 cover.jpg

# Kaliteli GIF (palet ile)
ffmpeg -i in.mp4 -vf "fps=15,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse" out.gif

# Logo/filigran (sağ üst)
ffmpeg -i in.mp4 -i logo.png -filter_complex "overlay=W-w-40:40" -c:a copy out.mp4

# Hızlandır 2x
ffmpeg -i in.mp4 -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" -map "[v]" -map "[a]" out.mp4
```

## Platform hedefleri

| Platform | Boyut | Not |
|---|---|---|
| Instagram Reels / TikTok / Shorts | 1080x1920, 30 fps | H.264, AAC, `+faststart` |
| Instagram kare / 4:5 | 1080x1080 / 1080x1350 | |
| X / YouTube | 1920x1080 | |

Karmaşık filtre zincirlerinde önce 5 saniyelik bir parçada (`-t 5`) dene, sonra tamamını işle.
