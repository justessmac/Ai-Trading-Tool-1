# clipforge

Turn long-form podcasts and livestream VODs into short vertical clips for
TikTok, YouTube Shorts and Instagram Reels. It finds the moments most likely
to hold a stranger's attention, cuts them on clean sentence boundaries, and
renders captioned 1080x1920 videos. Copyright checks are built in.

The choices in the tool come from a research pass on platform ranking
signals, editing practice, highlight detection, existing AI clippers and
copyright. You can read the [research report](docs/research-report.md) and the
[source notes](docs/research-notes/).

> This is a standalone project. It lives in this repo for now but doesn't
> import anything from the trading bot, so the `clipforge/` folder can be
> moved to its own repo as-is.

## What it does

```
long video ─► transcript (word timestamps) ─► signals ─► candidate clips ─► score ─► render
              faster-whisper / your SRT        audio energy, laughter,   whole sentences   heuristics + Claude
                                               chat spikes (streams)     only, 15-120 s    sub-scores, deduped
```

**Finding moments**

- **Clean cuts.** Clips only start and end on sentence boundaries, never mid-thought. Openings that need earlier context are penalised, for example "so…", "he said…" or "like I said…".
- **Hook strength.** The opening sentence is scored for bold claims, questions, numbers, direct address, high-arousal words, length, and vocal energy in the first 3 s.
- **Payoff.** A clip should end on a complete sentence, followed by a pause or by laughter or a reaction.
- **Arousal.** Emotional language and personal-story markers raise the score, because high-arousal emotion predicts sharing (Berger & Milkman).
- **Audio.** Loudness spikes compared with the speaker's normal level, and loud bursts between words (laughter, applause) that Whisper doesn't transcribe.
- **Chat (streams).** Message-rate and emote spikes, lag-corrected by cross-correlating chat activity with the audio.
- **Claude (optional, on by default).** Claude reads the transcript as numbered sentences, annotated with the audio and chat flags. It returns clip picks by sentence id, plus sub-scores, a hook title, a post caption and hashtags. Those sub-scores are blended with the measured signals, at 60/40 by default.
- **Penalties.** Sponsor reads, intros and outros, and low ASR confidence are penalised. Clips that overlap by more than 30% are deduplicated.

**Editing each clip**

- **Pacing.** Dead air is tightened (gaps over 0.45 s are cut down to 0.18 s) and "um"/"uh" are removed, with tiny audio fades so there are no clicks.
- **Cold open (optional).** If a later line is the strongest hook, it plays first as a teaser.
- **9:16 reframing.**
  - A face-centred crop for one speaker.
  - A split screen for side-by-side two-person shots.
  - A blurred-background fit for screen shares or gameplay.
  - Plain scaling if the source is already vertical.
- **Punch-in zooms (optional).** A small zoom on jump cuts.
- **Captions.** Animated word-by-word captions: 1-3 words at a time, the spoken word highlighted, and numbers and strong words in a second colour. They sit inside the safe zone that clears the TikTok, Reels and Shorts UI (x 60-940, y 210-1436).
- **Hook title.** Shown at the top when Claude is used.
- **Loudness.** Normalised to -14 LUFS with a -1 dB true peak.
- **Export.** H.264 High at 30 fps, closed GOP, AAC 48 kHz, faststart. One master file works on all three platforms.

## Install

Requires Python 3.10+ and ffmpeg (with libass, which standard builds include).

```bash
cd clipforge
pip install -r requirements.txt            # numpy, pydantic, anthropic
pip install faster-whisper                 # transcription (skip if you bring your own transcript)
pip install 'opencv-python-headless<5'     # face tracking for crop/split layouts (optional)
export ANTHROPIC_API_KEY=...               # optional; use --no-llm without it
```

## Use

```bash
# 1. Rank the best moments (no rendering, nothing posted)
python -m clipforge analyze episode.mp4 --platform tiktok --show "My Podcast"

# 2. Render the top 8 clips from your own podcast
python -m clipforge render episode.mp4 --rights owned --credit "My Podcast (@mypod)"

# Someone else's stream you have permission to clip, with chat signals
python -m clipforge render vod.mp4 --chat chat.json --platform shorts \
    --rights clipping-program --rights-note "https://whop.com/... campaign" \
    --credit "StreamerName on Twitch" --strict-music

# Without Claude (free, offline heuristics only), using an existing transcript
python -m clipforge render episode.mp4 --transcript episode.srt --no-llm --rights owned
```

Output goes to `<source>_clips/` by default. Every clip comes with:

