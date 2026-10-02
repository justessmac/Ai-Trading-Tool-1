"""End-to-end: long video -> ranked moments -> rendered vertical clips."""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


from . import llm as llm_mod
from .audio import envelope_from_file, per_second, reaction_events
from .captions import build_ass
from .chat import ChatTrack, load_chat
from .config import Settings
from .media import probe, require_ffmpeg
from .moments import Candidate, Signals, find_moments, score_candidate, select, sentence_flags
from .reframe import choose_layout, detect_faces
from .render import extract_cover, render_clip
from .rights import (MusicTrack, RightsDeclaration, description_with_credit, load_music_library,
                     max_length_for, music_flag, pick_music, write_manifest)
from .timeline import build_cutlist, with_cold_open
from .transcript import Transcript, split_sentences, transcribe


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


@dataclass
class Analysis:
    source: str
    transcript: Transcript
    sentences: list
    signals: Signals
    moments: list[Candidate]


def _fit_length(c: Candidate, sentences, min_len: float, max_len: float) -> Candidate | None:
    """Trim/extend an LLM pick on sentence boundaries to fit the platform,
    keeping its hook line inside."""
    i, j = c.start_idx, c.end_idx
    while sentences[j].end - sentences[i].start > max_len and j > i:
        if c.hook_idx is not None and j - 1 < c.hook_idx and i < c.hook_idx:
            i += 1
        else:
            j -= 1
    while sentences[j].end - sentences[i].start < min_len and j + 1 < len(sentences):
        if sentences[j + 1].end - sentences[i].start > max_len:
            break
        j += 1
    dur = sentences[j].end - sentences[i].start
    if not (min_len <= dur <= max_len):
        return None
    if (i, j) != (c.start_idx, c.end_idx):
        c.start_idx, c.end_idx = i, j
        c.start, c.end = sentences[i].start, sentences[j].end
        c.text = " ".join(s.text for s in sentences[i:j + 1])
        if c.hook_idx is not None and not (i <= c.hook_idx <= j):
            c.hook_idx = i
    return c


def analyze(source: str, settings: Settings, out_dir: Path, transcript_path: str | None = None,
            chat_path: str | None = None, use_llm: bool = True, whisper_model: str = "small",
            language: str | None = None, model: str = llm_mod.DEFAULT_MODEL, effort: str = "medium",
            llm_weight: float = 0.6, show_name: str | None = None, max_len: float | None = None) -> Analysis:
    require_ffmpeg()
    info = probe(source)
    if not info.has_audio:
        raise RuntimeError("source has no audio track")
    out_dir.mkdir(parents=True, exist_ok=True)

    cached = out_dir / "transcript.json"
    if transcript_path:
        log(f"- loading transcript {transcript_path}")
        transcript = Transcript.load(transcript_path)
    elif cached.exists():
        log(f"- reusing {cached}")
        transcript = Transcript.load(cached)
    else:
        log(f"- transcribing with faster-whisper ({whisper_model}); this is the slow step")
        transcript = transcribe(source, whisper_model, language)
    transcript.save(cached)
    if not transcript.words:
        raise RuntimeError("transcript is empty")

    log("- analysing audio")
    env = envelope_from_file(source)
    reactions = reaction_events(env, transcript.words)
    chat = None
    if chat_path:
        log(f"- loading chat {chat_path}")
        chat = ChatTrack.build(load_chat(chat_path), max(info.duration, transcript.duration))
        lag = chat.estimate_lag(per_second(env))
        log(f"  chat lag estimated at {lag:.0f}s")
    sig = Signals(env, chat, reactions)

    sentences = split_sentences(transcript.words)
    preset = settings.preset
    max_len = min(max_len or preset.max_len, preset.max_len)
    log(f"- {len(transcript.words)} words, {len(sentences)} sentences, {len(reactions)} reaction events")

    heuristic = find_moments(sentences, sig, preset, settings.weights, k=max(settings.max_clips * 3, 20),
                             max_overlap=settings.max_overlap, max_len=max_len)
    moments = heuristic
    if use_llm:
        log(f"- asking Claude ({model}) to pick moments")
        flags = sentence_flags(sentences, sig)
        picks = llm_mod.pick_with_claude(sentences, flags, preset, max_len, model=model, effort=effort,
                                         show_name=show_name)
        fused: list[Candidate] = []
        for c in picks:
            c = _fit_length(c, sentences, preset.min_len, max_len)
            if c is None:
                continue
            score_candidate(c, sentences, sig, preset, settings.weights)
            heur = c.score
            c.scores["heuristic"] = heur / 100
            c.scores.update({k: v for k, v in c.llm.items() if k.startswith("llm_")})
            c.score = round(llm_weight * 100 * c.llm["composite"] + (1 - llm_weight) * heur, 1)
            c.reasons = [c.llm["reasons"]] + c.reasons
            fused.append(c)
        if fused:
            moments = fused
        else:
            log("  ! Claude returned no usable picks - falling back to heuristic ranking")
    ranked = select(moments, k=max(settings.max_clips * 2, 10), max_overlap=settings.max_overlap)

    (out_dir / "moments.json").write_text(json.dumps([{
        "rank": n + 1, "score": c.score, "start": round(c.start, 2), "end": round(c.end, 2),
        "duration": round(c.duration, 1), "title": c.title, "hook_sentence": c.hook_idx,
        "reasons": c.reasons, "scores": {k: round(v, 3) for k, v in c.scores.items()},
        "description": c.description, "hashtags": c.hashtags, "text": c.text,
    } for n, c in enumerate(ranked)], indent=2))
    return Analysis(source, transcript, sentences, sig, ranked)


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40] or "clip"


