import sys, subprocess
RG = sys.argv[1]
hits = [l.split('\t')[0] for l in open('/Users/aritro/Downloads/Research/Chessendgames/research/star26_rings/c8/p10_5_5_hits.tsv')]
def parse(t, n=8):
    w, b = t.split('/')
    files = [[[], []] for _ in range(n)]
    for s in w.replace('W:', '').split(): files['abcdefghijklmnop'.index(s[0])][0].append(int(s[1]))
    for s in b.replace('B:', '').split(): files['abcdefghijklmnop'.index(s[0])][1].append(int(s[1]))
    return files
def tok(f):
    t = ('W' + ''.join(map(str, sorted(f[0]))) if f[0] else '') + ('B' + ''.join(map(str, sorted(f[1]))) if f[1] else '')
    return t or '-'
def solve(lines):
    out = subprocess.run([RG, 'solve', '3'], input='\n'.join(lines) + '\n', capture_output=True, text=True).stdout.split('\n')
    return [o.split()[0] for o in out if o.strip()]
cands = []
for t in hits:
    files = parse(t)
    for pos in range(8):            # insert new file before index pos
        for col in (0, 1):
            for r in range(2, 8):
                nf = [[[], []]]; nf[0][col] = [r]
                new = files[:pos] + nf + files[pos:]
                cands.append((t, pos, 'WB'[col] + str(r), ' '.join(tok(f) for f in new)))
sig = solve([c[3] for c in cands])
hit = [(c, s) for c, s in zip(cands, sig) if s == 'NNPN']
print(len(cands), 'C9 candidates;', len(hit), 'are *2 (NNPN)')
seen = set()
for c, s in hit:
    if c[3] in seen: continue
    seen.add(c[3]); print(c[3], '| from', c[0], 'insert', c[2], 'at', c[1])
