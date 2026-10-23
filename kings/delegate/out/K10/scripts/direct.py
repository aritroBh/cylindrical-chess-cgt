import sys, itertools, subprocess, json, collections, time, os
sys.path.insert(0, '.')
from cert import *

KP = '/private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/5e853794-e7f0-4f24-9541-471b59b05e33/scratchpad/k10/kp'
FILES = "abcdefgh"

def line(bd, pos, wk, bk, stm):
    toks = ["K"+name(wk), "k"+name(bk)] + ["P"+name(s) for s in sorted(pos.white)] + ["p"+name(s) for s in sorted(pos.black)]
    ep = "-"
    if pos.ep:
        # kpsolve keeps an ep target only if a capturer exists; give it only then
        t, c, side = pos.ep
        if ep_capturable.__call__ and any(((g, c[1]) in (pos.black if side == 'B' else pos.white)) for g in (bd.nb(c[0], -1), bd.nb(c[0], 1))):
            ep = name(t)
    return " ".join(toks) + " " + ("w" if stm == 'W' else "b") + " " + ep

def run_kp(bd, lines, threads=2):
    inp = "\n".join(lines) + "\n"
    r = subprocess.run(["nice", "-n", "10", KP, "--board", f"cyl:{bd.files}x{bd.ranks}", "--frozen", "--cap", "1", "--threads", str(threads)],
                       input=inp, capture_output=True, text=True)
    res = {}
    for l in r.stdout.splitlines():
        if " | " not in l: continue
        a, b = l.split(" | ")[0:2]
        v = b.split()
        res[a] = v
    return res

def enum_positions(bd, files, maxp, ranks):
    sqs = [(f, r) for f in files for r in ranks]
    def subsets(k):
        for n in range(0, k+1):
            yield from itertools.combinations(sqs, n)
    for w in subsets(maxp):
        ws = set(w)
        for b in subsets(maxp):
            if ws & set(b): continue
            yield frozenset(w), frozenset(b)

if __name__ == "__main__":
    W, H, maxp = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    files = list(range(2, W-1))
    bd = Board(W, H, True, True)
    wk, bk = (0, 1), (0, H)
    ranks = range(2, H)
    ablate = ['P1', 'front', 'kpath', 'K1', 'K2', 'N', 'M']
    full = tuple(ablate)
    inst = {}   # line -> list of tags
    t0 = time.time(); n = 0
    cand = collections.defaultdict(list)  # key (variant) -> list of (line, beta)
    for w, b in enum_positions(bd, files, maxp, ranks):
        pos = Pos(w, b)
        for stm in 'WB':
            L = line(bd, pos, wk, bk, stm)
            for beta in 'WB':
                if not (w if beta == 'W' else b): continue
                ok, _ = check(bd, pos, wk, bk, stm, beta, use=full)
                if ok: cand['FULL'].append((L, beta))
                else:
                    pass
                # ablation: drop one hypothesis (kings fixed in parked layout so K1,K2,kpath always hold there)
                for h in ('N', 'M'):
                    use = tuple(x for x in full if x != h)
                    ok2, _ = check(bd, pos, wk, bk, stm, beta, use=use)
                    if ok2 and not ok: cand['no_'+h].append((L, beta))
        n += 1
    print("enumerated", n, "pos pairs in", round(time.time()-t0), "s;", {k: len(v) for k, v in cand.items()}, flush=True)
    for k, v in cand.items():
        lines = sorted({L for L, _ in v})
        viol = 0; tot = 0; ex = []
        CH = 40000
        res = {}
        for i in range(0, len(lines), CH):
            res.update(run_kp(bd, lines[i:i+CH]))
        for L, beta in v:
            r = res.get(L)
            tot += 1
            want = 'W' if beta == 'W' else 'L'
            if r is None or r[0] != want or r[1] != want:
                viol += 1
                if len(ex) < 6: ex.append((L, beta, r))
        print(k, "instances", tot, "violations", viol, ex, flush=True)
