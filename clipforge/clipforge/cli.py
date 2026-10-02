"""clipforge command line.

  clipforge analyze  EPISODE.mp4                  # rank moments, no rendering
  clipforge render   EPISODE.mp4 --rights owned   # rank + render vertical clips
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import llm as llm_mod
from .config import PLATFORMS, Settings
from .pipeline import analyze, render_all, summary_table
from .rights import RIGHTS_BASES, RightsDeclaration, RightsError


def _common(p: argparse.ArgumentParser) -> None:
    p.add_argument("source", help="long-form video/audio file (podcast, stream VOD)")
    p.add_argument("-o", "--out", default=None, help="output folder (default: <source>_clips)")
    p.add_argument("-p", "--platform", choices=sorted(PLATFORMS), default="tiktok")
    p.add_argument("-n", "--clips", type=int, default=8, help="number of clips (default 8)")
    p.add_argument("--transcript", help="existing transcript (WhisperX/whisper JSON or SRT) to skip transcription")
    p.add_argument("--chat", help="livestream chat log (TwitchDownloader/chat-downloader JSON, CSV, or text)")
    p.add_argument("--whisper-model", default="small", help="faster-whisper model size (default small)")
    p.add_argument("--language", help="spoken language code, e.g. en (default: auto-detect)")
    p.add_argument("--no-llm", action="store_true", help="heuristic scoring only (no Claude API calls)")
    p.add_argument("--model", default=llm_mod.DEFAULT_MODEL, help=f"Claude model (default {llm_mod.DEFAULT_MODEL})")
    p.add_argument("--effort", default="medium", choices=["low", "medium", "high", "xhigh", "max"])
    p.add_argument("--llm-weight", type=float, default=0.6, help="share of the final score from Claude (0-1)")
    p.add_argument("--show", help="show / channel name, gives Claude context")
    p.add_argument("--max-len", type=float, help="override the platform's maximum clip length (seconds)")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="clipforge", description="Turn podcasts and streams into short-form clips.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("analyze", help="find and rank moments (no rendering, no rights needed)")
    _common(a)

    r = sub.add_parser("render", help="find moments and render vertical clips")
    _common(r)
    r.add_argument("--rights", choices=sorted(RIGHTS_BASES),
                   help="your legal basis for using this video (required): " +
                        "; ".join(f"{k} = {v}" for k, v in RIGHTS_BASES.items()))
    r.add_argument("--rights-note", help="licence reference / clipping-campaign URL / where permission is recorded")
    r.add_argument("--owner", help="copyright owner of the source")
    r.add_argument("--credit", help='credit line for post captions, e.g. "The XYZ Podcast (@xyz)"')
    r.add_argument("--music-dir", help="licensed music library folder with licenses.json (default: no music)")
    r.add_argument("--music", help="track title/file name from the library")
    r.add_argument("--strict-music", action="store_true",
                   help="skip clips where the source has a continuous sound bed (possible third-party music)")
    r.add_argument("--no-cold-open", action="store_true", help="don't play the strongest line first as a teaser")
    r.add_argument("--no-captions", action="store_true")
    r.add_argument("--no-titles", action="store_true", help="no on-screen hook title")
    r.add_argument("--title-seconds", type=float, help="show the hook title only for the first N seconds")
    r.add_argument("--layout", choices=["auto", "crop", "split", "blur"], default="auto")
    r.add_argument("--punch-in", type=float, default=0.0, metavar="SECONDS",
                   help="alternate a subtle zoom on cuts / every N seconds (0 = off, ~4 is typical)")
    r.add_argument("--font", help="caption font family (must be licensed for commercial video)")

    args = ap.parse_args(argv)
    settings = Settings(platform=args.platform, max_clips=args.clips)
    out = Path(args.out or f"{Path(args.source).with_suffix('')}_clips")

    rights = None
    if args.cmd == "render":
        rights = RightsDeclaration(args.rights or "", args.owner, args.rights_note, args.credit)
        try:
            rights.validate()  # fail before the slow steps
        except RightsError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
        settings.edit.layout = args.layout
        settings.edit.punch_in_every = args.punch_in
        settings.edit.title_seconds = args.title_seconds
        if args.font:
            settings.captions.font = args.font

    try:
        result = analyze(
            args.source, settings, out, transcript_path=args.transcript, chat_path=args.chat,
            use_llm=not args.no_llm, whisper_model=args.whisper_model, language=args.language,
            model=args.model, effort=args.effort, llm_weight=args.llm_weight, show_name=args.show,
            max_len=args.max_len,
        )
        print(summary_table(result.moments[: max(args.clips, 10)]))
        print(f"\nfull ranking: {out / 'moments.json'}")
        if args.cmd == "render":
            files = render_all(
                result, settings, out, rights, music_dir=args.music_dir, music_name=args.music,
                strict_music=args.strict_music, cold_open=not args.no_cold_open,
                captions=not args.no_captions, titles=not args.no_titles,
            )
            print(f"\nrendered {len(files)} clips to {out}/ (each with .json metadata + .rights.json record)")
    except (RightsError, RuntimeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
