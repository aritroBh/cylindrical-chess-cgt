"""Offline tests of the probe client: cache, ledger cap, 429 back-off.
The network is replaced by a stub; nothing is sent."""
import io
import json
import urllib.error

import pytest

from realchess import probe


class _Resp(io.BytesIO):
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def _stub(calls, codes):
    def urlopen(req, timeout=0):
        calls.append(req.full_url)
        code = codes.pop(0) if codes else 200
        if code != 200:
            raise urllib.error.HTTPError(req.full_url, code, "x", {}, io.BytesIO(b"{}"))
        return _Resp(json.dumps({"category": "draw", "moves": []}).encode())
    return urlopen


def test_cache_cap_and_backoff(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(probe.urllib.request, "urlopen", _stub(calls, [429, 200]))
    monkeypatch.setattr(probe, "BACKOFF_429", 0.0)
    monkeypatch.setattr(probe, "MIN_INTERVAL", 0.0)
    pr = probe.Prober(cap=3, ledger=str(tmp_path / "l.jsonl"), cache_dir=str(tmp_path / "c"))
    fen = "8/8/8/5Kp1/6Pk/8/8/8 w - - 0 1"
    rec = pr.probe(fen)
    assert rec["status"] == 200 and rec["data"]["category"] == "draw"
    assert len(calls) == 2 and pr.ledger_count() == 2      # the 429 counted too
    assert "_" in calls[0] and " " not in calls[0]
    pr.probe(fen)                                           # cache hit
    assert len(calls) == 2 and pr.hits == 1
    pr2 = probe.Prober(cap=3, ledger=str(tmp_path / "l.jsonl"), cache_dir=str(tmp_path / "c"))
    assert pr2.cached(fen) is not None                     # shared on disk
    pr2.probe("8/8/8/5Kp1/6Pk/8/8/8 b - - 0 1")             # 3rd request: allowed
    with pytest.raises(probe.CapReached):
        pr2.probe("8/8/8/5K2/6Pk/8/8/8 b - - 0 1")          # 4th: refused
    assert len(calls) == 3


def test_offline_mode(tmp_path):
    pr = probe.Prober(cap=10, ledger=str(tmp_path / "l.jsonl"), cache_dir=str(tmp_path / "c"),
                      offline=True)
    with pytest.raises(probe.CapReached):
        pr.probe("8/8/8/5Kp1/6Pk/8/8/8 w - - 0 1")
