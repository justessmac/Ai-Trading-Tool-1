"""Find and score clip-worthy moments.

Candidates are always whole sentences (never mid-thought). Each candidate
gets a set of 0-1 sub-scores, combined with tunable weights into a 0-100
score. Sub-scores are kept separate (and explained) so you can calibrate
the weights against how your posted clips actually perform.

Signals used, roughly in order of evidence strength (see the report):
  hook        - first sentence: claim / question / number / "you" / emotion,
                short and punchy, starts loud
  standalone  - doesn't open on a connective or unresolved reference
  payoff      - ends on a complete sentence, followed by laughter/pause
  emotion     - high-arousal language and personal story markers
                (arousal predicts sharing: Berger & Milkman 2012)
  energy      - vocal loudness vs the speaker's baseline + dynamics
  reactions   - laughter / applause (loud non-speech) inside or right after
  chat        - lag-corrected chat-rate spike (livestreams)
  pacing      - words per second inside a lively band, little dead air
  duration    - fit to the platform's sweet spot
Penalties: sponsor reads, low ASR confidence.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

import numpy as np

from .audio import AudioEnvelope
from .chat import ChatTrack
from .config import PlatformPreset, ScoringWeights
from .transcript import Sentence

CONNECTIVES = {"and", "but", "so", "because", "which", "also", "or", "then", "plus", "anyway",
               "anyways", "like", "yeah", "right", "okay", "ok", "well", "um", "uh", "cause", "'cause"}
DANGLING = re.compile(
    r"^(he|she|they|them|him|her|it|that|this|those|these|there|which|who)\b|"
    r"\b(like i said|as i said|as we said|like we said|as we discussed|we talked about|earlier|"
    r"going back to|to your point|that's what i|exactly that|same thing)\b", re.I)
HOOK_PATTERNS = re.compile(
    r"\b(never|always|nobody|no one|everyone|everybody|the truth|truth is|secret|biggest|worst|best|"
    r"mistake|wrong|lie|lied|actually|here's why|here's the thing|the reason|i can't believe|"
    r"you won't believe|stop|don't|if you|you need|you have to|you're|most people|"
    r"what if|imagine|crazy|insane|million|billion|fired|quit|died|almost|confession|honestly|"
    r"unpopular opinion|hot take|controversial)\b", re.I)
AROUSAL = re.compile(
    r"\b(love|hate|furious|angry|pissed|scared|terrified|shocked|amazing|incredible|insane|crazy|"
    r"unbelievable|disgusting|ridiculous|hilarious|wild|brutal|devastating|heartbroken|cried|"
    r"screamed|panic|obsessed|destroyed|fight|war|kill|dead|died|crying|fuck\w*|shit|damn|holy|"
    r"oh my god|omg|wow|whoa|dude|bro)\b", re.I)
STORY = re.compile(r"\b(i remember|one time|so i was|true story|when i was|my (dad|mom|wife|husband|"
                   r"brother|sister|friend|boss)|i was like|she was like|he was like|turns out|"
                   r"and then|the next day|all of a sudden|suddenly)\b", re.I)
SPONSOR = re.compile(r"\b(sponsor\w*|promo code|use code|discount code|link in (the )?(description|bio)|"
                     r"brought to you by|today's episode is|check out|sign up|free trial|percent off|% off)\b", re.I)

HOUSEKEEPING = re.compile(r"\b(welcome (back )?to|welcome back|thanks for (having|joining)|subscribe|hit the bell|"
                          r"like and subscribe|right back|quick break|after the break|see you next|that's (all|it) for|"
                          r"follow (us|me) on|patreon)\b", re.I)


@dataclass
class Candidate:
    start_idx: int
    end_idx: int                     # inclusive sentence index
    start: float
    end: float
    text: str
    scores: dict[str, float] = field(default_factory=dict)
    score: float = 0.0
    reasons: list[str] = field(default_factory=list)
    title: str | None = None
    hook_idx: int | None = None
    description: str | None = None
    hashtags: list[str] = field(default_factory=list)
    llm: dict | None = None

    @property
    def duration(self) -> float:
        return self.end - self.start


@dataclass
class Signals:
    env: AudioEnvelope | None = None
    chat: ChatTrack | None = None
    reactions: list[tuple[float, float]] = field(default_factory=list)

    def __post_init__(self) -> None:
        r = sorted(self.reactions)
        self._rt = np.array([t for t, _ in r])
        self._rcum = np.concatenate([[0.0], np.cumsum([st for _, st in r])])

    def stats(self, sentences: list[Sentence]) -> "SentenceStats":
        cache = self.__dict__.setdefault("_stats_cache", {})
        key = (id(sentences), len(sentences))
        if key not in cache:
            cache[key] = SentenceStats(sentences, self)
        return cache[key]

    def reactions_between(self, start: float, end: float) -> tuple[int, float]:
        """(count, total strength) of reaction events in [start, end]."""
        lo, hi = np.searchsorted(self._rt, start, "left"), np.searchsorted(self._rt, end, "right")
        return int(hi - lo), float(self._rcum[hi] - self._rcum[lo])


def _clip01(x: float) -> float:
    return float(min(max(x, 0.0), 1.0))


def sentence_flags(sentences: list[Sentence], sig: Signals) -> list[list[str]]:
    """Per-sentence multimodal annotations, shown to the LLM so it can see
    what text alone can't (laughs, raised voices, chat explosions)."""
    flags: list[list[str]] = []
    react_t = np.array([t for t, _ in sig.reactions]) if sig.reactions else np.array([])
    for i, s in enumerate(sentences):
        f: list[str] = []
        nxt_start = sentences[i + 1].start if i + 1 < len(sentences) else s.end + 2
        if len(react_t) and np.any((react_t >= s.start) & (react_t <= nxt_start + 1.0)):
            f.append("LAUGH/REACTION")
        if sig.env is not None and sig.env.energy_z(s.start, s.end) > 1.2:
            f.append("LOUD")
        if sig.chat is not None and sig.chat.spike_z(s.start, s.end) > 2.0:
            cat, _ = sig.chat.dominant_reaction(s.start, s.end)
            f.append(f"CHAT-SPIKE{':' + cat if cat else ''}")
        flags.append(f)
    return flags


