"""Reframe landscape footage to 9:16.

Layouts
  crop   - crop a 9:16 window centred on the speaker's face
  split  - two-person podcast: each face gets half the vertical frame
  blur   - whole frame fitted to width over a blurred, zoomed copy
           (fallback when no faces are found, e.g. screen shares / gameplay)
  native - source is already vertical: just scale

Face detection uses OpenCV's bundled Haar cascade when `opencv-python-headless<5`
is installed; without it, `auto` falls back to a centred crop.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .config import HEIGHT, WIDTH
from .media import MediaInfo, grab_frames


@dataclass
class Layout:
    kind: str                       # crop | split | blur | native
    centers: tuple[float, ...] = ()  # normalized face x-centres (0-1)
    face_y: tuple[float, ...] = ()   # normalized face y-centres


def detect_faces(path: str, start: float, end: float, info: MediaInfo,
                 samples_per_sec: float = 1.0) -> list[tuple[float, float, float]] | None:
    """Return (x_center, y_center, size) for faces across sampled frames,
    normalized to 0-1. None if no face detector is available."""
    try:
        import cv2
    except ImportError:
        return None
    if not hasattr(cv2, "CascadeClassifier"):  # OpenCV 5 moved Haar cascades out of the main package
        return None
    w = 640
    h = int(round(info.height * w / info.width / 2)) * 2
    frames = grab_frames(path, start, end, samples_per_sec, w, h)
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = []
    for f in frames:
        gray = cv2.cvtColor(f, cv2.COLOR_RGB2GRAY)
        for (x, y, fw, fh) in cascade.detectMultiScale(gray, 1.1, 6, minSize=(w // 20, w // 20)):
            faces.append(((x + fw / 2) / w, (y + fh / 2) / h, fw / w))
    return faces


def choose_layout(faces: list[tuple[float, float, float]] | None, info: MediaInfo,
                  requested: str = "auto") -> Layout:
    if not info.has_video:
        return Layout("audiogram")
    if info.width and info.height and info.height >= info.width:
        return Layout("native")
    if requested == "blur":
        return Layout("blur")
    if not faces:
        if requested == "split":
            return Layout("split", (0.27, 0.73), (0.42, 0.42))  # assume left/right seats
        if requested == "auto" and faces is not None:
            return Layout("blur")  # detector ran, nobody on screen: gameplay / screen share
        return Layout("crop", (0.5,), (0.4,))
    xs = np.array([f[0] for f in faces])
    ys = np.array([f[1] for f in faces])
    # Two clusters of faces far apart horizontally -> side-by-side podcast.
    left, right = xs[xs < 0.5], xs[xs >= 0.5]
    two_people = (len(left) >= 0.25 * len(xs) and len(right) >= 0.25 * len(xs)
                  and (np.median(right) - np.median(left)) > 0.28)
    if requested == "split" or (requested == "auto" and two_people):
        if len(left) and len(right):
            return Layout("split",
                          (float(np.median(left)), float(np.median(right))),
                          (float(np.median(ys[xs < 0.5])), float(np.median(ys[xs >= 0.5]))))
    # Single speaker (or the dominant one).
    return Layout("crop", (float(np.median(xs)),), (float(np.median(ys)),))


def video_filter(layout: Layout, info: MediaInfo) -> str:
    """ffmpeg filter chain turning one input stream into 1080x1920. Uses
    `[in]` / `[out]` labels."""
    W, H = WIDTH, HEIGHT
    sw, sh = info.width, info.height
    if layout.kind == "native":
        return f"[in]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}[out]"
    if layout.kind == "blur":
        return (f"[in]split[bg][fg];"
                f"[bg]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30:3,eq=brightness=-0.08[bgb];"
                f"[fg]scale={W}:-2[fgs];[bgb][fgs]overlay=(W-w)/2:(H-h)/2[out]")
    if layout.kind == "crop":
        cw = int(sh * 9 / 16) // 2 * 2
        cw = min(cw, sw)
        x = int(np.clip(layout.centers[0] * sw - cw / 2, 0, sw - cw))
        return f"[in]crop={cw}:{sh}:{x}:0,scale={W}:{H}[out]"
    if layout.kind == "split":
        # Each panel is 1080x960 (9:8). Crop a 9:8 region around each face.
        ph = H // 2
        ch = int(sh * 0.9) // 2 * 2
        cw = int(ch * W / ph) // 2 * 2
        if cw > sw // 2 + sw // 4:
            cw = (sw // 2) // 2 * 2
            ch = int(cw * ph / W) // 2 * 2
        parts = []
        for i, (cx, cy) in enumerate(zip(layout.centers, layout.face_y)):
            x = int(np.clip(cx * sw - cw / 2, 0, sw - cw))
            y = int(np.clip(cy * sh - ch * 0.42, 0, sh - ch))
            parts.append(f"[p{i}]crop={cw}:{ch}:{x}:{y},scale={W}:{ph}[q{i}]")
        return f"[in]split[p0][p1];{';'.join(parts)};[q0][q1]vstack[out]"
    raise ValueError(f"unknown layout {layout.kind}")
