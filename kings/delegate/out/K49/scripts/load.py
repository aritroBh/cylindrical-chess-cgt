"""K49: load K40's normal-play class tables. cls(W,H) -> dict pos -> (cls, row dict)."""
import lzma, os
D = os.path.dirname(os.path.abspath(__file__)) + '/../../K40/data'


def tag(v):
    r = list(v.values())
    if all(x == 'W' for x in r): return 'DEC'
    if all(x == 'D' for x in r): return 'DUD'
    if all(v[c] == 'W' for c in v if c not in ('off', 'dud')) and v['off'] == 'D' and v['dud'] == 'D': return 'ON'
    return 'OTHER'


def load(W, H, conv='normal'):
    fh = lzma.open(f'{D}/sums_{"normal_" if conv == "normal" else ""}cyl_{W}x{H}.tsv.xz', 'rt')
    cols = fh.readline().rstrip('\n').split('\t')[1:]
    out = {}
    for ln in fh:
        pos, *r = ln.rstrip('\n').split('\t')
        out[pos] = tag(dict(zip(cols, r)))
    return out


def sq(s):
    return ord(s[0]) - 97, int(s[1:])
