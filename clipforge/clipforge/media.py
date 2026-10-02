"""Thin wrappers around ffmpeg / ffprobe.

Everything that touches media files goes through here so the rest of the
package can stay pure-Python and unit-testable.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

import numpy as np


class FFmpegError(RuntimeError):
    pass


def require_ffmpeg() -> None:
    for tool in ("ffmpeg", "ffprobe"):
        if shutil.which(tool) is None:
            raise FFmpegError(f"{tool} not found on PATH - install ffmpeg first")


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    proc = subprocess.run(cmd, capture_output=True)
    if proc.returncode != 0:
        tail = proc.stderr.decode(errors="replace")[-2000:]
        raise FFmpegError(f"command failed: {' '.join(cmd[:6])} ...\n{tail}")
    return proc


@dataclass(frozen=True)
class MediaInfo:
    duration: float
    width: int | None
    height: int | None
    fps: float | None
    has_audio: bool

    @property
    def has_video(self) -> bool:
        return self.width is not None


def probe(path: str | Path) -> MediaInfo:
    proc = run([
        "ffprobe", "-v", "error", "-print_format", "json",
        "-show_format", "-show_streams", str(path),
    ])
    data = json.loads(proc.stdout)
    video = next((s for s in data["streams"] if s.get("codec_type") == "video"
                  and not s.get("disposition", {}).get("attached_pic")), None)  # skip mp3 cover art
    has_audio = any(s.get("codec_type") == "audio" for s in data["streams"])
    fps = None
    if video and video.get("avg_frame_rate", "0/0") != "0/0":
        num, den = video["avg_frame_rate"].split("/")
        fps = float(num) / float(den) if float(den) else None
    return MediaInfo(
        duration=float(data["format"].get("duration", 0.0)),
        width=int(video["width"]) if video else None,
        height=int(video["height"]) if video else None,
        fps=fps,
        has_audio=has_audio,
    )


def read_audio_mono(path: str | Path, sample_rate: int = 16000) -> np.ndarray:
    """Decode the first audio stream to mono float32 in [-1, 1]."""
    proc = run([
        "ffmpeg", "-v", "error", "-i", str(path), "-vn",
        "-ac", "1", "-ar", str(sample_rate), "-f", "s16le", "-",
    ])
    pcm = np.frombuffer(proc.stdout, dtype=np.int16)
    return pcm.astype(np.float32) / 32768.0


def extract_wav(path: str | Path, out: str | Path, sample_rate: int = 16000) -> Path:
    run([
        "ffmpeg", "-v", "error", "-y", "-i", str(path), "-vn",
        "-ac", "1", "-ar", str(sample_rate), str(out),
    ])
    return Path(out)


def grab_frames(path: str | Path, start: float, end: float, fps: float,
                width: int, height: int) -> np.ndarray:
    """Return RGB frames (N, H, W, 3) sampled at `fps` between start and end,
    scaled to width x height. Used for face tracking at low resolution."""
    proc = run([
        "ffmpeg", "-v", "error", "-ss", f"{start:.3f}", "-to", f"{end:.3f}",
        "-i", str(path), "-vf", f"fps={fps},scale={width}:{height}",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
    ])
    frame_bytes = width * height * 3
    n = len(proc.stdout) // frame_bytes
    return np.frombuffer(proc.stdout[: n * frame_bytes], dtype=np.uint8).reshape(n, height, width, 3)
