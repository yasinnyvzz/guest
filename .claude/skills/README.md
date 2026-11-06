# Skill'ler

Bu klasördeki skill'ler, bu repo ile açılan her Claude Code oturumunda (bulut ve yerel) otomatik yüklenir. `/skill-adı` ile çağrılabilir ya da konu geldiğinde Claude kendisi kullanır.

## Kaynak repolardan birebir alınanlar

| Kaynak | Skill'ler |
|---|---|
| [remotion-dev/skills](https://github.com/remotion-dev/skills) (Remotion'un resmi skill'leri; [remotion-dev/remotion](https://github.com/remotion-dev/remotion) için) | `remotion-best-practices`, `remotion-create`, `remotion-render`, `remotion-studio`, `remotion-captions`, `remotion-multimedia`, `remotion-markup`, `remotion-maps`, `remotion-interactivity`, `remotion-saas`, `remotion-docs`, `remotion-upgrade`, `remotion-license` |
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `hyperframes-figma` (orijinal adı `figma`), `media-use`, `remotion-to-hyperframes`, `reverse-any-video`, `slideshow`, `style-sampling` |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | `impeccable` |
| [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) | `chrome-devtools`, `chrome-devtools-cli`, `chrome-devtools-troubleshooting` (orijinal adı `troubleshooting`), `a11y-debugging`, `cookie-debugging`, `debug-optimize-lcp`, `memory-leak-debugging` |

## Bu repo için yazılanlar (kaynak repoda hazır skill yok)

| Kaynak | Skill |
|---|---|
| [blender/blender](https://github.com/blender/blender) + [ahujasid/mcp-for-blender](https://github.com/ahujasid/mcp-for-blender) | `blender` |
| [FFmpeg/FFmpeg](https://github.com/FFmpeg/FFmpeg) | `ffmpeg` |
| [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper) | `faster-whisper` |
| [resemble-ai/chatterbox](https://github.com/resemble-ai/chatterbox) | `chatterbox-tts` |
| [greensock/GSAP](https://github.com/greensock/GSAP) | `gsap` |
| [mrdoob/three.js](https://github.com/mrdoob/three.js) | `threejs` |
| [Comfy-Org/ComfyUI](https://github.com/Comfy-Org/ComfyUI) | `comfyui` |
| [yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp) | `yt-dlp` |

## MCP sunucuları (ayrıca etkinleştirilmeli)

`chrome-devtools*` skill'leri ve `blender` skill'inin canlı modu bir MCP sunucusu ister. Kendi bilgisayarında bir kez çalıştır:

```bash
claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest
uvx mcp-for-blender setup        # veya: claude mcp add blender uvx mcp-for-blender
```

## Güncelleme

Skill'ler 2026-11-06 tarihli kaynaklardan kopyalandı. Yenilemek için Claude'a "skill'leri kaynak repolardan güncelle" demen yeterli.

Kopyalanan sürümler:

- `remotion-dev/skills` @ `a2824c6`
- `heygen-com/hyperframes` @ `e2bb7da`
- `pbakaus/impeccable` @ `c3bb418`
- `ChromeDevTools/chrome-devtools-mcp` @ `e3eb901`
