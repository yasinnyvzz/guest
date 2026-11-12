"""Kokoro (Apache 2.0, offline) narration for this film.
  python3 logs/kokoro_tts.py audition <voice,voice,...> "<text>" <out_dir>
  python3 logs/kokoro_tts.py lines <voice> <speed> audio/vo-lines.json <out_dir>
Writes 48 kHz mono 24-bit WAVs (ffmpeg resample) and a log with each line's duration."""
import json, os, subprocess, sys, tempfile
import soundfile as sf
from kokoro_onnx import Kokoro

M = os.path.expanduser('~/.cinecode/tts/kokoro')
k = Kokoro(os.path.join(M, 'kokoro-v1.0.onnx'), os.path.join(M, 'voices-v1.0.bin'))


def say(text, voice, speed, out):
    lang = 'en-gb' if voice.startswith('b') else 'en-us'
    samples, sr = k.create(text, voice=voice, speed=speed, lang=lang)
    tmp = tempfile.mktemp(suffix='.wav')
    sf.write(tmp, samples, sr)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-ar', '48000', '-ac', '1', '-c:a', 'pcm_s24le', out], check=True)
    os.remove(tmp)
    return len(samples) / sr


mode = sys.argv[1]
if mode == 'audition':
    voices, text, out = sys.argv[2].split(','), sys.argv[3], sys.argv[4]
    os.makedirs(out, exist_ok=True)
    for v in voices:
        d = say(text, v, 1.0, os.path.join(out, f'{v}.wav'))
        print(f'{v}: {d:.1f} s')
else:
    voice, speed, lines, out = sys.argv[2], float(sys.argv[3]), sys.argv[4], sys.argv[5]
    os.makedirs(out, exist_ok=True)
    log = {}
    for ln in json.load(open(lines, encoding='utf-8'))['lines']:
        d = say(ln['text'], voice, speed, os.path.join(out, ln['id'] + '.wav'))
        log[ln['id']] = round(d, 2)
        print(f"{ln['id']}: {d:.1f} s")
    json.dump({'engine': 'kokoro v1.0', 'voice': voice, 'speed': speed, 'durations': log}, open(os.path.join(out, 'tts-log.json'), 'w'), indent=1)
