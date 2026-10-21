"""T1-refute: compare my pixel scan with (a) CLAIMS parsed from cylcgt/verify_paper.py source text (no import)
and (b) the worker's MINE FEN table parsed from verify/diagrams/rerun.py source text (no import).
Run: cd verify/diagrams/T1-refute && ../../../.venv/bin/python -I compare.py
"""
import ast, sys
sys.path.insert(0, '.')
import myscan

def literal_assign(path, name):
    tree = ast.parse(open(path).read())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, 'id', None) == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise KeyError(name)

CLAIMS = literal_assign('../../../cylcgt/verify_paper.py', 'CLAIMS')
MINE = literal_assign('../rerun.py', 'MINE')

def parse_text(t):
    w, b = t.split('/')
    w = set(w.replace('W:', '').split()); b = set(b.replace('B:', '').split())
    return w, b

def fen_pieces(fen):
    out = {}
    for i, row in enumerate(fen.split('/')):
        f = 0
        for ch in row:
            if ch.isdigit(): f += int(ch)
            else: out['abcdefgh'][f] if False else None; out['abcdefgh'[f] + str(8 - i)] = ch; f += 1
        assert f == 8
    return out

feats = myscan.main()
print('\n=== scan -> piece map (kings = bbox_w > 0.75) ===')
scan = {}
for key, fs in feats.items():
    m = {}
    for sq, (col, frac, wf, bf, bw, bh) in fs.items():
        kind = 'K' if bw > 0.75 else 'P'
        m[sq] = kind if col == 'W' else kind.lower()
    scan[key] = m
    print(key, ' '.join(f'{v}{k}' for k, v in sorted(m.items())))

print('\n=== (b) worker MINE vs my scan (all pieces, kings included) ===')
for key, fen in MINE.items():
    wm = fen_pieces(fen)
    print(key, 'MATCH' if wm == scan[key] else f'DIFF worker-only={set(wm.items())-set(scan[key].items())} scan-only={set(scan[key].items())-set(wm.items())}')

print('\n=== (a) CLAIMS vs my scan ===')
for label, text, claim in CLAIMS:
    key = label.split()[0]
    cw, cb = parse_text(text)
    sw = {s for s, p in scan[key].items() if p == 'P'}; sb = {s for s, p in scan[key].items() if p == 'p'}
    files = {s[0] for s in cw | cb}
    sw_f = {s for s in sw if s[0] in files}; sb_f = {s for s in sb if s[0] in files}
    full = (cw == sw and cb == sb)
    restricted = (cw == sw_f and cb == sb_f)
    kings = {s: p for s, p in scan[key].items() if p in 'Kk'}
    print(f'{label:32s} full-diagram-pawns: {"MATCH" if full else "DIFF"}; '
          f'restricted to files {"".join(sorted(files))}: {"MATCH" if restricted else "DIFF"}'
          + ('' if full else f'  [diagram-only W{sorted(sw-cw)} B{sorted(sb-cb)}; claims-only W{sorted(cw-sw)} B{sorted(cb-sb)}]')
          + (f'  kings in diagram not in CLAIMS: {kings}' if kings else ''))
covered = {l.split()[0] for l, _, _ in CLAIMS}
print('\nDiagrams with no CLAIMS entry:', sorted(set(scan) - covered))
