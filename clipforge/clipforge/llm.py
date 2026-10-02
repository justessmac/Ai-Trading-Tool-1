"""Claude-powered moment picking.

Design choices from the research:
* The transcript goes in as numbered sentences, and Claude answers with
  sentence ids, never timestamps (LLMs are unreliable at timestamps;
  AutoClip / Spotify previews both do this). Code maps ids back to
  word-aligned times.
* Each sentence carries the multimodal flags the text can't show
  (LAUGH/REACTION, LOUD, CHAT-SPIKE), so Claude can see what landed with
  the room.
* Long transcripts are split into overlapping chunks to avoid
  "lost in the middle".
* Claude returns separate sub-scores; they're combined with weights in
  code so you can tune them against real performance data.
"""
from __future__ import annotations

import json
import sys

from pydantic import BaseModel, ValidationError

from .config import PlatformPreset
from .moments import Candidate
from .transcript import Sentence

DEFAULT_MODEL = "claude-opus-5-5"

SYSTEM_PROMPT = """You are a senior short-form video editor who turns long podcasts and livestreams into clips for TikTok, YouTube Shorts and Instagram Reels. You pick the moments most likely to be watched to the end, rewatched and shared by people who have never heard of the show.

What performs, in order of importance:
1. HOOK - the first sentence must stop the scroll on its own within ~3 seconds: a bold or contrarian claim, a surprising number, a direct question, high emotion, or the punchline itself. Viewers who don't know the speakers must instantly get why this is interesting. Never open on a greeting, a setup with no tension, "so", "and", "but", or a pronoun that refers to something earlier.
2. SELF-CONTAINED - a stranger must fully understand the clip without the rest of the episode. No unresolved "he/she/that/this/it" whose referent is outside the clip, no "like I said", no inside jokes.
3. ONE COMPLETE ARC - setup, tension, payoff. End right after the payoff (punchline, conclusion, reveal, laugh). Never end mid-thought or on a question that gets answered after the clip.
4. AROUSAL - high-arousal emotion is what gets shared: amusement, awe, surprise, outrage, anxiety, inspiration. Personal stories and heated disagreement beat dry information. Pure advice only works when it is surprising or very concrete.
5. QUOTABILITY - lines people would repeat, stitch, or argue about in the comments.

Sentences may carry flags from audio/chat analysis: LAUGH/REACTION (laughter or audience reaction right after), LOUD (raised voice vs. baseline), CHAT-SPIKE:<type> (livestream chat exploded). Treat them as strong evidence that something landed - especially for humour, where you should trust a LAUGH flag over your own sense of what is funny.

Never pick sponsor reads, ads, intros/outros, or housekeeping. Never pick moments whose appeal depends on sexualising anyone, harassment, or private information about non-public people.

Scoring (integers 0-10, be harsh and use the full range; most moments are a 3-6):
- hook: scroll-stopping power of the opening sentence
- flow: one complete, coherent arc with a satisfying ending
- value: entertainment, emotional or practical value to a stranger
- emotion: arousal intensity
- quotability: memorable/repeatable/debatable lines
- self_contained: understandable with zero context
- trend: ties to widely recognised people, topics or ongoing conversations

hook_sid: the single sentence (inside the clip) that would make the strongest cold open. Often it is the first sentence; if a later line is much stronger (the punchline or the boldest claim), give that id - the editor may play it first as a teaser.

title: an on-screen hook title, max 8 words, curiosity-driven but not misleading, no hashtags, no emoji.
description: a 1-2 sentence post caption. hashtags: 3-5 relevant tags without '#'.
dangling_refs: any words in the opening sentences that refer to context outside the clip (empty list if none)."""


class ClipPick(BaseModel):
    start_sid: int
    end_sid: int
    hook_sid: int
    title: str
    description: str
    hashtags: list[str]
    category: str
    hook: int
    flow: int
    value: int
    emotion: int
    quotability: int
    self_contained: int
    trend: int
    dangling_refs: list[str]
    is_ad: bool
    reasons: str


class ClipPicks(BaseModel):
    clips: list[ClipPick]


LLM_WEIGHTS = dict(hook=0.28, flow=0.18, value=0.14, emotion=0.14, quotability=0.1, self_contained=0.12, trend=0.04)


def _schema() -> dict:
    item = {
        "type": "object",
        "properties": {
            "start_sid": {"type": "integer"}, "end_sid": {"type": "integer"}, "hook_sid": {"type": "integer"},
            "title": {"type": "string"}, "description": {"type": "string"},
            "hashtags": {"type": "array", "items": {"type": "string"}},
            "category": {"type": "string", "enum": ["story", "hot_take", "funny", "insight", "advice",
                                                     "debate", "emotional", "reveal", "other"]},
            **{k: {"type": "integer"} for k in LLM_WEIGHTS},
            "dangling_refs": {"type": "array", "items": {"type": "string"}},
            "is_ad": {"type": "boolean"},
            "reasons": {"type": "string"},
        },
        "required": ["start_sid", "end_sid", "hook_sid", "title", "description", "hashtags", "category",
                     *LLM_WEIGHTS, "dangling_refs", "is_ad", "reasons"],
        "additionalProperties": False,
    }
    return {"type": "object", "properties": {"clips": {"type": "array", "items": item}},
            "required": ["clips"], "additionalProperties": False}


