import json
import shutil
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from clipforge.transcript import Word  # noqa: E402

LINES = [
    ("A", "Welcome back to the show everybody."),
    ("A", "Today we have a great guest."),
    ("B", "Thanks for having me."),
    ("A", "So tell me about the worst mistake you ever made with money?"),
    ("B", "Honestly I lost a million dollars in one night."),
    ("B", "I remember sitting in the car and I was shaking."),
    ("B", "My wife called me and I could not even answer the phone."),
    ("B", "And then the next day I went back and did it again!"),
    ("A", "No way."),
    ("B", "That's the truth, nobody tells you how addictive it is."),
    ("A", "This episode is brought to you by our sponsor, use code SAVE for ten percent off."),
    ("A", "Check out the link in the description."),
    ("A", "Okay so what would you tell someone starting out?"),
    ("B", "Never bet money you need, that's the whole secret."),
    ("B", "Most people think they can win it back but you can't."),
    ("B", "The house always wins, and I learned that the hard way."),
    ("A", "That is insane, I can't believe you went back."),
    ("B", "Yeah um it was crazy, I was furious at myself."),
    ("A", "Alright let's take a quick break."),
    ("A", "We'll be right back after this."),
]
GAPS = [0.3, 0.6, 1.2, 0.3, 0.6, 0.3, 1.2, 0.6, 1.3, 0.3, 0.6, 0.3, 1.2, 0.3, 0.6, 0.3, 1.2, 0.6, 0.3, 0.6]


def make_words() -> list[Word]:
    words, t = [], 1.0
    for (spk, line), gap in zip(LINES, GAPS):
        for w in line.split():
            d = 0.18 + 0.04 * len(w)
            words.append(Word(w, round(t, 3), round(t + d, 3), spk, 0.95))
            t += d + 0.08
        t += gap
    return words


@pytest.fixture
def words() -> list[Word]:
    return make_words()


def _synth_audio(words: list[Word], path: Path, sr: int = 16000) -> float:
    rng = np.random.default_rng(0)
    dur = words[-1].end + 2
    x = np.zeros(int(sr * dur), np.float32)
    for w in words:
        a, b = int(w.start * sr), int(w.end * sr)
        t = np.arange(b - a) / sr
        x[a:b] += 0.15 * np.sin(2 * np.pi * 150 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 4 * t)) \
            + 0.03 * rng.standard_normal(b - a)
    # Laughter-like burst after "No way."
    i = next(k for k, w in enumerate(words) if w.text == "way.")
    s, e = int((words[i].end + 0.05) * sr), int((words[i + 1].start - 0.05) * sr)
    x[s:e] += 0.5 * rng.standard_normal(e - s).astype(np.float32)
    x = np.clip(x, -1, 1)
    with wave.open(str(path), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sr)
        f.writeframes((x * 32767).astype(np.int16).tobytes())
    return dur


@pytest.fixture(scope="session")
def podcast(tmp_path_factory):
    if shutil.which("ffmpeg") is None:
        pytest.skip("ffmpeg not installed")
    d = tmp_path_factory.mktemp("media")
    words = make_words()
    _synth_audio(words, d / "a.wav")
    video = d / "podcast.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=size=1280x720:rate=30",
                    "-i", str(d / "a.wav"), "-shortest", "-c:v", "libx264", "-preset", "ultrafast",
                    "-c:a", "aac", str(video)], check=True)
    transcript = d / "transcript.json"
    transcript.write_text(json.dumps({"language": "en", "words": [w.__dict__ for w in words]}))
    return video, transcript
