#!/usr/bin/env python3
"""chainV.py NAME CTXFILES PW PB BATCH [WAIT]: verification of the final survivors of configuration NAME over ALL their contexts with
kp_p --pmodel and ref3 (Phi) and kpsolve --frozen and ref3 --frozen (Psi, parked kings on PW/PB): scripts/ver2.sh, one heavy.sh call per
batch of BATCH groups.  Survivors are the 'differ 0' lines of data/B_NAME.txt (waits for it if WAIT is given) or of data/A_NAME.txt when phase A
covered all contexts.  Output data/ver_*.cmp, logs/V_NAME.log."""
import sys, re, subprocess, os, time
D = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/'
HEAVY = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh'
name, cf, pw, pb, batch = sys.argv[1:6]; batch = int(batch); wait = len(sys.argv) > 6
cfg = {l.split()[0]: l.split() for l in open(D + 'scripts/configs.txt') if l.strip() and not l.startswith('#')}[name]
board = cfg[1]; rb = board.replace('flat:', 'flat')   # ref3 spells the flat board flat7x6
tag = os.environ.get('BTAG', name)
src = D + 'data/B_%s.txt' % tag
if wait:
    while not os.path.exists(src): time.sleep(30)
if not os.path.exists(src): src = D + 'data/A_%s.txt' % name
surv = [m.group(1) for m in (re.match(r'R (.*?) \| contexts_checked (\d+) differ 0 ', l) for l in open(src)) if m]
log = open(D + 'logs/V_%s.log' % tag, 'a')
log.write('%s: %d survivors from %s\n' % (name, len(surv), os.path.basename(src))); log.flush()
for i in range(0, len(surv), batch):
    grp = surv[i:i + batch]
    t0 = time.time()
    with open(D + 'logs/V_%s.out' % tag, 'a') as fo, open(D + 'logs/V_%s.err' % tag, 'a') as fe:
        p = subprocess.Popen([HEAVY, '/usr/bin/time', '-l', 'zsh', D + 'scripts/ver2.sh', tag, board, rb, cf, pw, pb] + grp, stdout=fo, stderr=fe, cwd=D)
        log.write('%s batch %d (%d groups) pid %d started %s\n' % (name, i // batch, len(grp), p.pid, time.strftime('%H:%M:%S'))); log.flush()
        p.wait()
    log.write('%s batch %d done real %.0fs\n' % (name, i // batch, time.time() - t0)); log.flush()
log.write('%s VERDONE %s\n' % (name, time.strftime('%H:%M:%S'))); log.flush()
