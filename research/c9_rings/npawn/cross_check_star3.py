"""Signatures (h = 0..5) of the two C11 twelve-pawn rings that rg finds *3 (extend/res_C11_p12.tsv) and of the C11
RRNR ring (O_11 with W5 -> W4), with the two non-Claude solvers: Codex's research/ring_n_plus_2_check/odd/independent.py
and OpenCode's research/c9_rings/codex/engine.py, both imported unchanged by file path.
usage (project root): python3 -I -B research/c9_rings/npawn/cross_check_star3.py"""
import sys, time, importlib.util
sys.dont_write_bytecode = True
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
ind = load("codex_ind", "research/ring_n_plus_2_check/odd/independent.py")
oc = load("opencode_engine", "research/c9_rings/codex/engine.py")
RINGS = [("S3a", "B4 B7 W4 W6B7 W3 B7 B6 W3 W2 B6 W2"), ("S3b", "B5 W2 W5 B7 W3 B7 B6 W3 W2 B6 W2B3"),
         ("RRNR", "B4 B7 W4 B7 W3 B7 B6 W3 W2 B6 W2")]
for name, s in RINGS:
    toks = s.split(); n = len(toks); out = [name, "n=%d" % n, "pawns=%d" % sum(len(t) // 2 for t in toks)]
    for keep in (False, True):
        t0 = time.time(); e = ind.make_engine(n, keep)
        out.append("codex(%s)=%s %.0fs" % ("keep" if keep else "expire", e["signature"](ind.parse_files(toks, n), 6), time.time() - t0))
    t0 = time.time(); e = oc.make_engine(n, True)
    out.append("opencode=%s %.0fs" % (e["signature"](oc.parse_ring(toks, n), 6), time.time() - t0))
    print("  ".join(out), flush=True)
