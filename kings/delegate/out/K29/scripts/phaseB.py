#!/usr/bin/env python3
"""phaseB.py NAME [TARGET_CPU_S]: Phase B of configuration NAME (a line of scripts/configs.txt).
Phase A (scripts/phaseA.sh) screened every symmetry-class representative against the first 300 contexts (grp2 sorted order) and
kept the survivors (R lines with 'differ 0').  Phase B runs the survivors against the REST of the contexts [300, nctx) in shards,
one heavy.sh call per shard (grp2 --first 1 --ctxlo LO --ctxhi HI), each shard sized to about TARGET_CPU_S CPU-seconds from the
measured rate of the previous shard, and feeds each shard only the groups that survived the previous ones.
Output: data/B_NAME.txt, R lines  'R Z | contexts_checked N differ D parking_mismatch P | first fail: ...'  for every phase-A survivor
(N = all contexts of the class when D = 0; for a failing group N = contexts checked up to and including the first failure,
counted within its shard only, so use the 'first fail' text, not N).  Log: logs/B_NAME.log (one line per shard)."""
import sys, re, subprocess, os, time
D = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/'
HEAVY = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh'
name = sys.argv[1]; target = float(sys.argv[2]) if len(sys.argv) > 2 else 600.0
cfiles = sys.argv[3] if len(sys.argv) > 3 else ''   # grp3 --cfiles: contexts restricted to these files (subclass run, starts at context 0)
cwb = os.environ.get('CWB', '2')   # context pawns per side (default 2)
tag = name + ('_cf_' + cfiles if cfiles else '') + ('_c' + cwb if cwb != '2' else '') + os.environ.get('TAGX', '')
cfg = [l.split() for l in open(D + 'scripts/configs.txt') if l.strip() and not l.startswith('#')]
cfg = {c[0]: c for c in cfg}[name]
_, board, zs, fz, dmin, rep = cfg
out_final = D + 'data/B_%s.txt' % tag
if os.path.exists(out_final) and os.path.getsize(out_final) > 0: sys.exit(0)
log = open(D + 'logs/B_%s.log' % tag, 'a')
def L(s): log.write(s + '\n'); log.flush()
surv = []
for l in open(D + 'data/' + os.environ.get('ASRC', 'A_%s.txt' % name)):
    m = re.match(r'R (.*?) \| contexts_checked (\d+) differ (\d+)', l)
    if m and m.group(3) == '0': surv.append((m.group(1), int(m.group(2))))
fails = []   # R lines of groups that failed in phase B
checked0 = {z: n for z, n in surv}
nctx = None
lo = int(os.environ.get('LO0', 0 if (cfiles or cwb != '2') else 300)); step = int(max(10, min(int(os.environ.get('STEPMAX', 300)), target / (0.3 * max(1, len(surv))))))
cur = [z for z, n in surv]
if not cfiles and cwb == '2' and all(n < 300 for z, n in surv):          # phase A already covered the whole class
    lo = 10**9
while cur and lo < 10**9 and (nctx is None or lo < nctx):
    hi = lo + step
    inp = D + 'data/B/in_%s.txt' % tag; outp = D + 'data/B/out_%s_%d.txt' % (tag, lo); errp = D + 'logs/B_%s_%d.err' % (tag, lo)
    open(inp, 'w').write('\n'.join(cur) + '\n')
    t0 = time.time()
    cmd = [HEAVY, '/usr/bin/time', '-l', D + ('bin/grp3' if cfiles else 'bin/grp2'), '--board', board, '--mode', 'test', '--zs', zs, '--fz', fz, '--dmin', dmin,
           '--cw', cwb, '--cb', cwb, '--first', '1'] + (['--cfiles', cfiles] if cfiles else []) + ['--ctxlo', str(lo), '--ctxhi', str(hi)]
    with open(inp) as fi, open(outp, 'w') as fo, open(errp, 'w') as fe:
        p = subprocess.Popen(cmd, stdin=fi, stdout=fo, stderr=fe)
        L('%s shard [%d,%d) groups %d pid %d started %s' % (name, lo, hi, len(cur), p.pid, time.strftime('%H:%M:%S')))
        p.wait()
    err = open(errp).read()
    m = re.search(r'contexts (\d+)', err); nctx = int(m.group(1))
    u = re.search(r'([\d.]+) user', err); cpu = float(u.group(1)) if u else 1.0
    rss = re.search(r'(\d+)\s+maximum resident', err)
    realhi = min(hi, nctx); n = realhi - lo
    nxt = []
    for l in open(outp):
        mm = re.match(r'R (.*?) \| contexts_checked (\d+) differ (\d+)', l)
        if not mm: continue
        if mm.group(3) == '0': nxt.append(mm.group(1))
        else: fails.append(l.rstrip('\n'))
    L('%s shard [%d,%d) done: nctx %d cpu %.0fs real %.0fs rss %.0fMB survivors %d failed %d' % (
        name, lo, realhi, nctx, cpu, time.time() - t0, int(rss.group(1)) / 1e6 if rss else -1, len(nxt), len(cur) - len(nxt)))
    groups_in = len(cur)
    cur = nxt
    lo = hi
    if cur:
        per = max(cpu, 1.0) / max(1, n) / max(1, groups_in)       # CPU-s per (group, context) in this shard
        step = int(max(10, min(int(os.environ.get('STEPMAX', 1500)), target / (per * len(cur)))))
with open(out_final + '.tmp', 'w') as f:
    for z, n in surv:
        if z in cur: f.write('R %s | contexts_checked %d differ 0 parking_mismatch 0 | first fail: none\n' % (z, nctx if nctx else n))
    for l in fails: f.write(l + '\n')
os.replace(out_final + '.tmp', out_final)
L('%s DONE %s survivors %d of %d' % (name, time.strftime('%H:%M:%S'), len(cur), len(surv)))
