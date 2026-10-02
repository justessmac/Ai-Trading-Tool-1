"""Platform presets and tunable defaults.

Numbers here come from the research report in
`docs/research-report.md`; where research only
found practitioner consensus (not platform data) that's noted inline so
you know what's safe to tune.
"""
from __future__ import annotations

from dataclasses import dataclass, field

# 1080x1920 vertical canvas.
WIDTH, HEIGHT = 1080, 1920

# Conservative cross-platform safe area (union of TikTok / Reels / Shorts UI
# overlays, third-party measurements): keep text inside x 60-940, y 210-1436.
# TikTok's right-hand action rail and bottom caption area are the binding
# constraints.
SAFE_LEFT, SAFE_RIGHT, SAFE_TOP, SAFE_BOTTOM = 60, 940, 210, 1436


@dataclass(frozen=True)
class PlatformPreset:
    name: str
    min_len: float
    max_len: float
    # Lengths inside the sweet spot get full duration score; outside it
    # (but inside min/max) the score tapers linearly.
    sweet_min: float
    sweet_max: float
    # Hard cap when the source isn't fully owned. YouTube blocks Shorts
    # over 1 minute worldwide if any Content ID claim lands on them.
    unowned_max_len: float | None = None


PLATFORMS: dict[str, PlatformPreset] = {
    # OpusClip (13.5M clips): viral TikTok median is 41s. Buffer (1.1M
    # videos): >60s gets more reach. Socialinsider: <30s gets the highest
    # engagement rate. Favour 25-45s, allow up to 2 min for strong stories.
    "tiktok": PlatformPreset("tiktok", 15, 120, 25, 45),
    # Shorts allow 3 min, but 30-59s is the safe default.
    "shorts": PlatformPreset("shorts", 15, 59, 30, 58, unowned_max_len=59),
    # Reels: 15-60s, 90s soft max.
    "reels": PlatformPreset("reels", 15, 90, 20, 60),
}


@dataclass
class CaptionStyle:
    font: str = "Montserrat Black"     # OFL-licensed; see fonts/README.md
    font_size: int = 86
    uppercase: bool = True
    max_words: int = 3                 # 1-3 words per caption page
    max_chars: int = 18
    text_color: str = "#FFFFFF"
    highlight_color: str = "#FFE600"   # active (spoken) word
    emphasis_color: str = "#3DFF6E"    # numbers / high-arousal keywords
    outline_color: str = "#000000"
    outline_px: int = 7
    shadow_px: int = 2
    word_highlight: bool = True
    pop_scale: int = 112               # active-word "pop" scale in %
    # Safe-zone margins: TikTok's bottom UI covers ~484px, right rail ~140px.
    margin_left: int = SAFE_LEFT + 20
    margin_right: int = WIDTH - SAFE_RIGHT + 20
    margin_bottom: int = HEIGHT - SAFE_BOTTOM + 40   # caption baseline at ~1400px
    title_font_size: int = 62
    title_text_color: str = "#111111"
    title_bg_color: str = "#FFFFFF"
    title_margin_top: int = SAFE_TOP + 40


@dataclass
class EditSettings:
    # Dead-air removal: gaps longer than `max_gap` are shortened to
    # `keep_gap` (Descript-style). Practitioner consensus, tune to taste.
    max_gap: float = 0.45
    keep_gap: float = 0.18
    pad_start: float = 0.08            # breath before first word
    pad_end: float = 0.35              # let the punchline land, then cut hard
    remove_fillers: bool = True
    # Loudness: practitioner consensus for all three apps.
    target_lufs: float = -14.0
    true_peak: float = -1.0
    # Optional licensed background music, ducked well under speech.
    music_gain_db: float = -20.0
    # Hook title shown at the top for the first N seconds (None = whole clip).
    title_seconds: float | None = None
    # Punch-in zoom every N seconds to keep a visual change on screen.
    punch_in_every: float = 0.0        # 0 disables; ~4s is common practice
    punch_in_scale: float = 1.08
    layout: str = "auto"               # auto | crop | blur | split
    fps: int = 30
    crf: int = 18
    maxrate: str = "12M"
    audio_bitrate: str = "192k"


@dataclass
class ScoringWeights:
    """Weights for the heuristic scorer (sum need not be 1). The order
    reflects what platforms say they optimise for: the first seconds
    (swipe-away), completion/watch time, then shares > comments > saves."""
    hook: float = 0.26
    standalone: float = 0.16
    payoff: float = 0.12
    emotion: float = 0.12
    energy: float = 0.10
    reactions: float = 0.08
    chat: float = 0.08
    pacing: float = 0.04
    duration_fit: float = 0.04


@dataclass
class Settings:
    platform: str = "tiktok"
    captions: CaptionStyle = field(default_factory=CaptionStyle)
    edit: EditSettings = field(default_factory=EditSettings)
    weights: ScoringWeights = field(default_factory=ScoringWeights)
    max_clips: int = 8
    # Two clips sharing more than this fraction of transcript are treated
    # as duplicates - platforms down-rank near-identical uploads.
    max_overlap: float = 0.3

    @property
    def preset(self) -> PlatformPreset:
        return PLATFORMS[self.platform]
