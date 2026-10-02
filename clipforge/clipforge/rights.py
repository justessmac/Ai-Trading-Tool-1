"""Copyright safety.

This module keeps clips legitimately copyright-safe through permission and
licensing. It does NOT try to dodge Content ID or other matching systems
(no pitch-shifting, mirroring, speed tricks): those don't make a clip
legal, platforms treat them as evasion, and they don't count as
transformation either.

What it enforces:
1. Rights basis per source. Every export records why you're allowed to
   post it: you own it, you hold a written licence, or the owner runs a
   clipping programme you joined. With no basis the tool will analyse
   the video but won't render clips. Crediting the source is not
   permission, and there's no "30-second rule".
2. Licensed music only. Default is no added music (safest, and YouTube
   pays Shorts with no music a bigger share of the creator pool). Tracks
   come from a local library whose licences.json says commercial use is
   allowed on the target platform. In-app libraries (TikTok CML, Meta
   Sound Collection, YouTube's Shorts library) are only licensed inside
   their own app, so they can't be baked in here.
3. Third-party audio in the source. A creator's permission doesn't cover
   music or TV/sports audio they don't own. The tool flags clips with a
   continuous sound bed under speech (music, game audio, a TV) for
   review, or skips them with --strict-music.
4. YouTube's 1-minute rule. A Short over 60s with any active Content ID
   claim is blocked worldwide, so non-owned sources are capped at 59s.
5. Originality. Exports are clean (no third-party watermarks) and get
   real edits (captions, hook title, reframing, tightened pacing). The
   description carries a source credit, but a credit alone doesn't
   satisfy reused-content policies. Add your own commentary where you can.

Not legal advice. Fair use is a defence decided after the fact, not a
permission; don't build a channel on it.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

import numpy as np

from .audio import AudioEnvelope
from .transcript import Word

RIGHTS_BASES = {
    "owned": "You created/own this content (your own podcast or stream).",
    "licensed": "You hold a written licence or explicit written permission from the copyright owner.",
    "clipping-program": "The owner runs an official clipping programme/campaign you joined (e.g. Whop Content Rewards, "
                        "Vyro, a streamer's own clipping programme) whose terms allow this use.",
    "creative-commons": "The source is published under CC0 or CC BY (credit required). CC BY-NC does not cover "
                        "monetised posts, and ND licences don't allow edits at all.",
}


class RightsError(RuntimeError):
    pass


@dataclass
class RightsDeclaration:
    basis: str
    source_owner: str | None = None
    note: str | None = None          # licence ref, campaign URL, email date...
    credit: str | None = None        # e.g. "From The XYZ Podcast (@xyz)"

    def validate(self) -> None:
        if self.basis not in RIGHTS_BASES:
            raise RightsError(
                "Rendering is blocked until you state your right to use this video.\n"
                "Pass --rights with one of:\n"
                + "\n".join(f"  {k:17s} {v}" for k, v in RIGHTS_BASES.items())
                + "\nIf you don't have one of these, ask the creator for written permission or join their "
                  "clipping programme first. `clipforge analyze` still works without rights."
            )
        if self.basis != "owned" and not self.note:
            raise RightsError("--rights-note is required for licensed / clipping-program / creative-commons "
                              "sources (licence reference, campaign URL, or where the permission is recorded).")
        if self.basis == "creative-commons" and not self.credit:
            raise RightsError("--credit is required for creative-commons sources (CC BY requires attribution).")

    @property
    def owned(self) -> bool:
        return self.basis == "owned"


@dataclass
class MusicTrack:
    file: str
    title: str
    source: str
    license: str
    license_url: str
    commercial_use: bool
    platforms: list[str] = field(default_factory=lambda: ["tiktok", "shorts", "reels"])
    attribution: str | None = None   # text that must go in the description, if any

    def allowed_on(self, platform: str) -> bool:
        return self.commercial_use and platform in self.platforms


def load_music_library(folder: str | Path) -> list[MusicTrack]:
    """Read `licenses.json` in a music folder. Tracks without a licence
    entry are ignored - unknown licence = not cleared."""
    folder = Path(folder)
    manifest = folder / "licenses.json"
    if not manifest.exists():
        raise RightsError(f"{manifest} not found - every music track needs a licence entry (see music/README.md)")
    tracks = []
    for t in json.loads(manifest.read_text()):
        track = MusicTrack(**t)
        if not (folder / track.file).exists():
            raise RightsError(f"music file listed in licenses.json is missing: {track.file}")
        track.file = str(folder / track.file)
        tracks.append(track)
    return tracks


def pick_music(tracks: list[MusicTrack], platform: str, name: str | None = None) -> MusicTrack:
    allowed = [t for t in tracks if t.allowed_on(platform)]
    if name:
        allowed = [t for t in allowed if name.lower() in (t.title.lower(), Path(t.file).name.lower())]
    if not allowed:
        raise RightsError(f"no music track in the library is licensed for commercial use on {platform}"
                          + (f" matching '{name}'" if name else ""))
    return allowed[0]


def background_bed_ratio(env: AudioEnvelope, words: list[Word], min_gap: float = 0.25) -> float:
    """Share of the pauses between words where audio stays loud.

    Speech-only recordings drop close to the noise floor between phrases.
    Music, game audio or a TV keep playing through the pauses. A high ratio
    means a continuous sound bed is likely, which may be third-party
    copyrighted audio. A cheap heuristic that errs on the side of flagging.
    """
    gap_frames = []
    for a, b in zip(words, words[1:]):
        if b.start - a.end >= min_gap:
            gap_frames.append(env.slice(a.end + 0.05, b.start - 0.05))
    if not gap_frames:
        return 0.0
    frames = np.concatenate([g for g in gap_frames if len(g)]) if any(len(g) for g in gap_frames) else np.array([])
    if not len(frames):
        return 0.0
    loud = frames > env.speech_floor - 14.0
    return float(loud.mean())


def music_flag(env: AudioEnvelope | None, words: list[Word], threshold: float = 0.6) -> str | None:
    if env is None:
        return None
    ratio = background_bed_ratio(env, words)
    if ratio >= threshold:
        return (f"continuous background audio under speech ({ratio:.0%} of pauses stay loud) - possible music, "
                f"game audio or TV. Make sure that audio is cleared too; the creator's permission doesn't cover "
                f"third-party music.")
    return None


def max_length_for(platform: str, preset_max: float, rights: RightsDeclaration, flagged_audio: bool) -> float:
    """YouTube blocks Shorts over 60s worldwide when any Content ID claim
    lands, so stay at 59s unless the content is fully yours and clean."""
    if platform == "shorts" and (not rights.owned or flagged_audio):
        return min(preset_max, 59.0)
    return preset_max


def description_with_credit(description: str | None, hashtags: list[str], rights: RightsDeclaration,
                            music: MusicTrack | None) -> str:
    parts = [description.strip()] if description else []
    if rights.credit:
        parts.append(f"Source: {rights.credit}" + ("" if rights.owned else " - clipped with permission"))
    if music and music.attribution:
        parts.append(music.attribution)
    if hashtags:
        parts.append(" ".join(f"#{h}" for h in hashtags))
    return "\n\n".join(parts)


def write_manifest(path: str | Path, source: str, rights: RightsDeclaration, clip: dict,
                   music: MusicTrack | None, audio_flag: str | None, font: str) -> None:
    Path(path).write_text(json.dumps({
        "created": date.today().isoformat(),
        "source_file": source,
        "rights": asdict(rights),
        "rights_basis_meaning": RIGHTS_BASES[rights.basis],
        "clip": clip,
        "added_music": asdict(music) if music else None,
        "source_audio_review": audio_flag,
        "font": f"{font} (must be licensed for commercial video - OFL/Apache Google Fonts are fine)",
        "edits_applied": [e for e in ("9:16 reframe", "dead-air/filler removal", "burned-in captions",
                                      "hook title" if clip.get("title") else None,
                                      "cold-open teaser" if clip.get("cold_open") else None,
                                      "loudness normalisation") if e],
        "notes": "No detection-evasion processing is applied. Keep this file with the export as your record of permission.",
    }, indent=2))