class SentenceStats:
    """Per-sentence features computed once, with prefix sums so scoring
    each of the tens of thousands of candidate windows is O(1)."""

    def __init__(self, sentences: list[Sentence], sig: Signals):
        n = len(sentences)
        arousal, story, excl, earlier, sponsor = (np.zeros(n) for _ in range(5))
        n_words, speech, prob, loud, dur = (np.zeros(n) for _ in range(5))
        self.hook: list[tuple[float, list[str]]] = []
        for i, st in enumerate(sentences):
            t = st.text
            arousal[i] = len(AROUSAL.findall(t))
            story[i] = len(STORY.findall(t))
            excl[i] = t.count("!")
            earlier[i] = bool(EARLIER.search(t))
            sponsor[i] = bool(SPONSOR.search(t))
            n_words[i] = len(st.words)
            speech[i] = sum(w.end - w.start for w in st.words)
            prob[i] = sum(w.prob for w in st.words)
            dur[i] = max(st.end - st.start, 1e-3)
            if sig.env is not None:
                loud[i] = float(np.percentile(sig.env.slice(st.start, st.end), 90))
            self.hook.append(_hook_score(st, sig))
        cum = lambda a: np.concatenate([[0.0], np.cumsum(a)])
        self.arousal, self.story, self.excl, self.earlier, self.sponsor = map(cum, (arousal, story, excl, earlier, sponsor))
        self.n_words, self.speech, self.prob = map(cum, (n_words, speech, prob))
        self.loud_w, self.loud2_w, self.dur = cum(loud * dur), cum(loud * loud * dur), cum(dur)

    @staticmethod
    def span(arr: np.ndarray, i: int, j: int) -> float:
        return float(arr[j + 1] - arr[i])

    def loudness(self, i: int, j: int) -> tuple[float, float]:
        """Duration-weighted mean and std of per-sentence loudness (dB)."""
        d = self.span(self.dur, i, j)
        mean = self.span(self.loud_w, i, j) / d
        var = max(self.span(self.loud2_w, i, j) / d - mean * mean, 0.0)
        return mean, var ** 0.5


