# Re-check the near-miss placements with ref3m (K23 solver) only: roots, freezes, q values. Prints per placement the
# U1..U4 status of each root. Usage: python3 near_ref3m.py REF3M BOARD < list (lines: "<pieces> shuttle z0z1")
import subprocess, sys
REF, BOARD = sys.argv[1], sys.argv[2]
def ref(lines, moves=False):
    a = [REF, '--board', BOARD] + (['--moves'] if moves else [])
    out = subprocess.run(a, input='\n'.join(lines) + '\n', capture_output=True, text=True).stdout.strip().split('\n')
    return out
def parse(s):
    t = s.split(); return t
def apply(pieces, mv, side):
    mv = (mv[0].upper() if side == 'w' else mv[0].lower()) + mv[1:]
    # mv like Kb5a6 or Pc5c4 or Pa2a4 or Pb5xc6 forms: piece letter + from + to (+promo?)
    pc, fr, to = mv[0], mv[1:3], mv[3:5]
    side = 'w' if pc.isupper() else 'b'
    new = [p for p in pieces if p[1:] != to and p != pc + fr]
    ep = '-'
    if pc in 'Pp':
        df = ord(to[0]) - ord(fr[0]); dr = int(to[1]) - int(fr[1])
        if df != 0 and not any(p[1:] == to for p in pieces):  # e.p. capture
            cap = to[0] + fr[1]; new = [p for p in new if p[1:] != cap]
        if abs(dr) == 2: ep = fr[0] + str((int(fr[1]) + int(to[1])) // 2)
    new.append(pc + to)
    return new, ep
for line in sys.stdin:
    t = line.split()
    if not t: continue
    pieces = [x for x in t if x[0] in 'KkPp' and len(x) == 3]
    sh = t[t.index('shuttle') + 1]; z = [sh[:2], sh[2:4]]
    wk = [p for p in pieces if p[0] == 'K'][0][1:]; S = 'K' if wk in z else 'k'
    rest = [p for p in pieces if p[0] != S]
    res = []
    for a in (0, 1):
        root = rest + [S + z[a]]
        sstm = 'w' if S == 'K' else 'b'; fstm = 'b' if S == 'K' else 'w'
        sw = 'W' if sstm == 'w' else 'L'   # shuttler wins (White's view)
        fw = 'L' if sstm == 'w' else 'W'   # freezer wins
        r1 = ref([' '.join(root) + ' ' + sstm + ' -'], True)[0]
        mv = [x.split(':') for x in r1.split('|')[1].split()[1:]]
        u1 = all(v == fw for m, v in mv if m != S + z[a] + z[1 - a]) and any(m == S + z[a] + z[1 - a] for m, v in mv)
        r2 = ref([' '.join(root) + ' ' + fstm + ' -'], True)[0]
        mv2 = [x.split(':') for x in r2.split('|')[1].split()[1:]]
        frz = [m for m, v in mv2 if v != sw]
        u3 = u4 = True
        for m in frz:
            q, ep = apply(root, m, fstm)
            qa = ref([' '.join(q) + ' ' + sstm + ' ' + ep], True)[0]
            qv = qa.split('|')[1].split()
            if not (qv[0] == fw and len(qv) > 1): u3 = False
            qb = ref([' '.join(q) + ' ' + fstm + ' -'], True)[0]
            qbv = qb.split('|')[1].split()
            if not (qbv[0] == sw and len(qbv) > 1): u4 = False
        res.append(f"root {z[a]}: U1={u1} freezes={frz} U3={u3} U4={u4}")
    print(line.strip(), '||', ' ; '.join(res))
