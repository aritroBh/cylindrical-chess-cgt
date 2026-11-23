"""confirm.py NAME m_lo m_hi : solve family members with mob1_32 and mob2_32, one ring (one width) per process."""
import sys, time, re, subprocess
from lib import M1, M2, npawns
FAMS = {
  'TT': lambda m: 'B5 W2 W6B7 W3 B7 B6 W3 W2 B6 W2' + ' B4 W2' * m,
  'SS': lambda m: 'B6 W3' + ' W2 B4' * m + ' W6B7 W3 B7 B6 W3 W2 B6 W2 B4',
  'E2': lambda m: 'B5 W3' + ' W2 B4' * m + ' W2 W4 B7 B7 W3 W2 W2B7 B7',
  'H2': lambda m: 'B5 W3' + ' W2 B4' * m + ' W4 B7 B7 W3 W2 W2B7 B7',
  'H4': lambda m: 'B5 W3 W4 B7' + ' W2 B4' * m + ' B7 W3 W2 W2B7 B7',
  'G6': lambda m: 'B7 W4 W23 B5 W3B7 W4B7' + ' W2 B4' * m,
}
def run(b, r):
    p = subprocess.run(['nice', '-n', '15', b, 'solve'], input=r + '\n', capture_output=True, text=True, timeout=1100)
    m = re.search(r'nodes (\d+)', p.stderr)
    return p.stdout.strip(), (m.group(1) if m else '?')
name, lo, hi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
for m in range(lo, hi + 1):
    r = FAMS[name](m); n = len(r.split())
    if n > 32: break
    t = time.time(); s1, k1 = run(M1, r); t1 = time.time() - t
    t = time.time(); s2, k2 = run(M2, r); t2 = time.time() - t
    print(f'{name} m={m} n={n} pawns={npawns(r)} mob1={s1} mob2={s2} mob1_nodes={k1} t1={t1:.1f}s t2={t2:.1f}s  [{r}]', flush=True)
