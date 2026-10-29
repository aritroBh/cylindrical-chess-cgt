import sys
# orbits_own.py FILE W ZS FZ REFLECT(0/1)
fn, Wd, zs, fz, refl = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
H = 6
def parse(l):
    out = []
    for t in l.split():
        out.append((t[0], 'abcdefgh'.index(t[1]), int(t[2:])))
    return frozenset(out)
def swap(g):  # colour swap with rank flip
    return frozenset((c.swapcase(), f, H + 1 - r) for c, f, r in g)
def mirror(g):
    return frozenset((c, (2 * zs + fz - 1 - f) % Wd, r) for c, f, r in g)
G = set(parse(l) for l in open(fn) if l.strip())
seen = set(); orb = 0; closed = True
for g in G:
    if g in seen: continue
    orb += 1
    stack = [g]; seen.add(g)
    while stack:
        x = stack.pop()
        imgs = [swap(x)] + ([mirror(x)] if refl else [])
        for y in imgs:
            if y not in G: closed = False
            if y not in seen and y in G: seen.add(y); stack.append(y)
print(fn.split('/')[-1], 'groups', len(G), 'classes', orb, 'closed', closed)
