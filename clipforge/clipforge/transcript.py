"""Word-level transcripts: data model, loaders, transcription, sentence grouping.

Every downstream step (candidate windows, scoring, silence removal,
captions) works off word timestamps, so this is the backbone of the tool.
"""
from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class Word:
    text: str
    start: float
    end: float
    speaker: str | None = None
    prob: float = 1.0


@dataclass
class Sentence:
    words: list[Word] = field(default_factory=list)

    @property
    def start(self) -> float:
        return self.words[0].start

    @property
    def end(self) -> float:
        return self.words[-1].end

    @property
    def text(self) -> str:
        return " ".join(w.text for w in self.words).strip()

    @property
    def speaker(self) -> str | None:
        speakers = [w.speaker for w in self.words if w.speaker]
        return max(set(speakers), key=speakers.count) if speakers else None


@dataclass
class Transcript:
    words: list[Word]
    language: str | None = None

    @property
    def duration(self) -> float:
        return self.words[-1].end if self.words else 0.0

    def words_between(self, start: float, end: float) -> list[Word]:
        return [w for w in self.words if w.start >= start - 1e-3 and w.end <= end + 1e-3]

    def text_between(self, start: float, end: float) -> str:
        return " ".join(w.text for w in self.words_between(start, end))

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps({
            "language": self.language,
            "words": [asdict(w) for w in self.words],
        }))

    @classmethod
    def load(cls, path: str | Path) -> "Transcript":
        """Load our own format, WhisperX / faster-whisper style JSON, or SRT."""
        path = Path(path)
        if path.suffix.lower() == ".srt":
            return _load_srt(path.read_text(encoding="utf-8", errors="replace"))
        data = json.loads(path.read_text())
        if "words" in data:
            return cls([Word(**w) for w in data["words"]], data.get("language"))
        if "segments" in data:  # WhisperX / whisper JSON
            words: list[Word] = []
            for seg in data["segments"]:
                seg_words = seg.get("words")
                if not seg_words:
                    words.extend(_spread_words(seg["text"], seg["start"], seg["end"], seg.get("speaker")))
                    continue
                for w in seg_words:
                    if "start" not in w or "end" not in w:
                        continue  # WhisperX leaves numerals unaligned
                    words.append(Word(
                        text=w["word"].strip(), start=float(w["start"]), end=float(w["end"]),
                        speaker=w.get("speaker", seg.get("speaker")), prob=float(w.get("score", w.get("probability", 1.0))),
                    ))
            return cls(words, data.get("language"))
        raise ValueError(f"unrecognised transcript format: {path}")


def _spread_words(text: str, start: float, end: float, speaker: str | None = None) -> list[Word]:
    """Approximate word timings when only segment timings are known
    (e.g. SRT). Time is allotted proportional to word length."""
    tokens = text.split()
    if not tokens:
        return []
    total = sum(len(t) + 1 for t in tokens)
    out, t = [], start
    for tok in tokens:
        dur = (end - start) * (len(tok) + 1) / total
        out.append(Word(tok, t, t + dur, speaker))
        t += dur
    return out


_SRT_TIME = re.compile(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)")


def _load_srt(raw: str) -> Transcript:
    words: list[Word] = []
    for block in re.split(r"\n\s*\n", raw.strip()):
        lines = block.strip().splitlines()
        for i, line in enumerate(lines):
            m = _SRT_TIME.search(line)
            if m:
                g = [int(x) for x in m.groups()]
                start = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
                end = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
                text = re.sub(r"<[^>]+>", "", " ".join(lines[i + 1:]))
                words.extend(_spread_words(text, start, end))
                break
    return Transcript(words)


def transcribe(media_path: str | Path, model_size: str = "small", language: str | None = None,
               device: str = "auto") -> Transcript:
    """Transcribe with faster-whisper (optional dependency) using word timestamps."""
    try:
        from faster_whisper import WhisperModel
    except ImportError as e:  # pragma: no cover - depends on optional install
        raise RuntimeError(
            "faster-whisper is not installed. `pip install faster-whisper`, or pass an "
            "existing transcript with --transcript (WhisperX JSON or SRT)."
        ) from e
    model = WhisperModel(model_size, device=device, compute_type="auto")
    segments, info = model.transcribe(
        str(media_path), language=language, word_timestamps=True, vad_filter=True,
    )
    words = [
        Word(w.word.strip(), float(w.start), float(w.end), prob=float(w.probability))
        for seg in segments for w in (seg.words or [])
        if w.word.strip()
    ]
    return Transcript(words, info.language)


_TERMINAL = re.compile(r"[.!?…]+[\"')\]]*$")


def split_sentences(words: list[Word], pause_split: float = 0.8, max_words: int = 45) -> list[Sentence]:
    """Group words into sentences on terminal punctuation, long pauses or
    speaker changes. Sentence ends are the only places clips may start/stop,
    which is what keeps clips from being cut mid-thought."""
    sentences: list[Sentence] = []
    cur = Sentence()
    for i, w in enumerate(words):
        cur.words.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        boundary = (
            nxt is None
            or bool(_TERMINAL.search(w.text))
            or (nxt.start - w.end) >= pause_split
            or (nxt.speaker is not None and w.speaker is not None and nxt.speaker != w.speaker)
            or len(cur.words) >= max_words
        )
        if boundary:
            sentences.append(cur)
            cur = Sentence()
    return sentences