- `NN_title.mp4`: the clip.
- `NN_title.jpg`: a cover frame.
- `NN_title.json`: the score, sub-scores, reasons, and a ready-to-paste post caption with credit and hashtags.
- `NN_title.rights.json`: your record of the rights basis, any music licence, and any source-audio review flags.
- `moments.json`: the full ranking. `transcript.json` is cached, so later runs skip transcription.

Useful flags:

| Flag | What it does |
|---|---|
| `-p tiktok\|shorts\|reels` | Sets the length window: TikTok 15-120 s (sweet spot 25-45 s), Shorts 15-59 s, Reels 15-90 s. |
| `-n 8` | Number of clips. |
| `--layout auto\|crop\|split\|blur` | Sets the reframing mode. |
| `--punch-in 4` | Alternates a subtle zoom on cuts and every ~4 s. |
| `--no-cold-open` | Turns off the teaser line at the start. |
| `--title-seconds 3` | Shows the hook title only for the first 3 s. |
| `--effort low..max`, `--model` | Sets Claude's thinking depth and model. The default is `claude-opus-5-5` at medium effort. |
| `--llm-weight 0.6` | Sets how much of the final score comes from Claude versus the measured signals. |

## Copyright: keeping clips legitimately safe

The tool keeps clips copyright-safe through permission and licensing. It
does **not** try to dodge detection: there's no pitch shifting, mirroring or
speed tricks. Those don't make a clip legal, platforms treat them as
evasion, and they don't count as transformation either.

1. **No rights, no render.** `render` requires `--rights`:
   - `owned`: your own show.
   - `licensed`: written permission from the owner.
   - `clipping-program`: the owner's official clipping campaign, such as Whop Content Rewards, Vyro, or a streamer's own programme.
   - `creative-commons`: CC0 or CC BY.

   Everything except `owned` also needs `--rights-note` saying where the permission is recorded. Crediting a creator is not permission, and there is no "30-second rule". `analyze` works on anything.
2. **No added music by default.** Music is the most common cause of claims. Clips with no music also get a larger share of YouTube's Shorts creator pool. If you want music, use `--music-dir` pointing to a folder with a `licenses.json`; only tracks marked for commercial use on that platform are used. In-app music libraries (TikTok's Commercial Music Library, Meta Sound Collection, YouTube's Shorts library) are licensed only inside their own apps. Add those sounds in the app when you post, not here. See [music/README.md](music/README.md).
3. **Third-party audio in the source gets flagged.** A creator's permission doesn't cover music, TV or game audio they don't own. Clips with a continuous sound bed under the speech are flagged for review in their `.json`. `--strict-music` skips them instead.
4. **YouTube's one-minute rule.** A Short over 60 s with *any* Content ID claim is blocked worldwide. Shorts are capped at 59 s unless the source is `owned` and has no flagged audio.
5. **Originality.** YouTube, Meta and TikTok all down-rank or demonetise lightly edited reposts. Exports carry no third-party watermarks and get real edits (captions, hook title, reframing, tightened pacing). Near-duplicate clips are dropped. Adding your own commentary or context is still the strongest originality signal.
6. **Assets.** The caption font is Montserrat Black under the SIL Open Font License (`fonts/OFL.txt`), which is fine for commercial video. If you switch fonts with `--font`, use one licensed for commercial video.

This is not legal advice. Fair use is a defence decided after the fact, not a
permission, so don't build a channel on it.

## How to make the scores better over time

No platform publishes ranking weights, and no clipping vendor has shown its
"virality score" predicts views. Treat the 0-100 score as a ranking aid.

- Log how each posted clip performs (YouTube *engaged views*, Reels skip rate, TikTok average watch time). Normalise per account, because follower count dominates raw views.
- Tune `ScoringWeights` in `clipforge/config.py` and `LLM_WEIGHTS` in `clipforge/llm.py`. Each clip's `.json` stores its sub-scores, so you can fit weights against outcomes.
- The first A/B test worth running is cold open on versus off (`--no-cold-open`). There is no published controlled data on it.

## Limits

- **Face tracking** uses OpenCV's Haar cascade with one static crop per clip. Fast camera switches or more than two people may need `--layout blur`. Active-speaker detection (TalkNet, ClipsAI-style diarization) would be the upgrade.
- **Laughter and music detection** are energy heuristics. Swapping in YAMNet or PANNs would make them more precise, at the cost of a TensorFlow or PyTorch dependency.
- **Transcription** runs on CPU by default. A 1-hour episode with the `small` model takes a few minutes. Pass `--transcript` to reuse WhisperX or other transcripts.

## Tests

```bash
cd clipforge && python -m pytest -q
```

The tests synthesise a fake podcast with ffmpeg, then render real clips in each layout. They also check the exact Claude API request against a local mock server, so no API key is needed.
