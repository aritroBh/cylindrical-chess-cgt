"""Signatures (h = 0..5) of the n+1-pawn rings S_m = B4 B6 W3 (W2 B4)^m W6B7 W3 B7 B6 W3 W2 B6 W2 (C_{11+2m}), which rg
finds *3 for m = 1..24 (research/c9_rings/star3/res_fam3_odd.tsv), with the two non-Claude solvers: Codex's
research/ring_n_plus_2_check/odd/independent.py and OpenCode's research/c9_rings/codex/engine.py, imported unchanged.
and T_m = (B4 W2)^m B5 W2 W6B7 W3 B7 B6 W3 W2 B6 W2 (C_{10+2m}, star3/res_fam3_even.tsv).
usage (project root): python3 -I -B research/c9_rings/npawn/cross_check_S3.py [MMAX] [S|T]"""
import sys, time, importlib.util
sys.dont_write_bytecode = True
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
ind = load("codex_ind", "research/ring_n_plus_2_check/odd/independent.py")
oc = load("opencode_engine", "research/c9_rings/codex/engine.py")
FAM = {"S": lambda m: "B4 B6 W3".split() + ["W2", "B4"] * m + "W6B7 W3 B7 B6 W3 W2 B6 W2".split(),
       "T": lambda m: ["B4", "W2"] * m + "B5 W2 W6B7 W3 B7 B6 W3 W2 B6 W2".split()}
fam = sys.argv[2] if len(sys.argv) > 2 else "S"
for m in range(0, int(sys.argv[1]) + 1 if len(sys.argv) > 1 else 4):
    toks = FAM[fam](m); n = len(toks); out = ["%s_%d" % (fam, m), "n=%d" % n, "pawns=%d" % sum(len(t) // 2 for t in toks)]
    for keep in (False, True):
        t0 = time.time(); e = ind.make_engine(n, keep)
        out.append("codex(%s)=%s %.0fs" % ("keep" if keep else "expire", e["signature"](ind.parse_files(toks, n), 6), time.time() - t0))
    t0 = time.time(); e = oc.make_engine(n, True)
    out.append("opencode=%s %.0fs" % (e["signature"](oc.parse_ring(toks, n), 6), time.time() - t0))
    print("  ".join(out), flush=True)
