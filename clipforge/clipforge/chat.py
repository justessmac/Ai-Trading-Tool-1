"""Livestream chat signals.

Chat is the strongest cheap highlight signal for streams (Fu et al. 2017;
Song et al. 2021): epic moments show bursts of messages, short messages,
copy-pasted "crowdspeak" and emote floods. Chat lags the moment it reacts
to (broadcast delay + typing), so the lag is estimated and shifted out.
"""
from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np

EMOTES = {
    "laugh": {"lul", "lol", "kekw", "omegalul", "lmao", "lmfao", "kek", "icant", "xd", "haha", "hahaha",
              "😂", "🤣", "💀", "dead", "pepelaugh", "lulw"},
    "hype": {"pog", "pogchamp", "poggers", "pogu", "w", "letsgo", "lets", "hype", "🔥", "goat", "clip", "clipit",
             "insane", "yooo", "omg"},
    "shock": {"monkas", "wtf", "d:", "😱", "😳", "wait", "what", "nah", "bruh", "holy"},
    "cringe": {"l", "cringe", "ratio", "yikes", "😬", "residentsleeper", "weirdchamp"},
}


@dataclass
class ChatMessage:
    t: float
    text: str


def _parse_clock(s: str) -> float:
    parts = [float(p) for p in s.split(":")]
    t = 0.0
    for p in parts:
        t = t * 60 + p
    return t


def load_chat(path: str | Path) -> list[ChatMessage]:
    """Supports TwitchDownloader JSON, chat-downloader JSON, CSV
    (`seconds,user,message` or `time,message`) and plain text
    `[HH:MM:SS] user: message` logs."""
    path = Path(path)
    raw = path.read_text(encoding="utf-8", errors="replace")
    msgs: list[ChatMessage] = []
    if path.suffix.lower() == ".json":
        data = json.loads(raw)
        items = data.get("comments", data) if isinstance(data, dict) else data
        for c in items:
            if "content_offset_seconds" in c:  # TwitchDownloader
                body = c.get("message", {})
                text = body.get("body", "") if isinstance(body, dict) else str(body)
                msgs.append(ChatMessage(float(c["content_offset_seconds"]), text))
            elif "time_in_seconds" in c:  # chat-downloader
                msgs.append(ChatMessage(float(c["time_in_seconds"]), c.get("message", "")))
            elif "t" in c:
                msgs.append(ChatMessage(float(c["t"]), c.get("text", "")))
    elif path.suffix.lower() == ".csv":
        for row in csv.reader(raw.splitlines()):
            if not row:
                continue
            try:
                t = _parse_clock(row[0]) if ":" in row[0] else float(row[0])
            except ValueError:
                continue  # header
            msgs.append(ChatMessage(t, row[-1]))
    else:
        pat = re.compile(r"^\[?(\d+:\d{2}(?::\d{2})?(?:\.\d+)?)\]?\s+(?:<?[\w\-]+>?:\s*)?(.*)$")
        for line in raw.splitlines():
            m = pat.match(line.strip())
            if m:
                msgs.append(ChatMessage(_parse_clock(m.group(1)), m.group(2)))
    return sorted(msgs, key=lambda m: m.t)


@dataclass
class ChatTrack:
    rate: np.ndarray                 # messages per second (smoothed)
    categories: dict[str, np.ndarray]
    crowd: np.ndarray                # fraction of short / repeated messages per second
    lag: float = 0.0

    @classmethod
    def build(cls, msgs: list[ChatMessage], duration: float, smooth: int = 5) -> "ChatTrack":
        n = int(duration) + 1
        rate = np.zeros(n)
        crowd = np.zeros(n)
        cats = {k: np.zeros(n) for k in EMOTES}
        prev_texts: dict[int, list[str]] = {}
        for m in msgs:
            i = int(m.t)
            if not 0 <= i < n:
                continue
            rate[i] += 1
            tokens = [t.lower() for t in re.findall(r"[\w:']+|[^\w\s]", m.text)]
            for cat, words in EMOTES.items():
                if any(t in words for t in tokens):
                    cats[cat][i] += 1
            norm = m.text.strip().lower()
            seen = prev_texts.setdefault(i // 5, [])
            if len(tokens) <= 3 or norm in seen:
                crowd[i] += 1
            seen.append(norm)
        kernel = np.ones(smooth) / smooth
        sm = lambda a: np.convolve(a, kernel, mode="same")
        return cls(sm(rate), {k: sm(v) for k, v in cats.items()}, sm(crowd))

    def estimate_lag(self, reference: np.ndarray, max_lag: int = 20, default: float = 8.0) -> float:
        """Estimate chat delay by cross-correlating chat rate with a
        per-second reference signal (audio energy / reactions)."""
        n = min(len(self.rate), len(reference))
        if n < 120 or self.rate[:n].std() == 0 or reference[:n].std() == 0:
            self.lag = default
            return self.lag
        a = (self.rate[:n] - self.rate[:n].mean()) / self.rate[:n].std()
        b = (reference[:n] - reference[:n].mean()) / reference[:n].std()
        best, best_lag = -np.inf, default
        for lag in range(0, max_lag + 1):
            c = float(np.mean(a[lag:] * b[: n - lag]))
            if c > best:
                best, best_lag = c, float(lag)
        self.lag = best_lag if best > 0.05 else default
        return self.lag

    def _window(self, arr: np.ndarray, start: float, end: float, tail: float = 6.0) -> np.ndarray:
        s = int(max(start + self.lag, 0))
        e = int(min(end + self.lag + tail, len(arr)))
        return arr[s:max(e, s + 1)]

    def spike_z(self, start: float, end: float) -> float:
        """Peak chat activity in the (lag-shifted) window, as a z-score
        against the whole stream."""
        w = self._window(self.rate, start, end)
        mu, sd = float(self.rate.mean()), float(self.rate.std()) or 1.0
        return (float(w.max()) - mu) / sd if len(w) else 0.0

    def dominant_reaction(self, start: float, end: float) -> tuple[str | None, float]:
        best, best_z = None, 0.0
        for cat, arr in self.categories.items():
            w = self._window(arr, start, end)
            sd = float(arr.std()) or 1.0
            z = (float(w.max()) - float(arr.mean())) / sd if len(w) else 0.0
            if z > best_z:
                best, best_z = cat, z
        return best, best_z
