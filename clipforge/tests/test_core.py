import json

import numpy as np
import pytest

from clipforge.audio import AudioEnvelope, reaction_events
from clipforge.captions import TimedWord, build_ass, chunk_words
from clipforge.chat import ChatMessage, ChatTrack, load_chat
from clipforge.config import PLATFORMS, CaptionStyle, EditSettings, ScoringWeights
from clipforge.moments import Candidate, Signals, find_moments, select
from clipforge.rights import (MusicTrack, RightsDeclaration, RightsError, background_bed_ratio,
                              load_music_library, max_length_for, pick_music)
from clipforge.timeline import build_cutlist, with_cold_open
from clipforge.transcript import Transcript, Word, split_sentences


# --- transcript -------------------------------------------------------------

def test_sentences_split_on_punctuation_and_speaker(words):
    sents = split_sentences(words)
    assert len(sents) == 20
    assert sents[0].text == "Welcome back to the show everybody."
    assert all(s.speaker in ("A", "B") for s in sents)


def test_load_whisperx_and_srt(tmp_path):
    wx = tmp_path / "wx.json"
    wx.write_text(json.dumps({"segments": [{"text": "Hello there 2024", "start": 0, "end": 2, "speaker": "S1",
                                            "words": [{"word": "Hello", "start": 0.0, "end": 0.4, "score": 0.9},
                                                      {"word": "there", "start": 0.5, "end": 0.9},
                                                      {"word": "2024"}]}]}))
    t = Transcript.load(wx)
    assert [w.text for w in t.words] == ["Hello", "there"]  # unaligned numerals dropped
    assert t.words[0].speaker == "S1"

    srt = tmp_path / "a.srt"
    srt.write_text("1\n00:00:01,000 --> 00:00:03,000\nhello big world\n\n2\n00:00:04,000 --> 00:00:05,000\nbye\n")
    t = Transcript.load(srt)
    assert [w.text for w in t.words] == ["hello", "big", "world", "bye"]
    assert t.words[0].start == pytest.approx(1.0) and t.words[2].end == pytest.approx(3.0)


# --- timeline ---------------------------------------------------------------

def test_cutlist_removes_fillers_and_dead_air():
    ws = [Word("I", 0.0, 0.2), Word("um", 0.3, 0.6), Word("think", 0.7, 1.0),
          Word("so.", 2.5, 2.8)]  # 1.5s of dead air before "so."
    cut = build_cutlist(ws, EditSettings())
    texts = [w.text for w in cut.words]
    assert "um" not in texts
    assert cut.duration < 2.8 - 1.0  # dead air tightened
    starts = [w.start for w in cut.words]
    assert starts == sorted(starts) and starts[0] >= 0


def test_cold_open_prepends_hook(words):
    body = build_cutlist(words[10:40], EditSettings())
    hook = words[30:35]
    cut = with_cold_open(hook, body, EditSettings())
    assert cut.segments[0].start >= hook[0].start - 0.1
    assert [w.text for w in cut.words[:5]] == [w.text for w in hook]
    assert cut.duration == pytest.approx(body.duration + sum(s.duration for s in cut.segments[:-len(body.segments)]))


# --- captions ---------------------------------------------------------------

def test_caption_chunks_short_and_highlighted():
    tw = [TimedWord(t, i * 0.3, i * 0.3 + 0.25) for i, t in enumerate("this is a {weird} test of captions here".split())]
    chunks = chunk_words(tw, 3, 18)
    assert all(len(c) <= 3 for c in chunks)
    ass = build_ass(tw, CaptionStyle(), 3.0, title="Hook title")
    assert "PlayResY: 1920" in ass and "Style: Caption" in ass
    assert "{weird}" not in ass and "(WEIRD)" in ass  # override braces escaped
    assert ass.count("Dialogue: 0,") == len(tw)
    assert "Title,,0,0,0,," in ass


# --- moments ----------------------------------------------------------------

def test_story_beats_ad_read_and_intro(words):
    sents = split_sentences(words)
    env = AudioEnvelope(np.full(int(words[-1].end / 0.05) + 40, -30.0))
    sig = Signals(env, None, [(words[[w.text for w in words].index("way.")].end + 0.5, 3.0)])
    top = find_moments(sents, sig, PLATFORMS["tiktok"], ScoringWeights(), k=3, max_overlap=0.3)
    assert "million dollars" in top[0].text
    assert all(not c.text.startswith("Welcome back") for c in top[:2])
    for c in top:
        assert c.duration >= PLATFORMS["tiktok"].min_len
    ad = [c for c in top if "sponsor" in c.text]
    assert all(c.score < top[0].score for c in ad)


