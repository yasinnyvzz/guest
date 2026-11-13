#!/usr/bin/env bash
# Video üretimi için gerekli araçları kurar/denetler. Tekrar çalıştırmak güvenlidir.
set -u
ok(){ echo "  [ok] $1"; }; eksik(){ echo "  [kur] $1"; }
echo "== Sistem araçları =="
for c in ffmpeg ffprobe node npm python3; do
  command -v $c >/dev/null && ok $c || eksik "$c bulunamadı (apt/brew ile kurun)"
done
echo "== Python paketleri =="
python3 -m pip install -q faster-whisper yt-dlp 2>&1 | tail -1
python3 -c "import faster_whisper" 2>/dev/null && ok faster-whisper || eksik faster-whisper
command -v yt-dlp >/dev/null && ok yt-dlp
echo "== Remotion projesi =="
DIR="${VIDEO_PROJE:-$(dirname "$0")/remotion-proje}"
if [ ! -f "$DIR/package.json" ]; then
  mkdir -p "$DIR" && cd "$DIR" && npm init -y >/dev/null
  npm i -s remotion @remotion/cli @remotion/captions @remotion/media-utils react react-dom typescript
  echo "  Remotion kuruldu: $DIR"
else ok "Remotion projesi: $DIR"; fi
echo "Bitti. Kurallar: VIDEO_KURALLARI.md"
