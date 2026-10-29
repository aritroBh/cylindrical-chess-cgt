"""K40: list every position where the atlas KPK code and P disagree, with the reason.
Reason, for White to move with the pawn on rank H-1 and the promotion square empty: 'Kxq' (after the promotion
Black's king takes the unprotected queen: a K v K draw) or 'stalemate' (the queen stalemates); otherwise
'later' (P's win passes through such a promotion further on).  Writes data/atlas_disagreements.tsv.xz and
prints counts (JSON).  The normal-play class of the position (DEC/ON) is added from data/classify inputs.
"""
import json, lzma, os
from collections import Counter

D = os.path.dirname(os.path.abspath(__file__)) + '/..'


def geo(W, H):
    def at(f, r):
        return None if r < 0 or r >= H else r * W + f % W
    K = []
    for s in range(W * H):
        f, r = s % W, s // W
        nb = {at(f + a, r + b) for a in (-1, 0, 1) for b in (-1, 0, 1) if (a, b) != (0, 0)} - {None, s}
        K.append(nb)
    return at, K


def qatt(W, H, at, q, t, wk):
    for df, dr in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
        f, r = q % W, q // W
        for _ in range(64):
            f, r = f + df, r + dr
            s = at(f, r)
            if s is None or s == q:
                break
            if s == t:
                return True
            if s == wk:
                break
    return False


out_rows, cnt = [], Counter()
for H in (6, 8):
    for W in range(3, 9):
        at, K = geo(W, H)
        sq = lambda n: (int(n[1:]) - 1) * W + ord(n[0]) - 97
        cls = {}
        for ln in lzma.open(f'{D}/data/sums_normal_cyl_{W}x{H}.tsv.xz', 'rt'):
            pos, *r = ln.rstrip('\n').split('\t')
            if pos == 'pos':
                continue
            cls[pos] = 'DEC' if all(x == 'W' for x in r) else ('DUD' if all(x == 'D' for x in r) else 'ON/other')
        for ln in lzma.open(f'{D}/data/base_cyl_{W}x{H}.tsv.xz', 'rt'):
            wk, bk, p, s, r0, rk, rr, ra = ln.rstrip('\n').split('\t')
            if wk == 'wk' or ra == r0:
                continue
            reason = 'later'
            P, WK, BK = sq(p), sq(wk), sq(bk)
            if s == 'w' and P // W == H - 2 and P + W not in (WK, BK):
                q = P + W
                mv = [d for d in K[BK] if d != WK and d not in K[WK]]
                if q in mv:
                    reason = 'Kxq'
                elif not any(not qatt(W, H, at, q, d, WK) for d in mv) and not qatt(W, H, at, q, BK, WK):
                    reason = 'stalemate'
            pos = f'{wk} {bk} {p} {s}'
            c = cls[pos]
            cnt[f'cyl:{W}x{H} {s} {reason} normal={c}'] += 1
            out_rows.append(f'cyl:{W}x{H}\t{wk}\t{bk}\t{p}\t{s}\tP={r0}\tatlas={ra}\t{reason}\t{c}\n')
with lzma.open(f'{D}/data/atlas_disagreements.tsv.xz', 'wt') as fh:
    fh.write('board\twk\tbk\tp\tstm\tP\tatlas\treason\tnormal_class\n')
    fh.writelines(out_rows)
print(json.dumps(dict(sorted(cnt.items())), indent=0))