def test_select_drops_near_duplicates():
    a = Candidate(0, 1, 0, 30, "a", score=90)
    b = Candidate(0, 1, 5, 35, "b", score=80)  # mostly overlaps a
    c = Candidate(0, 1, 40, 70, "c", score=70)
    assert [x.text for x in select([a, b, c], 3, 0.3)] == ["a", "c"]


def test_reaction_events_find_loud_gaps(words):
    db = np.full(int(words[-1].end / 0.05) + 40, -60.0)
    for w in words:
        db[int(w.start / 0.05):int(w.end / 0.05)] = -25.0
    i = [w.text for w in words].index("way.")
    gap_s, gap_e = words[i].end, words[i + 1].start
    db[int(gap_s / 0.05) + 1:int(gap_e / 0.05)] = -12.0
    ev = reaction_events(AudioEnvelope(db), words)
    assert any(gap_s <= t <= gap_e for t, _ in ev)


# --- rights -----------------------------------------------------------------

def test_rights_required_before_render():
    with pytest.raises(RightsError):
        RightsDeclaration("").validate()
    with pytest.raises(RightsError):
        RightsDeclaration("licensed").validate()  # needs a note
    RightsDeclaration("owned").validate()
    RightsDeclaration("clipping-program", note="https://example.com/campaign").validate()


def test_shorts_capped_under_a_minute_unless_owned_and_clean():
    owned, lic = RightsDeclaration("owned"), RightsDeclaration("licensed", note="x")
    assert max_length_for("shorts", 59, lic, False) == 59
    assert max_length_for("tiktok", 120, lic, False) == 120
    assert max_length_for("shorts", 180, owned, False) == 180
    assert max_length_for("shorts", 180, owned, True) == 59


def test_music_library_requires_commercial_licence(tmp_path):
    (tmp_path / "ok.mp3").write_bytes(b"x")
    (tmp_path / "nc.mp3").write_bytes(b"x")
    (tmp_path / "licenses.json").write_text(json.dumps([
        dict(file="nc.mp3", title="NC", source="CC", license="CC BY-NC", license_url="u", commercial_use=False),
        dict(file="ok.mp3", title="OK", source="Lib", license="Lib licence", license_url="u", commercial_use=True,
             platforms=["tiktok"]),
    ]))
    tracks = load_music_library(tmp_path)
    assert pick_music(tracks, "tiktok").title == "OK"
    with pytest.raises(RightsError):
        pick_music(tracks, "shorts")
    assert not MusicTrack("f", "t", "s", "l", "u", False).allowed_on("tiktok")


def test_background_bed_detection(words):
    n = int(words[-1].end / 0.05) + 40
    clean = np.full(n, -70.0)
    for w in words:
        clean[int(w.start / 0.05):int(w.end / 0.05)] = -20.0
    bed = np.maximum(clean, -28.0)  # music keeps playing through pauses
    assert background_bed_ratio(AudioEnvelope(clean), words) < 0.2
    assert background_bed_ratio(AudioEnvelope(bed), words) > 0.8


# --- chat -------------------------------------------------------------------

def test_chat_formats_and_spike(tmp_path):
    (tmp_path / "c.json").write_text(json.dumps({"comments": [
        {"content_offset_seconds": 1.5, "message": {"body": "hi"}}]}))
    assert load_chat(tmp_path / "c.json")[0].t == 1.5
    (tmp_path / "c.txt").write_text("[0:01:05] someuser: KEKW\n[1:06] other: lol\n")
    msgs = load_chat(tmp_path / "c.txt")
    assert [m.t for m in msgs] == [65.0, 66.0]

    rng = np.random.default_rng(1)
    msgs = [ChatMessage(float(t), "hello there friend") for t in rng.uniform(0, 600, 300)]
    msgs += [ChatMessage(300 + 8 + rng.uniform(0, 4), "KEKW") for _ in range(80)]  # reaction 8s after event
    track = ChatTrack.build(msgs, 600)
    track.lag = 8
    assert track.spike_z(298, 302) > 3
    assert track.spike_z(100, 104) < 1.5
    assert track.dominant_reaction(298, 302)[0] == "laugh"
