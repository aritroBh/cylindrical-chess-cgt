"""K40: the three-class picture.  For each board:
  normal play: per side, class of (x, s) in {DEC (W vs every test, = P_L), ON (signature of on), DUD (D vs every
  test), OTHER}; per quiet placement, the pair (class with White to move, class with Black to move);
  P (chess stalemate): the same tags, plus the integer pattern for OTHER; and the cross-tab of the normal class
  with the bare P result (T = 0) and with the atlas result.
Usage: python classify.py > data/classify.json
"""
import json, lzma, os
from collections import Counter, defaultdict

D = os.path.dirname(os.path.abspath(__file__)) + '/..'
ON = None


def tag(cols, r):
    v = dict(zip(cols, r))
    ints = ''.join(v[str(n)] for n in range(-12, 13))
    if all(x == 'W' for x in r):
        return 'DEC', ints
    if all(x == 'D' for x in r):
        return 'DUD', ints
    on_sig = all(v[c] == 'W' for c in cols if c not in ('off', 'dud')) and v['off'] == 'D' and v['dud'] == 'D'
    return ('ON' if on_sig else 'OTHER'), ints


out = {}
for H in (6, 8):
    for W in range(3, 9):
        b = f'{W}x{H}'
        res = {}
        for conv in ('normal', 'P'):
            fh = lzma.open(f'{D}/data/sums_{"normal_" if conv == "normal" else ""}cyl_{b}.tsv.xz', 'rt')
            cols = fh.readline().rstrip('\n').split('\t')[1:]
            for ln in fh:
                pos, *r = ln.rstrip('\n').split('\t')
                res[(conv, pos)] = tag(cols, r)
        base = {}
        for ln in lzma.open(f'{D}/data/base_cyl_{b}.tsv.xz', 'rt'):
            wk, bk, p, s, r0, rk, rr, ra = ln.rstrip('\n').split('\t')
            if wk == 'wk':
                continue
            base[f'{wk} {bk} {p} {s}'] = (r0, ra)
        o = {'side': {}, 'pairs': {}, 'xtab_P0': {}, 'xtab_atlas': {}, 'P_vs_normal': {}, 'P_other_ints': {}}
        for conv in ('normal', 'P'):
            c = Counter((pos.split()[-1], res[(conv, pos)][0]) for (cv, pos) in res if cv == conv)
            o['side'][conv] = {f'{s} {t}': n for (s, t), n in sorted(c.items())}
            pr = Counter(); ex = {}
            places = {pos[:-2] for (cv, pos) in res if cv == conv}
            for pl in places:
                if (conv, pl + ' w') in res and (conv, pl + ' b') in res:
                    k = res[(conv, pl + ' w')][0] + '/' + res[(conv, pl + ' b')][0]
                    pr[k] += 1; ex.setdefault(k, pl)
            o['pairs'][conv] = {k: [n, ex[k]] for k, n in sorted(pr.items())}
        xt, xa, pn, pi = Counter(), Counter(), Counter(), Counter()
        exs = {}
        for (cv, pos), (t, ints) in res.items():
            if cv != 'normal':
                continue
            s = pos.split()[-1]
            r0, ra = base[pos]
            xt[f'{s} {t} P0={r0}'] += 1
            xa[f'{s} {t} atlas={ra}'] += 1
            tp, ip = res[('P', pos)]
            pn[f'{s} normal={t} P={tp}'] += 1
            exs.setdefault(f'{s} normal={t} P={tp}', pos)
            if tp == 'OTHER':
                pi[f'{s} {ip}'] += 1
        o['xtab_P0'] = dict(sorted(xt.items()))
        o['xtab_atlas'] = dict(sorted(xa.items()))
        o['P_vs_normal'] = {k: [n, exs[k]] for k, n in sorted(pn.items())}
        o['P_other_ints'] = dict(sorted(pi.items(), key=lambda x: -x[1]))
        out[b] = o
print(json.dumps(out, indent=1))
