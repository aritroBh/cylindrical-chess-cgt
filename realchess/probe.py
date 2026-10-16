"""Cache-safe, rate-limited client for the Lichess tablebase API.

    GET https://tablebase.lichess.ovh/standard?fen=<FEN with spaces as '_'>

Guarantees (shared by every process that uses the same cache directory):
  * one JSON file per position (sha256 of the normalised FEN), written
    atomically (tmp file + os.replace), so concurrent readers never see a
    half-written file;
  * every HTTP request is made while holding an exclusive fcntl lock on
    <cache>/.net.lock, and at least MIN_INTERVAL seconds after the previous
    request by ANY process (timestamp kept in <cache>/.last_request);
    so the whole machine stays at <= 1 request per second;
  * the cache is re-checked after the lock is taken, so two processes never
    fetch the same position twice;
  * HTTP 429 -> sleep 60 s (still holding the lock, so every process backs
    off) and retry;
  * a HARD request cap: every HTTP attempt (including retries and failures)
    is appended to a ledger file (JSON lines) under the lock, and a Prober
    refuses to make a request once the ledger holds `cap` entries.
    Use one ledger per workstream; `cap` is the total for that ledger.

Cache hits never count against the cap.

CLI:
    python -m realchess.probe --cap 1200 --ledger realchess/logs/ledger.jsonl "<FEN>"
    python -m realchess.probe --count --ledger realchess/logs/ledger.jsonl
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

from . import movegen

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CACHE = os.path.join(HERE, "cache")
DEFAULT_LEDGER = os.path.join(HERE, "logs", "ledger.jsonl")
API = "https://tablebase.lichess.ovh/standard"
MIN_INTERVAL = 1.05  # seconds between requests, machine-wide
BACKOFF_429 = 60.0
USER_AGENT = "cylcgt-research-realchess/0.1 (tablebase verification; python-urllib)"


class CapReached(RuntimeError):
    pass


class ProbeError(RuntimeError):
    pass


def fen_key(fen: str) -> str:
    """Normalised FEN used for caching and for the request itself:
    ep square only when an ep capture is legal, clocks fixed to '0 1'."""
    return movegen.normal_fen(fen)


def _cache_path(cache_dir: str, key: str) -> str:
    h = hashlib.sha256(key.encode()).hexdigest()
    return os.path.join(cache_dir, h[:2], h + ".json")


class Prober:
    def __init__(self, cap: int, ledger: str = DEFAULT_LEDGER, cache_dir: str = DEFAULT_CACHE,
                 tag: str = "", offline: bool = False, verbose: bool = False):
        self.cap = int(cap)
        self.ledger = os.path.abspath(ledger)
        self.cache_dir = os.path.abspath(cache_dir)
        self.tag = tag
        self.offline = offline  # True: never touch the network (cache only)
        self.verbose = verbose
        self.hits = 0
        self.requests_this_process = 0
        os.makedirs(self.cache_dir, exist_ok=True)
        os.makedirs(os.path.dirname(self.ledger), exist_ok=True)

    # -------------------------------------------------------------- cache
    def cached(self, fen: str):
        key = fen_key(fen)
        path = _cache_path(self.cache_dir, key)
        try:
            with open(path) as fh:
                rec = json.load(fh)
        except (FileNotFoundError, json.JSONDecodeError):
            return None
        if rec.get("fen") != key:  # hash collision guard
            return None
        return rec

    def _store(self, key: str, rec: dict):
        path = _cache_path(self.cache_dir, key)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = f"{path}.{os.getpid()}.tmp"
        with open(tmp, "w") as fh:
            json.dump(rec, fh)
        os.replace(tmp, path)

    def ledger_count(self) -> int:
        try:
            with open(self.ledger) as fh:
                return sum(1 for line in fh if line.strip())
        except FileNotFoundError:
            return 0

    def remaining(self) -> int:
        return self.cap - self.ledger_count()

    # -------------------------------------------------------------- probe
    def probe(self, fen: str) -> dict:
        """Return the cached record {fen, status, data, fetched}; fetch if needed.
        `data` is the parsed JSON body (None on HTTP error)."""
        key = fen_key(fen)
        rec = self.cached(key)
        if rec is not None:
            self.hits += 1
            return rec
        if self.offline:
            raise CapReached(f"offline mode and not cached: {key}")
        lock_path = os.path.join(self.cache_dir, ".net.lock")
        with open(lock_path, "a+") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            try:
                rec = self.cached(key)  # someone may have fetched it meanwhile
                if rec is not None:
                    self.hits += 1
                    return rec
                return self._fetch_locked(key)
            finally:
                fcntl.flock(lock, fcntl.LOCK_UN)

    def _wait_interval(self):
        stamp = os.path.join(self.cache_dir, ".last_request")
        try:
            last = float(open(stamp).read().strip() or 0)
        except (FileNotFoundError, ValueError):
            last = 0.0
        dt = time.time() - last
        if dt < MIN_INTERVAL:
            time.sleep(MIN_INTERVAL - dt)
        with open(stamp, "w") as fh:
            fh.write(repr(time.time()))

    def _log(self, key, status, note=""):
        with open(self.ledger, "a") as fh:
            fh.write(json.dumps({"t": time.time(), "fen": key, "status": status,
                                 "tag": self.tag, "pid": os.getpid(), "note": note}) + "\n")

    def _fetch_locked(self, key: str) -> dict:
        url = API + "?" + urllib.parse.urlencode({"fen": key.replace(" ", "_")})
        attempts = 0
        while True:
            if self.ledger_count() >= self.cap:
                raise CapReached(f"request cap {self.cap} reached (ledger {self.ledger})")
            attempts += 1
            self._wait_interval()
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT,
                                                       "Accept": "application/json"})
            status, body, note = None, None, ""
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    status = resp.status
                    body = resp.read().decode()
            except urllib.error.HTTPError as e:
                status = e.code
                try:
                    body = e.read().decode()
                except Exception:  # pragma: no cover
                    body = ""
            except (urllib.error.URLError, TimeoutError, OSError) as e:
                status, note = -1, repr(e)
            self.requests_this_process += 1
            self._log(key, status, note)
            if self.verbose:
                print(f"[probe] {status} {key}", flush=True)
            if status == 429:
                time.sleep(BACKOFF_429)
                continue
            if status == -1 or (status is not None and status >= 500):
                if attempts >= 4:
                    raise ProbeError(f"network/server failure for {key}: {status} {note}")
                time.sleep(5 * attempts)
                continue
            data = None
            if status == 200:
                data = json.loads(body)
            rec = {"fen": key, "status": status, "data": data,
                   "body": None if status == 200 else body, "fetched": time.time()}
            self._store(key, rec)
            return rec


# ---------------------------------------------------------------- helpers
def categories(rec: dict) -> tuple[str | None, dict]:
    """(root category, {uci: category-after-move})."""
    d = rec.get("data") or {}
    return d.get("category"), {m["uci"]: m.get("category") for m in d.get("moves", [])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fen", nargs="*")
    ap.add_argument("--cap", type=int, default=0)
    ap.add_argument("--ledger", default=DEFAULT_LEDGER)
    ap.add_argument("--cache", default=DEFAULT_CACHE)
    ap.add_argument("--count", action="store_true", help="print ledger size and exit")
    ap.add_argument("--offline", action="store_true")
    a = ap.parse_args()
    pr = Prober(a.cap, a.ledger, a.cache, tag="cli", offline=a.offline)
    if a.count:
        print(pr.ledger_count())
        return
    rec = pr.probe(" ".join(a.fen))
    print(json.dumps(rec, indent=1))


if __name__ == "__main__":
    main()