EARLIER = re.compile(r"\b(like i said|as i said|we talked about|earlier)\b", re.I)


def generate_candidates(sentences: list[Sentence], preset: PlatformPreset, max_len: float | None = None,
                        stride: int = 1) -> list[Candidate]:
    max_len = max_len or preset.max_len
    out: list[Candidate] = []
    for i in range(0, len(sentences), stride):
        first = sentences[i].words[0].text.lower().strip(",.!?\"'")
        if first in CONNECTIVES and len(sentences[i].words) < 4:
            continue
        for j in range(i, len(sentences)):
            dur = sentences[j].end - sentences[i].start
            if dur > max_len:
                break
            if dur >= preset.min_len:
                out.append(Candidate(i, j, sentences[i].start, sentences[j].end,
                                     " ".join(s.text for s in sentences[i:j + 1])))
    return out


def _hook_score(first: Sentence, sig: Signals) -> tuple[float, list[str]]:
    text = first.text
    s, why = 0.15, []
    n_words = len(first.words)
    if HOOK_PATTERNS.search(text):
        s += 0.3
        why.append("opens with a bold claim/trigger phrase")
    if text.rstrip().endswith("?"):
        s += 0.2
        why.append("opens with a question")
    if re.search(r"\d", text):
        s += 0.1
    if re.search(r"\byou\b", text, re.I):
        s += 0.1
    if AROUSAL.search(text):
        s += 0.15
    if 4 <= n_words <= 16:
        s += 0.1
    elif n_words > 30:
        s -= 0.15
    if sig.env is not None:
        s += 0.1 * _clip01(sig.env.energy_z(first.start, min(first.end, first.start + 3)))
    if first.words[0].text.lower().strip(",.") in CONNECTIVES:
        s -= 0.25
    return _clip01(s), why


