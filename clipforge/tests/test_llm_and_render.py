import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from clipforge import llm
from clipforge.config import PLATFORMS, Settings
from clipforge.media import probe
from clipforge.pipeline import analyze, render_all
from clipforge.rights import RightsDeclaration
from clipforge.transcript import Sentence, Word, split_sentences


def test_chunks_cover_everything_with_overlap():
    t = 0.0
    long = []
    for i in range(600):
        long.append(Sentence([Word("x.", t, t + 4.0)]))
        t += 5.0
    ranges = llm.chunk_ranges(long, chunk_seconds=600, overlap_seconds=60)
    assert ranges[0][0] == 0 and ranges[-1][1] == len(long)
    for (a0, a1), (b0, b1) in zip(ranges, ranges[1:]):
        assert b0 < a1  # overlap
        assert b0 > a0  # progress


def _pick(**kw):
    base = dict(start_sid=4, end_sid=9, hook_sid=4, title="He lost $1M in one night", description="d",
                hashtags=["#money", "podcast"], category="story", hook=9, flow=8, value=7, emotion=9,
                quotability=7, self_contained=9, trend=3, dangling_refs=[], is_ad=False, reasons="strong story")
    base.update(kw)
    return llm.ClipPick(**base)


def test_llm_pick_validation(words):
    sents = split_sentences(words)
    c = llm._to_candidate(_pick(), sents, 0, len(sents))
    assert c is not None and c.hashtags == ["money", "podcast"]
    assert 0.7 < c.llm["composite"] <= 1
    assert llm._to_candidate(_pick(is_ad=True), sents, 0, len(sents)) is None
    assert llm._to_candidate(_pick(end_sid=99), sents, 0, len(sents)) is None
    assert llm._to_candidate(_pick(hook_sid=15), sents, 0, len(sents)).hook_idx == 4  # hook outside clip


class _FakeClaude(BaseHTTPRequestHandler):
    requests: list = []

    def do_POST(self):  # noqa: N802
        body = json.loads(self.rfile.read(int(self.headers["content-length"])))
        _FakeClaude.requests.append((self.path, dict(self.headers), body))
        picks = {"clips": [_pick().model_dump(), _pick(start_sid=13, end_sid=17, hook_sid=16,
                                                          title="Never bet money you need").model_dump()]}
        resp = {"id": "msg_1", "type": "message", "role": "assistant", "model": body["model"],
                "content": [{"type": "text", "text": json.dumps(picks)}], "stop_reason": "end_turn",
                "stop_sequence": None, "usage": {"input_tokens": 10, "output_tokens": 10}}
        data = json.dumps(resp).encode()
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *a):
        pass


@pytest.fixture
def fake_claude(monkeypatch):
    server = HTTPServer(("127.0.0.1", 0), _FakeClaude)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setenv("ANTHROPIC_BASE_URL", f"http://127.0.0.1:{server.server_port}")
    for k in ("HTTPS_PROXY", "HTTP_PROXY", "https_proxy", "http_proxy", "ALL_PROXY", "all_proxy"):
        monkeypatch.delenv(k, raising=False)
    _FakeClaude.requests = []
    yield _FakeClaude
    server.shutdown()


def test_claude_request_shape_and_fusion(podcast, tmp_path, fake_claude):
    video, transcript = podcast
    a = analyze(str(video), Settings(platform="tiktok", max_clips=2), tmp_path, transcript_path=str(transcript))
    path, headers, body = fake_claude.requests[0]
    assert path.split("?")[0] == "/v1/messages"
    assert body["model"] == llm.DEFAULT_MODEL
    assert body["output_config"]["format"]["type"] == "json_schema"
    assert body["fallbacks"] == "default"
    assert "server-side-fallback-2026-07-01" in headers.get("anthropic-beta", "")
    assert "[4] (" in body["messages"][0]["content"]  # numbered sentences
    assert "LAUGH/REACTION" in body["messages"][0]["content"]
    assert a.moments[0].title == "He lost $1M in one night"
    assert all("llm_hook" in m.scores and "heuristic" in m.scores for m in a.moments)


@pytest.mark.parametrize("layout", ["auto", "split", "blur"])
def test_render_vertical_clip(podcast, tmp_path, fake_claude, layout):
    video, transcript = podcast
    s = Settings(platform="shorts", max_clips=1)
    s.edit.layout = layout
    s.edit.punch_in_every = 4.0 if layout == "auto" else 0.0
    a = analyze(str(video), s, tmp_path, transcript_path=str(transcript))
    rights = RightsDeclaration("licensed", note="email from host 2026-09-30", credit="Test Pod")
    outs = render_all(a, s, tmp_path, rights)
    assert len(outs) == 1
    info = probe(outs[0])
    assert (info.width, info.height) == (1080, 1920)
    meta = json.loads(outs[0].with_suffix(".json").read_text())
    assert info.duration == pytest.approx(meta["duration"], abs=0.25)
    assert info.duration <= 59.5  # non-owned Shorts stay under a minute
    assert "clipped with permission" in meta["post_caption"]
    assert outs[0].with_suffix(".jpg").exists()
    manifest = json.loads((tmp_path / (outs[0].stem + ".rights.json")).read_text())
    assert manifest["rights"]["basis"] == "licensed"


def test_cold_open_used_when_hook_is_later(podcast, tmp_path, fake_claude):
    video, transcript = podcast
    s = Settings(platform="tiktok", max_clips=2)
    a = analyze(str(video), s, tmp_path, transcript_path=str(transcript))
    outs = render_all(a, s, tmp_path, RightsDeclaration("owned"))
    metas = [json.loads(o.with_suffix(".json").read_text()) for o in outs]
    assert any(m["cold_open"] for m in metas)
    assert PLATFORMS["tiktok"].min_len <= metas[0]["duration"] <= PLATFORMS["tiktok"].max_len + 5


def test_audio_only_podcast_renders_audiogram(podcast, tmp_path, fake_claude):
    import subprocess
    video, transcript = podcast
    mp3 = tmp_path / "episode.mp3"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-vn", "-c:a", "libmp3lame", str(mp3)], check=True)
    s = Settings(platform="reels", max_clips=1)
    a = analyze(str(mp3), s, tmp_path, transcript_path=str(transcript))
    outs = render_all(a, s, tmp_path, RightsDeclaration("owned"))
    info = probe(outs[0])
    assert (info.width, info.height) == (1080, 1920) and info.has_audio
    assert json.loads(outs[0].with_suffix(".json").read_text())["layout"] == "audiogram"
