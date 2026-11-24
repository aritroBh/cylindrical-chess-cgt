"""K59: compare (B1) per non-shuttle Black root move between vgsum59 (sum rule beside -1, and the 1-pass game) and
K56's pr56 output ((N1) = Black's move loses against one Black pass, stalemate a draw; implies (B1)).
usage: cmp_p1.py <vgsum59 .out> <pr56 .out> <label>"""
import re, sys
vg, pr, lab = sys.argv[1:4]
V = {}  # (black king square at root, move) -> (B1, pass1)
cur = None
for line in open(vg):
    m = re.match(r'^root[AB]_b (\S+) (k\w+)', line)
    if m: cur = m.group(2)[1:]; continue
    if re.match(r'^root', line) or line.startswith('query') or line.startswith('peak'): cur = None; continue
    if cur and 'B1(' in line:
        mv = line.split()[0]
        b1 = re.search(r'B1\(sum rule, -1\)=(W|not W)', line).group(1)
        ps = re.search(r'stalemate draw: (W|not W)\]', line).group(1)
        V[(cur, mv)] = (b1, ps)
P = {}
cur = None
for line in open(pr):
    m = re.match(r'^root k(\w\d) (b|w) ', line)
    if m: cur = m.group(1) if m.group(2) == 'b' else None; continue
    if line.startswith('RESULT') or line.startswith('board'): cur = None; continue
    if cur:
        t = line.split()
        if not t or t[1] == 'shuttle': continue
        n1 = re.search(r'\(N1\) (yes|no)', line)
        if n1: P[(cur, t[0])] = n1.group(1)
bad = []
if set(V) != set(P): bad.append('move lists differ: vgsum only %s, pr56 only %s' % (sorted(set(V) - set(P)), sorted(set(P) - set(V))))
for k in sorted(set(V) & set(P)):
    b1, ps = V[k]
    if not (b1 == 'W' and ps == 'W' and P[k] == 'yes'): bad.append('%s %s: vgsum B1 %s, vgsum pass %s, pr56 N1 %s' % (k[0], k[1], b1, ps, P[k]))
print('%s: %d non-shuttle Black root moves (vgsum59), %d (pr56); %s' % (lab, len(V), len(P), 'AGREE, all W / N1 yes' if not bad else 'DIFFER'))
for b in bad: print('   ', b)
for k in sorted(V): print('    %s %-7s vgsum59 B1=%s pass1=%s | pr56 N1=%s' % (k[0], k[1], V[k][0], V[k][1], P.get(k, '?')))
