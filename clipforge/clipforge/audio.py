"""Audio analysis: loudness envelope, silences, energy spikes, laughter proxy.

Deliberately dependency-light (numpy only). A loudness envelope plus the
word timestamps gets most of the value of heavier models:

* silences          -> dead-air removal and natural clip boundaries
* energy z-scores   -> excitement / raised voices / cross-talk
* loud non-speech   -> laughter, applause, reactions (Whisper rarely
                       transcribes laughter, so energy in a word gap is a
                       good proxy)
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

import numpy as np

from .transcript import Word

HOP = 0.05  # seconds per envelope frame


@dataclass
class AudioEnvelope:
    db: np.ndarray          # loudness per frame in dBFS
    hop: float = HOP

    @classmethod
    def from_samples(cls, samples: np.ndarray, sample_rate: int, hop: float = HOP) -> "AudioEnvelope":
        n = int(sample_rate * hop)
        frames = len(samples) // n
        if frames == 0:
            return cls(np.full(1, -90.0), hop)
        x = samples[: frames * n].reshape(frames, n).astype(np.float64)
        rms = np.sqrt(np.mean(x * x, axis=1))
        return cls(20 * np.log10(np.maximum(rms, 1e-5)), hop)

    @property
    def duration(self) -> float:
        return len(self.db) * self.hop

    def _idx(self, t: float) -> int:
        return int(np.clip(round(t / self.hop), 0, len(self.db)))

    def slice(self, start: float, end: float) -> np.ndarray:
        return self.db[self._idx(start): max(self._idx(end), self._idx(start) + 1)]

    @cached_property
    def speech_floor(self) -> float:
        """Robust estimate of 'normal talking' loudness (median of the
        non-silent frames)."""
        active = self.db[self.db > np.percentile(self.db, 20)]
        return float(np.median(active)) if len(active) else float(np.median(self.db))

    @cached_property
    def spread(self) -> float:
        active = self.db[self.db > np.percentile(self.db, 20)]
        s = float(np.std(active)) if len(active) > 1 else 1.0
        return max(s, 1.0)

    def energy_z(self, start: float, end: float) -> float:
        """How much louder than this speaker's baseline a window is, in
        standard deviations, using the 90th percentile so a single shout in
        a window counts."""
        seg = self.slice(start, end)
        return (float(np.percentile(seg, 90)) - self.speech_floor) / self.spread

    def dynamics(self, start: float, end: float) -> float:
        """Loudness variation inside a window - flat monotone delivery scores low."""
        seg = self.slice(start, end)
        seg = seg[seg > self.speech_floor - 2 * self.spread]
        return float(np.std(seg)) / self.spread if len(seg) > 2 else 0.0

    def silences(self, threshold_db: float | None = None, min_len: float = 0.3) -> list[tuple[float, float]]:
        thr = threshold_db if threshold_db is not None else self.speech_floor - 18.0
        quiet = self.db < thr
        out, start = [], None
        for i, q in enumerate(quiet):
            if q and start is None:
                start = i
            elif not q and start is not None:
                if (i - start) * self.hop >= min_len:
                    out.append((start * self.hop, i * self.hop))
                start = None
        if start is not None and (len(quiet) - start) * self.hop >= min_len:
            out.append((start * self.hop, len(quiet) * self.hop))
        return out


def envelope_from_file(path: str, hop: float = HOP, sample_rate: int = 8000) -> AudioEnvelope:
    """Stream-decode the audio so multi-hour streams never sit in memory."""
    import subprocess

    n = int(sample_rate * hop)
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "1", "-ar", str(sample_rate), "-f", "s16le", "-"],
        stdout=subprocess.PIPE,
    )
    chunks: list[np.ndarray] = []
    leftover = np.zeros(0, dtype=np.float32)
    block = n * 2 * 2000  # bytes per read: 2000 frames
    assert proc.stdout is not None
    while True:
        buf = proc.stdout.read(block)
        if not buf:
            break
        x = np.concatenate([leftover, np.frombuffer(buf[: len(buf) // 2 * 2], dtype=np.int16).astype(np.float32) / 32768.0])
        frames = len(x) // n
        if frames:
            f = x[: frames * n].reshape(frames, n).astype(np.float64)
            chunks.append(20 * np.log10(np.maximum(np.sqrt(np.mean(f * f, axis=1)), 1e-5)))
        leftover = x[frames * n:]
    if proc.wait() != 0:
        raise RuntimeError(f"ffmpeg could not decode audio from {path}")
    db = np.concatenate(chunks) if chunks else np.full(1, -90.0)
    return AudioEnvelope(db, hop)


def per_second(env: AudioEnvelope) -> np.ndarray:
    """Loudness per second (for chat-lag estimation)."""
    k = int(round(1 / env.hop))
    n = len(env.db) // k
    return env.db[: n * k].reshape(n, k).max(axis=1) if n else env.db.copy()


_LAUGH_TOKENS =("haha", "hahaha", "lol", "lmao", "(laughs)", "[laughter]", "(laughter)", "[laughs]")


def reaction_events(env: AudioEnvelope, words: list[Word], min_gap: float = 0.4,
                    z_threshold: float = 0.8) -> list[tuple[float, float]]:
    """Find loud stretches with no transcribed speech (laughter, applause,
    gasps) plus explicit laughter tokens. Returns (time, strength) pairs."""
    events: list[tuple[float, float]] = []
    for a, b in zip(words, words[1:]):
        gap = b.start - a.end
        if gap < min_gap:
            continue
        z = env.energy_z(a.end, b.start)
        if z >= z_threshold:
            events.append(((a.end + b.start) / 2, min(z, 3.0) * min(gap, 2.0)))
    for w in words:
        if w.text.lower().strip(".,!?") in _LAUGH_TOKENS:
            events.append((w.start, 1.5))
    return sorted(events)
