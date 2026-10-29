#!/usr/bin/env python3
"""sym.py BOARD ZS FZ ENUMFILE -> one line per symmetry class: 'rep | dw db | class size | members'.
Symmetries that preserve the pair (board, F_Z, context class): colour swap with rank flip (r -> H+1-r), and the file
reflection f -> 2*zs+fz-1-f (mod W on a cylinder; only if it maps the board to itself on a flat board)."""
import sys
board, zs, fz, fn = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
kind, dims = board.split(':'); W, H = map(int, dims.split('x'))
cyl = kind == 'cyl'
refl_ok = cyl or (2*zs+fz-1 == W-1)
def parse(z):
    out = []
    for t in z.split():
        out.append((t[0], ord(t[1])-97, int(t[2:])))
    return out
def fmt(p):
    # canonical order: K, P..., k, p...
    key = {'K':0,'P':1,'k':2,'p':3}
    return ' '.join(f"{c}{chr(97+f)}{r}" for c,f,r in sorted(p, key=lambda x:(key[x[0]],x[1],x[2])))
def colour(p): return [({'K':'k','k':'K','P':'p','p':'P'}[c], f, H+1-r) for c,f,r in p]
def refl(p): return [(c, (2*zs+fz-1-f) % W if cyl else 2*zs+fz-1-f, r) for c,f,r in p]
classes = {}
for l in open(fn):
    l = l.strip()
    if not l or l.startswith('#'): continue
    z, d = l.split(' | ')
    dw, db = map(int, d.split())
    p = parse(z)
    imgs = [(p, (dw,db))]
    imgs.append((colour(p), (db,dw)))
    if refl_ok:
        imgs.append((refl(p), (dw,db))); imgs.append((refl(colour(p)), (db,dw)))
    best = min(imgs, key=lambda x: fmt(x[0]))
    k = fmt(best[0])
    classes.setdefault(k, [best[1], []])[1].append(z)
for k in sorted(classes):
    d, mem = classes[k]
    print(f"{k} | {d[0]} {d[1]} | {len(mem)} | {'; '.join(mem)}")
