"""Render a clip with ffmpeg: cut list -> punch-ins -> 9:16 reframe ->
captions -> (licensed music, ducked) -> loudness normalisation -> H.264.

Export settings follow YouTube's published recommendations (H.264 High,
closed GOP of half the frame rate, AAC 48 kHz, faststart), which also sit
inside TikTok's and Instagram's limits, so one master works for all three.
"""
from __future__ import annotations

import tempfile
from pathlib import Path

from .config import HEIGHT, WIDTH, EditSettings
from .media import MediaInfo, run
from .reframe import Layout, video_filter
from .rights import MusicTrack
from .timeline import Segment

FONTS_DIR = Path(__file__).resolve().parent.parent / "fonts"


def _ff_escape(path: str) -> str:
    return path.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")


def build_filtergraph(segments: list[Segment], offset: float, info: MediaInfo, layout: Layout,
                      ass_path: str | None, settings: EditSettings, music: bool) -> str:
    parts: list[str] = []
    cx = layout.centers[0] if layout.centers else 0.5
    cy = layout.face_y[0] if layout.face_y else 0.45
    elapsed = 0.0
    zoomed = False
    video = info.has_video
    for i, seg in enumerate(segments):
        s, e = seg.start - offset, seg.end - offset
        fade = min(0.015, seg.duration / 4)
        parts.append(f"[0:a]atrim=start={s:.3f}:end={e:.3f},asetpts=PTS-STARTPTS,"
                     f"afade=t=in:d={fade:.3f},afade=t=out:st={max(seg.duration - fade, 0):.3f}:d={fade:.3f}[a{i}]")
        if not video:
            continue
        v = f"[0:v]trim=start={s:.3f}:end={e:.3f},setpts=PTS-STARTPTS,fps={settings.fps},setsar=1"
        # Alternate a subtle punch-in on jump cuts (and every N seconds) to
        # hide the cut and keep a visual change on screen.
        if settings.punch_in_every > 0 and layout.kind in ("crop", "native", "blur"):
            if i > 0 and (elapsed >= settings.punch_in_every or i % 2 == 1):
                zoomed = not zoomed
                elapsed = 0.0
            if zoomed:
                z = settings.punch_in_scale
                v += (f",crop=iw/{z}:ih/{z}:min(max(iw*{cx:.3f}-iw/{z}/2\\,0)\\,iw-iw/{z})"
                      f":min(max(ih*{cy:.3f}-ih/{z}/2\\,0)\\,ih-ih/{z}),scale={info.width}:{info.height}")
        elapsed += seg.duration
        parts.append(v + f",setsar=1[v{i}]")
    n = len(segments)
    if video:
        parts.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[vc][ac]")
        parts.append(video_filter(layout, info).replace("[in]", "[vc]").replace("[out]", "[vr]"))
    else:
        # Audio-only source: audiogram (dark background + live waveform).
        parts.append("".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[acat]")
        parts.append("[acat]asplit[ac][aw]")
        parts.append(f"[aw]showwaves=s={WIDTH}x480:mode=cline:rate={settings.fps}:colors=white,format=yuva420p[wave]")
        parts.append(f"color=c=0x15151c:s={WIDTH}x{HEIGHT}:r={settings.fps}[bg]")
        parts.append("[bg][wave]overlay=0:(H-h)/2-120:shortest=1,setsar=1[vr]")
    if ass_path:
        fonts = f":fontsdir='{_ff_escape(str(FONTS_DIR))}'" if FONTS_DIR.exists() else ""
        parts.append(f"[vr]ass=filename='{_ff_escape(ass_path)}'{fonts},format=yuv420p[vout]")
    else:
        parts.append("[vr]format=yuv420p[vout]")
    loud = f"loudnorm=I={settings.target_lufs}:TP={settings.true_peak}:LRA=11,aresample=48000"
    if music:
        parts.append("[ac]asplit[speech][sc]")
        parts.append(f"[1:a]volume={settings.music_gain_db}dB[mus]")
        parts.append("[mus][sc]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=350[duck]")
        parts.append(f"[speech][duck]amix=inputs=2:duration=first:normalize=0,{loud}[aout]")
    else:
        parts.append(f"[ac]{loud}[aout]")
    return ";".join(parts)


def render_clip(source: str, info: MediaInfo, segments: list[Segment], layout: Layout, ass_text: str | None,
                out_path: str | Path, settings: EditSettings, music: MusicTrack | None = None) -> Path:
    out_path = Path(out_path)
    offset = max(min(s.start for s in segments) - 1.0, 0.0)
    span = max(s.end for s in segments) - offset + 1.0
    with tempfile.TemporaryDirectory(prefix="clipforge_") as tmp:
        ass_path = None
        if ass_text:
            ass_path = str(Path(tmp) / "captions.ass")
            Path(ass_path).write_text(ass_text, encoding="utf-8")
        graph = build_filtergraph(segments, offset, info, layout, ass_path, settings, music is not None)
        cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{offset:.3f}", "-t", f"{span:.3f}", "-i", source]
        if music:
            cmd += ["-stream_loop", "-1", "-i", music.file]
        gop = max(settings.fps // 2, 1)
        cmd += [
            "-filter_complex", graph, "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "medium", "-profile:v", "high", "-crf", str(settings.crf),
            "-maxrate", settings.maxrate, "-bufsize", "24M", "-g", str(gop), "-bf", "2", "-flags", "+cgop",
            "-pix_fmt", "yuv420p", "-r", str(settings.fps), "-s", f"{WIDTH}x{HEIGHT}",
            "-c:a", "aac", "-b:a", settings.audio_bitrate, "-ar", "48000",
            "-movflags", "+faststart", "-shortest", str(out_path),
        ]
        try:
            run(cmd)
        except Exception:
            out_path.unlink(missing_ok=True)
            raise
    return out_path


def extract_cover(video: str | Path, out: str | Path, t: float = 0.6) -> Path:
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(video), "-frames:v", "1", "-q:v", "2", str(out)])
    return Path(out)