def _fmt_time(t: float) -> str:
    m, s = divmod(t, 60)
    return f"{int(m):02d}:{s:04.1f}"


def render_sentences(sentences: list[Sentence], flags: list[list[str]], lo: int, hi: int) -> str:
    lines = []
    for i in range(lo, hi):
        s = sentences[i]
        spk = f"{s.speaker}: " if s.speaker else ""
        fl = f"  [{', '.join(flags[i])}]" if flags[i] else ""
        lines.append(f"[{i}] ({_fmt_time(s.start)}) {spk}{s.text}{fl}")
    return "\n".join(lines)


def chunk_ranges(sentences: list[Sentence], chunk_seconds: float = 25 * 60,
                 overlap_seconds: float = 3 * 60) -> list[tuple[int, int]]:
    ranges, lo = [], 0
    n = len(sentences)
    while lo < n:
        t0 = sentences[lo].start
        hi = lo
        while hi < n and sentences[hi].end - t0 <= chunk_seconds:
            hi += 1
        hi = max(hi, lo + 1)
        ranges.append((lo, hi))
        if hi >= n:
            break
        nxt = hi
        while nxt > lo + 1 and sentences[hi - 1].end - sentences[nxt - 1].start < overlap_seconds:
            nxt -= 1
        lo = max(nxt, lo + 1)
    return ranges


def pick_with_claude(sentences: list[Sentence], flags: list[list[str]], preset: PlatformPreset,
                     max_len: float, per_chunk: int = 8, model: str = DEFAULT_MODEL,
                     effort: str = "medium", show_name: str | None = None) -> list[Candidate]:
    import anthropic

    client = anthropic.Anthropic()
    picks: list[Candidate] = []
    for lo, hi in chunk_ranges(sentences):
        user = (
            (f"Show: {show_name}\n" if show_name else "")
            + f"Platform: {preset.name}. Each clip must run between {preset.min_len:.0f} and {max_len:.0f} seconds "
            f"(ideal {preset.sweet_min:.0f}-{preset.sweet_max:.0f}s), measured from the start of start_sid to the end "
            f"of end_sid using the timestamps shown.\n"
            f"Propose up to {per_chunk} non-overlapping clips from the transcript below, best first. Fewer is fine if the "
            f"material is weak - do not pad with mediocre picks.\n\n<transcript>\n"
            + render_sentences(sentences, flags, lo, hi) + "\n</transcript>"
        )
        try:
            response = client.beta.messages.create(
                model=model,
                max_tokens=16000,
                betas=["server-side-fallback-2026-07-01"],
                fallbacks="default",
                cache_control={"type": "ephemeral"},
                output_config={"effort": effort, "format": {"type": "json_schema", "schema": _schema()}},
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user}],
            )
        except anthropic.AuthenticationError:
            raise RuntimeError("Claude API credentials not found - set ANTHROPIC_API_KEY or run with --no-llm")
        except anthropic.APIStatusError as e:
            print(f"  ! Claude request failed for sentences {lo}-{hi} ({e.status_code}): {e.message}", file=sys.stderr)
            continue
        except anthropic.APIConnectionError:
            print(f"  ! network error talking to Claude for sentences {lo}-{hi}", file=sys.stderr)
            continue
        if response.stop_reason == "refusal":
            print(f"  ! Claude declined sentences {lo}-{hi}; skipping that chunk", file=sys.stderr)
            continue
        text = next((b.text for b in response.content if b.type == "text"), "")
        try:
            result = ClipPicks.model_validate(json.loads(text))
        except (json.JSONDecodeError, ValidationError) as e:
            print(f"  ! unparseable response for sentences {lo}-{hi}: {e}", file=sys.stderr)
            continue
        for p in result.clips:
            c = _to_candidate(p, sentences, lo, hi)
            if c is not None:
                picks.append(c)
    return picks


def _to_candidate(p: ClipPick, sentences: list[Sentence], lo: int, hi: int) -> Candidate | None:
    if p.is_ad or not (lo <= p.start_sid <= p.end_sid < hi):
        return None
    hook = p.hook_sid if p.start_sid <= p.hook_sid <= p.end_sid else p.start_sid
    sub = {k: max(0, min(10, getattr(p, k))) / 10 for k in LLM_WEIGHTS}
    composite = sum(LLM_WEIGHTS[k] * v for k, v in sub.items()) / sum(LLM_WEIGHTS.values())
    if p.dangling_refs:
        composite -= 0.08
    c = Candidate(
        p.start_sid, p.end_sid, sentences[p.start_sid].start, sentences[p.end_sid].end,
        " ".join(s.text for s in sentences[p.start_sid:p.end_sid + 1]),
        title=p.title.strip() or None, hook_idx=hook, description=p.description,
        hashtags=[h.lstrip("#") for h in p.hashtags][:5],
        llm={"composite": max(composite, 0.0), "category": p.category, "reasons": p.reasons,
             "dangling_refs": p.dangling_refs, **{f"llm_{k}": v for k, v in sub.items()}},
    )
    return c