def render_all(a: Analysis, settings: Settings, out_dir: Path, rights: RightsDeclaration,
               music_dir: str | None = None, music_name: str | None = None, strict_music: bool = False,
               cold_open: bool = True, captions: bool = True, titles: bool = True) -> list[Path]:
    rights.validate()
    info = probe(a.source)
    preset = settings.preset
    music: MusicTrack | None = None
    if music_dir:
        music = pick_music(load_music_library(music_dir), preset.name, music_name)
        log(f"- music: {music.title} ({music.license})")

    outputs: list[Path] = []
    for c in a.moments:
        if len(outputs) >= settings.max_clips:
            break
        words = [w for s in a.sentences[c.start_idx:c.end_idx + 1] for w in s.words]
        flag = music_flag(a.signals.env, words)
        if flag and strict_music:
            log(f"  skip {c.start:.0f}s: {flag}")
            continue
        limit = max_length_for(preset.name, preset.max_len, rights, bool(flag))
        if c.duration > limit:
            fitted = _fit_length(c, a.sentences, preset.min_len, limit)
            if fitted is None:
                log(f"  skip {c.start:.0f}s: can't fit under {limit:.0f}s")
                continue
            words = [w for s in a.sentences[c.start_idx:c.end_idx + 1] for w in s.words]

        cut = build_cutlist(words, settings.edit)
        hook_used = False
        if cold_open and c.hook_idx is not None and c.hook_idx != c.start_idx:
            hook = a.sentences[c.hook_idx]
            if hook.end - hook.start <= 7.0 and cut.duration + (hook.end - hook.start) <= limit:
                cut = with_cold_open(hook.words, cut, settings.edit)
                hook_used = True

        n = len(outputs) + 1
        name = f"{n:02d}_{_slug(c.title or c.text[:40])}"
        log(f"- rendering {name} ({cut.duration:.1f}s, score {c.score})")

        faces = detect_faces(a.source, c.start, min(c.end, c.start + 30), info) if info.has_video else None
        layout = choose_layout(faces, info, settings.edit.layout)
        ass = build_ass(cut.words if captions else [], settings.captions, cut.duration,
                        title=(c.title if titles else None), title_seconds=settings.edit.title_seconds) \
            if (captions or (titles and c.title)) else None
        out = out_dir / f"{name}.mp4"
        render_clip(a.source, info, cut.segments, layout, ass, out, settings.edit, music)
        extract_cover(out, out_dir / f"{name}.jpg")

        meta = {
            "rank": n, "score": c.score, "source_start": round(c.start, 2), "source_end": round(c.end, 2),
            "duration": round(cut.duration, 2), "title": c.title, "cold_open": hook_used, "layout": layout.kind,
            "reasons": c.reasons, "scores": {k: round(v, 3) for k, v in c.scores.items()},
            "post_caption": description_with_credit(c.description, c.hashtags, rights, music),
            "transcript": c.text,
        }
        if flag:
            meta["review"] = flag
            log(f"  ! review: {flag}")
        (out_dir / f"{name}.json").write_text(json.dumps(meta, indent=2))
        write_manifest(out_dir / f"{name}.rights.json", a.source, rights, meta, music, flag, settings.captions.font)
        outputs.append(out)
    return outputs


def summary_table(moments: list[Candidate]) -> str:
    rows = ["rank  score  start    dur   title / opening line", "-" * 78]
    for n, c in enumerate(moments, 1):
        m, s = divmod(c.start, 60)
        label = c.title or c.text[:48]
        rows.append(f"{n:>4}  {c.score:>5.1f}  {int(m):02d}:{s:04.1f}  {c.duration:4.0f}s  {label}")
        if c.reasons:
            rows.append(f"{'':24}why: {'; '.join(r for r in c.reasons[:3] if r)[:100]}")
    return "\n".join(rows)
