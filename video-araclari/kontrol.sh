#!/usr/bin/env bash
# Kullanım: kontrol.sh video.mp4  -> çözünürlük, donmuş kare, sahne ritmi, ses seviyesi raporu
f="${1:?video.mp4 verin}"
echo "== Çözünürlük/fps =="
read -r w h < <(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=' ' "$f")
fps=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$f")
echo "$w x $h @ $fps"
[ "$w" = 1080 ] && [ "$h" = 1920 ] && echo "  [ok] 1080x1920" || echo "  [HATA] 1080x1920 olmalı"
echo "== Donmuş kareler (>=2 sn) =="
ffmpeg -v info -i "$f" -vf "freezedetect=n=-50dB:d=2" -an -f null - 2>&1 | grep -E "freeze_(start|duration)" || echo "  [ok] yok"
echo "== Sahne kesmeleri =="
n=$(ffmpeg -v info -i "$f" -vf "select='gt(scene,0.25)',showinfo" -an -f null - 2>&1 | grep -c pts_time)
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
echo "  süre=${d}s kesme=$n ortalama sahne=$(python3 -c "print(round($d/max($n+1,1),1))")s (hedef 2-4 sn)"
echo "== Ses seviyesi (hedef -14 LUFS) =="
ffmpeg -v info -i "$f" -af loudnorm=print_format=summary -vn -f null - 2>&1 | grep -E "Input Integrated"
