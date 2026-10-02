"""Animated word-by-word captions and hook titles as ASS subtitles.

ASS is rendered by ffmpeg's libass filter, so captions get burned in with
no extra dependencies. Output canvas is the vertical 1080x1920 frame.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from .config import CaptionStyle


@dataclass
class TimedWord:
    text: str
    start: float
    end: float
    emphasis: bool = False


def _ts(t: float) -> str:
    t = max(t, 0.0)
    cs = int(round(t * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def _escape(text: str) -> str:
    return text.replace("\\", "/").replace("{", "(").replace("}", ")").replace("\n", " ")


def _hex_to_ass(color: str, alpha: int = 0) -> str:
    """#RRGGBB -> &HAABBGGRR"""
    c = color.lstrip("#")
    r, g, b = c[0:2], c[2:4], c[4:6]
    return f"&H{alpha:02X}{b}{g}{r}".upper()


_STRIP = re.compile(r"[^\w'%$#@&+\-.,!?]")


def chunk_words(words: list[TimedWord], max_words: int, max_chars: int,
                gap_break: float = 0.5) -> list[list[TimedWord]]:
    """Group words into short caption 'pages' (1-3 words reads best on
    mobile). Breaks on punctuation and pauses so pages follow speech rhythm."""
    chunks: list[list[TimedWord]] = []
    cur: list[TimedWord] = []
    for i, w in enumerate(words):
        if cur:
            chars = sum(len(x.text) + 1 for x in cur) + len(w.text)
            if (len(cur) >= max_words or chars > max_chars
                    or w.start - cur[-1].end > gap_break
                    or re.search(r"[.!?,;:]$", cur[-1].text)):
                chunks.append(cur)
                cur = []
        cur.append(w)
    if cur:
        chunks.append(cur)
    return chunks


def build_ass(words: list[TimedWord], style: CaptionStyle, duration: float,
              title: str | None = None, title_seconds: float | None = None,
              width: int = 1080, height: int = 1920) -> str:
    primary = _hex_to_ass(style.text_color)
    highlight = _hex_to_ass(style.highlight_color)
    emphasis = _hex_to_ass(style.emphasis_color)
    outline = _hex_to_ass(style.outline_color)
    title_box = _hex_to_ass(style.title_bg_color, alpha=0x10)
    title_text = _hex_to_ass(style.title_text_color)

    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,{style.font},{style.font_size},{primary},{primary},{outline},&H80000000,-1,0,0,0,100,100,1,0,1,{style.outline_px},{style.shadow_px},2,{style.margin_left},{style.margin_right},{style.margin_bottom},1
Style: Title,{style.font},{style.title_font_size},{title_text},{title_text},{title_box},{title_box},-1,0,0,0,100,100,0,0,3,18,0,8,{style.margin_left},{style.margin_right},{style.title_margin_top},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines: list[str] = []

    if title:
        end = duration if title_seconds is None else min(title_seconds, duration)
        lines.append(f"Dialogue: 1,{_ts(0)},{_ts(end)},Title,,0,0,0,,{{\\fad(150,200)}}{_escape(title)}")

    def fmt(w: TimedWord, active: bool) -> str:
        text = _escape(w.text.upper() if style.uppercase else w.text)
        if active:
            pop = f"\\t(0,80,\\fscx{style.pop_scale}\\fscy{style.pop_scale})" if style.pop_scale != 100 else ""
            return f"{{\\c{highlight}{pop}}}{text}{{\\r}}"
        if w.emphasis:
            return f"{{\\c{emphasis}}}{text}{{\\r}}"
        return text

    for chunk in chunk_words(words, style.max_words, style.max_chars):
        for i, w in enumerate(chunk):
            start = w.start if i else chunk[0].start
            end = chunk[i + 1].start if i + 1 < len(chunk) else w.end
            if end <= start:
                continue
            text = " ".join(fmt(x, x is w and style.word_highlight) for x in chunk)
            lines.append(f"Dialogue: 0,{_ts(start)},{_ts(end)},Caption,,0,0,0,,{text}")
    return header + "\n".join(lines) + "\n"


_EMPHASIS = re.compile(r"^(\$?\d[\d,.]*[%kKmMbB]?|never|always|nobody|everyone|million|billion|insane|crazy|secret|worst|best|biggest|free|money|dead|died|fired|broke|rich)$", re.I)


def auto_emphasis(text: str) -> bool:
    """Colour numbers and high-arousal words - viewers skim captions, and
    a coloured keyword carries the line when watched muted."""
    return bool(_EMPHASIS.match(text.strip(".,!?\"'")))
