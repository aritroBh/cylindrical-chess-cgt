"""Probe and knowledge-base plumbing for the certify workstream.

Everything this workstream WRITES stays under realchess/certify/:
  * new Lichess records go to realchess/certify/cache (same key scheme as
    realchess/probe.py: sha256 of the normal FEN);
  * the request ledger is realchess/certify/logs/ledger.jsonl (own cap);
  * results go to realchess/certify/results.
Existing caches are READ only: realchess/cache (the A2-realchess cache) and
the sibling caches that realchess/kb.py already indexes.

Etiquette (as realchess/probe.py): <= 1 request per 1.05 s, 60 s back-off on
HTTP 429, a hard cap counted on the ledger. In addition this prober holds the
shared lock realchess/cache/.net.lock (opened read-only, never written) while
it makes a request, and also waits for the shared .last_request stamp, so it
never fires within 1.05 s of a request made by the realchess tooling.
"""
from __future__ import annotations

import fcntl
import json
import os
import time

from realchess import kb as K
from realchess import probe as P

HERE = os.path.dirname(os.path.abspath(__file__))
REALCHESS = os.path.dirname(HERE)
CACHE = os.path.join(HERE, "cache")
LEDGER = os.path.join(HERE, "logs", "ledger.jsonl")
RESULTS = os.path.join(HERE, "results")
SHARED_CACHE = os.path.join(REALCHESS, "cache")
READ_DIRS = [CACHE, SHARED_CACHE] + K.EXTRA

_KB = None


def kb():
    """KB over my cache, the realchess cache and the sibling caches; it is
    updated in place whenever this process fetches a new record."""
    global _KB
    if _KB is None:
        _KB = K.KB(dirs=READ_DIRS)
    return _KB


class CertProber(P.Prober):
    def __init__(self, cap: int, ledger: str = LEDGER, tag: str = "certify", offline: bool = False,
                 verbose: bool = False):
        super().__init__(cap, ledger, CACHE, tag=tag, offline=offline, verbose=verbose)

    def cached(self, fen: str):
        key = P.fen_key(fen)
        for d in READ_DIRS:
            path = P._cache_path(d, key)
            try:
                with open(path) as fh:
                    rec = json.load(fh)
            except (FileNotFoundError, json.JSONDecodeError, OSError):
                continue
            if rec.get("fen") == key and rec.get("status") == 200 and rec.get("data"):
                return rec
        return None

    def probe(self, fen: str) -> dict:
        key = P.fen_key(fen)
        rec = self.cached(key)
        if rec is not None:
            self.hits += 1
            return rec
        if self.offline:
            raise P.CapReached(f"offline mode and not cached: {key}")
        shared_lock = os.path.join(SHARED_CACHE, ".net.lock")
        own_lock = os.path.join(CACHE, ".net.lock")
        with open(own_lock, "a+") as lock2:
            fcntl.flock(lock2, fcntl.LOCK_EX)
            try:
                sh = open(shared_lock, "r") if os.path.exists(shared_lock) else None
                try:
                    if sh is not None:
                        fcntl.flock(sh, fcntl.LOCK_EX)
                    rec = self.cached(key)
                    if rec is not None:
                        self.hits += 1
                        return rec
                    rec = self._fetch_locked(key)
                finally:
                    if sh is not None:
                        fcntl.flock(sh, fcntl.LOCK_UN)
                        sh.close()
            finally:
                fcntl.flock(lock2, fcntl.LOCK_UN)
        if rec.get("status") == 200 and rec.get("data"):
            k = kb()
            if key not in k.records:
                k.records[key] = rec
                k.record_dir[key] = CACHE
                k._index(key, rec)
        return rec

    def _wait_interval(self):
        last = 0.0
        for d in (CACHE, SHARED_CACHE):
            try:
                last = max(last, float(open(os.path.join(d, ".last_request")).read().strip() or 0))
            except (FileNotFoundError, ValueError, OSError):
                pass
        dt = time.time() - last
        if dt < P.MIN_INTERVAL:
            time.sleep(P.MIN_INTERVAL - dt)
        with open(os.path.join(CACHE, ".last_request"), "w") as fh:
            fh.write(repr(time.time()))


def patch_realchess():
    """Point the realchess stages at this workstream's prober, KB and results
    directory (module attributes only; no file outside certify/ is touched)."""
    from realchess import solve_candidate as S
    from realchess import oracle_value as O  # noqa: F401  (imports RESULTS lazily)
    S.RESULTS = RESULTS
    S.Prober = CertProber
    K._DEFAULT = kb()
    try:
        from realchess import pin
        pin.RESULTS = RESULTS
    except Exception:  # pragma: no cover
        pass
    for name in ("root_table", "compare_nodes", "verify_nodes", "final_summary", "random_check",
                 "stops_check", "verify_proof", "consistency", "summarize"):
        try:
            mod = __import__(f"realchess.{name}", fromlist=["x"])
        except Exception:
            continue
        if hasattr(mod, "RESULTS"):
            mod.RESULTS = RESULTS
    return S
