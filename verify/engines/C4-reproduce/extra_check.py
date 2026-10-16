"""ep squares, root passers, cache-key fallback for cgt_verified.epd (verifier scratch).
    cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python verify/engines/C4-reproduce/extra_check.py
"""
import collections, glob, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import indep_check as I  # re-runs the main checks (prints), then exposes helpers
ep, fallback, rootpass = 0, 0, 0
tiers = collections.Counter()
for fen4, ops in I.ver:
    if fen4.split()[3] != "-":
        ep += 1
        print("ep FEN in verified:", fen4, ops["c2"])
    if fen4 not in I.cache:
        fallback += 1
    b = I.board_of(fen4)
    W = frozenset(s for s, p in b.items() if p == "P" and s[0] < 4)
    B = frozenset(s for s, p in b.items() if p == "p" and s[0] < 4)
    if I.passed(W, B, "W") or I.passed(W, B, "B"):
        rootpass += 1
    tiers[ops["c3"].split("tier ")[1].split(";")[0]] += 1
    # e-file empty and trebuchet intact
    assert not any(f == 4 for f, r in b), fen4
print("verified with ep square:", ep, "; cache lookups needing ep->'-' fallback:", fallback,
      "; root component has a passer:", rootpass)
print("verified by tier:", dict(tiers))
