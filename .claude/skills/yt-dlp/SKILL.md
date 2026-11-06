---
name: yt-dlp
description: yt-dlp ile YouTube, X/Twitter, Instagram vb. sitelerden video, ses, altyazı, küçük resim ve meta veri indirirken kullan; referans video analizi, transkripsiyon veya kendi içeriğini arşivleme için. Kaynak - github.com/yt-dlp/yt-dlp.
---

# yt-dlp

## Kurulum

```bash
pip install -U yt-dlp      # veya: uv tool install yt-dlp / brew install yt-dlp
```
Birleştirme için `ffmpeg` gerekir.

## Tarifler

```bash
# Önce bilgi al, indirmeden
yt-dlp -F URL                                  # mevcut formatlar
yt-dlp --dump-json --skip-download URL > meta.json

# En iyi kalite, MP4
yt-dlp -f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b" --merge-output-format mp4 -o "%(title).80s [%(id)s].%(ext)s" URL

# En fazla 1080p
yt-dlp -f "bv*[height<=1080]+ba/b[height<=1080]" --merge-output-format mp4 URL

# Sadece ses (MP3) - transkripsiyon için
yt-dlp -x --audio-format mp3 URL

# Sadece altyazı (varsa elle, yoksa otomatik), video yok
yt-dlp --skip-download --write-subs --write-auto-subs --sub-langs "tr,en" --convert-subs srt URL

# Belirli bölüm
yt-dlp --download-sections "*00:01:00-00:02:30" URL

# Küçük resim
yt-dlp --skip-download --write-thumbnail --convert-thumbnails jpg URL

# Oynatma listesi, numaralı
yt-dlp -o "%(playlist_index)03d - %(title)s.%(ext)s" PLAYLIST_URL
```

## Kurallar

- Telif: sadece kullanıcının hakkı olan içeriği veya analiz/alıntı için gereken kısmı indir; başkasının videosunu yeniden yayımlamak için kullanma.
- Giriş gerektiren içerikte `--cookies-from-browser chrome` sadece kullanıcının kendi bilgisayarında ve onayıyla.
- "Sign in to confirm you're not a bot" veya 403 hatası: önce `pip install -U yt-dlp` ile güncelle. Bulut oturumlarında YouTube çoğu zaman engellenir; kullanıcıya dosyayı kendisinin yüklemesini öner.
- Dosya adlarında `%(title).80s` ile uzunluğu sınırla.