def score_candidate(c: Candidate, sentences: list[Sentence], sig: Signals, preset: PlatformPreset,
                    weights: ScoringWeights) -> Candidate:
    i, j = c.start_idx, c.end_idx
    first, last = sentences[i], sentences[j]
    st = sig.stats(sentences)
    span = st.span
    reasons: list[str] = []

    hook, why = st.hook[i]
    reasons += why

    # Standalone: penalise openers that depend on earlier context.
    standalone = 1.0
    if first.words[0].text.lower().strip(",.") in CONNECTIVES:
        standalone -= 0.35
    if DANGLING.search(first.text):
        standalone -= 0.4
    if span(st.earlier, i, j):
        standalone -= 0.2
    standalone = _clip01(standalone)
    if standalone < 0.5:
        reasons.append("may depend on earlier context")

    # Payoff: complete final sentence, and a beat after it.
    payoff = 0.3
    if re.search(r"[.!?]$", last.text.strip()):
        payoff += 0.25
    nxt = sentences[c.end_idx + 1] if c.end_idx + 1 < len(sentences) else None
    if nxt is None or nxt.start - last.end >= 0.6 or (nxt.speaker and nxt.speaker != last.speaker):
        payoff += 0.15
    if sig.reactions_between(last.start - 1, last.end + 2.5)[0]:
        payoff += 0.3
        reasons.append("ends on a laugh/reaction")
    payoff = _clip01(payoff)

    # Emotion / narrative.
    n_arousal = span(st.arousal, i, j)
    n_story = span(st.story, i, j)
    emotion = _clip01(0.12 * n_arousal + 0.12 * n_story + 0.1 * span(st.excl, i, j))
    if n_story:
        reasons.append("personal story")
    if n_arousal >= 3:
        reasons.append("high-arousal language")

    energy = 0.0
    if sig.env is not None:
        mean_db, std_db = st.loudness(i, j)
        z = (mean_db - sig.env.speech_floor) / sig.env.spread
        energy = _clip01(0.5 + 0.25 * z) * 0.7 + _clip01(std_db / sig.env.spread / 1.5) * 0.3
        if z > 1.0:
            reasons.append("raised voices / high energy")

    n_react, strength = sig.reactions_between(c.start, c.end + 2.0)
    reactions = _clip01(strength / 4.0)
    if n_react >= 2:
        reasons.append(f"{n_react} laughs/reactions")

    chat = 0.0
    if sig.chat is not None:
        z = sig.chat.spike_z(c.start, c.end)
        chat = _clip01(z / 4.0)
        if z > 2.0:
            cat, _ = sig.chat.dominant_reaction(c.start, c.end)
            reasons.append(f"chat spike ({cat or 'activity'})")

    n_words = span(st.n_words, i, j)
    speech_time = span(st.speech, i, j)
    wps = n_words / max(c.duration, 1e-6)
    density = speech_time / max(c.duration, 1e-6)
    pacing = _clip01(1 - abs(wps - 3.0) / 2.0) * 0.6 + _clip01(density) * 0.4

    d = c.duration
    if preset.sweet_min <= d <= preset.sweet_max:
        duration_fit = 1.0
    elif d < preset.sweet_min:
        duration_fit = _clip01((d - preset.min_len) / max(preset.sweet_min - preset.min_len, 1))
    else:
        duration_fit = _clip01(1 - (d - preset.sweet_max) / max(preset.max_len - preset.sweet_max, 1))

    scores = dict(hook=hook, standalone=standalone, payoff=payoff, emotion=emotion, energy=energy,
                  reactions=reactions, chat=chat, pacing=pacing, duration_fit=duration_fit)
    wsum = 0.0
    total = 0.0
    for k, v in scores.items():
        w = getattr(weights, k)
        if k == "chat" and sig.chat is None:
            continue  # don't punish podcasts for having no chat
        if k in ("energy",) and sig.env is None:
            continue
        total += w * v
        wsum += w
    total /= max(wsum, 1e-9)

    penalty = 0.0
    if span(st.sponsor, i, j):
        penalty += 0.35
        reasons.append("looks like an ad read (penalised)")
    if HOUSEKEEPING.search(first.text) or HOUSEKEEPING.search(last.text):
        penalty += 0.25
        reasons.append("intro/outro housekeeping (penalised)")
    mean_prob = span(st.prob, i, j) / n_words if n_words else 1.0
    if mean_prob < 0.6:
        penalty += 0.15
    c.scores = scores
    c.score = round(100 * _clip01(total - penalty), 1)
    c.reasons = reasons
    return c


def overlap(a: Candidate, b: Candidate) -> float:
    inter = max(0.0, min(a.end, b.end) - max(a.start, b.start))
    return inter / max(min(a.duration, b.duration), 1e-6)


def select(cands: list[Candidate], k: int, max_overlap: float) -> list[Candidate]:
    """Greedy non-maximum suppression - near-duplicate clips get
    down-ranked by platforms, so never export two that share much content."""
    chosen: list[Candidate] = []
    for c in sorted(cands, key=lambda c: c.score, reverse=True):
        if all(overlap(c, o) <= max_overlap for o in chosen):
            chosen.append(c)
        if len(chosen) >= k:
            break
    return chosen


def find_moments(sentences: list[Sentence], sig: Signals, preset: PlatformPreset, weights: ScoringWeights,
                 k: int, max_overlap: float, max_len: float | None = None) -> list[Candidate]:
    cands = generate_candidates(sentences, preset, max_len)
    for c in cands:
        score_candidate(c, sentences, sig, preset, weights)
    return select(cands, k, max_overlap)
