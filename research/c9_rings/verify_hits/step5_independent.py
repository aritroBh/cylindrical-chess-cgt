"""step5_independent.py -- run Codex's independent whole-board solver (research/ring_n_plus_2_check/odd/independent.py,
standard library only, its own move generator / e.p. / passed-pawn test / count race / minimax) on the C9 ten-pawn rings.
Only this driver is new: independent.py is imported unchanged (module name loaded by file path), its rules are not touched.
usage: step5_independent.py RING|@FILE [...]      (rg token strings, 9 files; @FILE = one ring per line)
For each ring: signature for h = 0..4 with ep_on_heap = False ("expire") and True ("keep"), states, seconds."""
import sys, os, time, importlib.util, resource
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(HERE, "..", "..", "ring_n_plus_2_check", "odd", "independent.py")
spec = importlib.util.spec_from_file_location("codex_independent_odd", path)
ind = importlib.util.module_from_spec(spec); spec.loader.exec_module(ind)
ind.self_check()
print("self_check of independent.py passed", flush=True)
rings = []
for a in sys.argv[1:]:
    rings += [l.strip() for l in open(a[1:]) if l.strip()] if a.startswith('@') else [a]
for ring in rings:
    toks = ring.split(); n = len(toks)
    pos = ind.parse_files(toks, n)
    npawns = bin(pos[0]).count("1") + bin(pos[1]).count("1")
    assert n == 9 and npawns == 10, (n, npawns)
    assert ind.make_engine(n, False)["passers"](pos) == (False, False)   # root: no passed pawn
    for keep in (False, True):
        t0 = time.time()
        eng = ind.make_engine(n, keep)
        sig = eng["signature"](pos, 5)
        print("%-34s ep_on_heap=%-5s h=0..4: %s  states=%d  wall %.1fs  maxrss %.0f MB" % (
            ring, "keep" if keep else "expire", sig, eng["wins"].cache_info().currsize, time.time() - t0,
            resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20), flush=True)
        del eng
