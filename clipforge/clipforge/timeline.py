"""Cut list for a clip: tighten dead air, drop filler words, remap word
timings onto the edited timeline (so captions stay in sync)."""
from __future__ import annotations

import re
from dataclasses import dataclass

from .captions import TimedWord, auto_emphasis
from .config import EditSettings
from .transcript import Word

FILLERS = {"um", "uh", "erm", "uhh", "umm", "uhm", "hmm", "mm"}


def is_filler(w: Word) -> bool:
    return re.sub(r"[^a-z]", "", w.text.lower()) in FILLERS


@dataclass
class Segment:
    start: float  # source time
    end: float

    @property
    def duration(self) -> float:
        return self.end - self.start


@dataclass
class CutList:
    segments: list[Segment]
    words: list[TimedWord]  # in output time

    @property
    def duration(self) -> float:
        return sum(s.duration for s in self.segments)


def build_cutlist(words: list[Word], settings: EditSettings, clip_end: float | None = None,
                  min_segment: float = 0.25) -> CutList:
    """`words` are the source words of one clip, in order."""
    kept = [w for w in words if not (settings.remove_fillers and is_filler(w))]
    if not kept:
        raise ValueError("clip has no speech")
    half = settings.keep_gap / 2
    segments: list[Segment] = []
    seg_start = max(kept[0].start - settings.pad_start, 0.0)
    for prev, nxt in zip(kept, kept[1:]):
        gap = nxt.start - prev.end
        dropped_filler = any(prev.end <= w.start and w.end <= nxt.start and is_filler(w) for w in words) \
            if settings.remove_fillers else False
        if gap > settings.max_gap or (dropped_filler and gap > settings.keep_gap):
            segments.append(Segment(seg_start, prev.end + half))
            seg_start = nxt.start - half
    end = kept[-1].end + settings.pad_end
    if clip_end is not None:
        end = min(end, clip_end) if clip_end > kept[-1].end else end
    segments.append(Segment(seg_start, end))

    # Merge slivers that would just flash on screen.
    merged: list[Segment] = []
    for s in segments:
        if merged and (s.duration < min_segment or s.start - merged[-1].end < 0.05):
            merged[-1] = Segment(merged[-1].start, max(merged[-1].end, s.end))
        else:
            merged.append(s)

    return CutList(merged, remap_words(kept, merged))


def with_cold_open(hook_words: list[Word], body: CutList, settings: EditSettings) -> CutList:
    """Play the strongest line first as a teaser, then the clip from its
    start ("hook-first" / cold open). Consensus practice for podcast
    clips; there's no controlled data on it, so it's optional."""
    tight = EditSettings(**{**settings.__dict__, "pad_start": 0.03, "pad_end": 0.12})
    teaser = build_cutlist(hook_words, tight)
    shift = teaser.duration
    moved = [TimedWord(w.text, w.start + shift, w.end + shift, w.emphasis) for w in body.words]
    return CutList(teaser.segments + body.segments, teaser.words + moved)


def remap_words(words: list[Word], segments: list[Segment]) -> list[TimedWord]:
    out: list[TimedWord] = []
    offset = 0.0
    seg_offsets = []
    for s in segments:
        seg_offsets.append(offset)
        offset += s.duration
    for w in words:
        for s, off in zip(segments, seg_offsets):
            if s.start - 1e-3 <= w.start <= s.end + 1e-3:
                start = off + (w.start - s.start)
                end = off + (min(w.end, s.end) - s.start)
                out.append(TimedWord(w.text, start, max(end, start + 0.05), auto_emphasis(w.text)))
                break
    return out
