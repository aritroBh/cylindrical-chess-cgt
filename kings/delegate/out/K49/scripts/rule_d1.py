"""K49: the rule for the pawn one step from promotion (d = 1), tested against the normal-play classes.
Rule (pawn p on (f, H-1), q = (f, H), Pi = the three squares of rank H-2 at file distance <= 1 from f):
 White to move: q not occupied by bk -> DEC; bk on q -> ON if wk is within one king step of Pi, else DUD.
 Black to move: Kxp legal (bk next to p, wk not next to p) -> DUD; bk on q -> ON (then wk is in Pi);
   bk may step to q -> the White-to-move class of (wk, q) (DUD or ON); otherwise DEC.
Classes come from kn.c runs with the standard 34 tests (H = 6, 7, 8) on W = 3, 5..9."""
import subprocess, load
def cd(a, b, W): d = (a - b) % W; return min(d, W - d)
def cheb(a, b, W): return max(cd(a[0], b[0], W), abs(a[1] - b[1]))
def rule(wk, bk, p, s, W, H):
    q = (p[0], p[1] + 1); Pi = [((p[0] + i) % W, p[1] - 1) for i in (-1, 0, 1)]
    def wclass(wk, bk):
        if bk != q: return 'DEC'
        return 'ON' if min(cheb(wk, x, W) for x in Pi) <= 1 else 'DUD'
    if s == 'w': return wclass(wk, bk)
    if cheb(bk, p, W) == 1 and cheb(wk, p, W) > 1: return 'DUD'
    if bk == q: return 'ON'
    if cheb(bk, q, W) == 1 and cheb(wk, q, W) > 1: return wclass(wk, q)
    return 'DEC'
tot = bad = 0
for W in (3, 5, 6, 7, 8, 9):
    for H in (6, 7, 8):
        out = subprocess.run(['../tmp/kn', str(W), str(H), 'std.t'], capture_output=True, text=True).stdout.splitlines()
        cols = out[0].split()[1:]; n = b = 0
        for ln in out[1:]:
            a, r = ln.split('|'); a = a.split()
            wk, bk, p = (load.sq(x) for x in a[:3]); wk = (wk[0], wk[1]); p = (p[0], p[1])
            if H - p[1] != 1: continue
            c = load.tag(dict(zip(cols, r.split())))
            n += 1
            if rule(wk, bk, p, a[3], W, H) != c:
                b += 1
                if b <= 3: print('  exception', W, H, ' '.join(a), c, rule(wk, bk, p, a[3], W, H))
        print(f'cyl:{W}x{H} d=1 positions {n} exceptions {b}'); tot += n; bad += b
print('total', tot, 'exceptions', bad)
