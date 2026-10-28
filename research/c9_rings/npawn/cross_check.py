"""Signatures (h = 0..4) of M_10, M_12, M_14 (n pawns) and N1_11, N1_13 (n+1 pawns) with the two non-Claude solvers:
Codex's research/ring_n_plus_2_check/odd/independent.py and OpenCode's research/c9_rings/codex/engine.py, both
imported unchanged by file path.  usage (project root): python3 -I -B research/c9_rings/npawn/cross_check.py"""
import sys, time, importlib.util
sys.dont_write_bytecode = True
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
ind = load("codex_ind", "research/ring_n_plus_2_check/odd/independent.py")
oc = load("opencode_engine", "research/c9_rings/codex/engine.py")
M = lambda n: ["B4", "W2"] * ((n - 8) // 2) + "B6 W2 W3 B6 B7 W3 B7 W5".split()
N1 = lambda n: ["B4", "W2"] * ((n - 7) // 2) + "B6 W2 W3 B6 B7 W3 W6B7".split()
for name, toks in [("M_10", M(10)), ("M_12", M(12)), ("M_14", M(14)), ("N1_11", N1(11)), ("N1_13", N1(13))]:
    n = len(toks); out = [name, "n=%d" % n, "pawns=%d" % sum(len(t) // 2 for t in toks)]
    for keep in (False, True):
        t0 = time.time(); e = ind.make_engine(n, keep)
        out.append("codex(%s)=%s %.0fs" % ("keep" if keep else "expire", e["signature"](ind.parse_files(toks, n), 5), time.time() - t0))
    t0 = time.time(); e = oc.make_engine(n, True)
    out.append("opencode=%s %.0fs" % (e["signature"](oc.parse_ring(toks, n), 5), time.time() - t0))
    print("  ".join(out), flush=True)
